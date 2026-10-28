import { useState } from 'react';
import { Frame, Select, Slider, fmt, type WidgetProps } from './common';
import { LinePlot, type Series } from './plot';

export interface ArchCfg {
  label: string;
  params: number;
  layers: number;
  heads: number;
  kvHeads: number;
  headDim: number;
}

// Published architectures: GPT-2 small; Llama 2 7B (multi-head attention); Mistral 7B and Llama 2 70B
// (grouped-query attention with 8 key-value heads).
export const ARCHS: Record<string, ArchCfg> = {
  gpt2: { label: 'GPT-2 small (124M, MHA)', params: 124e6, layers: 12, heads: 12, kvHeads: 12, headDim: 64 },
  llama7: { label: 'Llama 2 7B (MHA)', params: 6.74e9, layers: 32, heads: 32, kvHeads: 32, headDim: 128 },
  mistral7: { label: 'Mistral 7B (GQA, 8 KV heads)', params: 7.24e9, layers: 32, heads: 32, kvHeads: 8, headDim: 128 },
  llama70: { label: 'Llama 2 70B (GQA, 8 KV heads)', params: 69e9, layers: 80, heads: 64, kvHeads: 8, headDim: 128 },
};

export const CACHE_BYTES = { fp16: 2, fp8: 1, int4: 0.5 } as const;
export type CachePrecision = keyof typeof CACHE_BYTES;

// Capacity in bytes and memory bandwidth in bytes per second.
export const INFER_GPUS = {
  t4: { label: 'T4 (16 GB, 320 GB/s)', bytes: 15360 * 2 ** 20, bw: 320e9 },
  a100: { label: 'A100 80GB (2.0 TB/s)', bytes: 81920 * 2 ** 20, bw: 2039e9 },
  h100: { label: 'H100 80GB (3.35 TB/s)', bytes: 81920 * 2 ** 20, bw: 3350e9 },
} as const;
export type InferGpu = keyof typeof INFER_GPUS;

// Keys and values for every layer and key-value head: 2 x layers x kv_heads x head_dim numbers per token.
export const kvBytesPerToken = (a: ArchCfg, bytes: number) => 2 * a.layers * a.kvHeads * a.headDim * bytes;
export const kvBytes = (a: ArchCfg, bytes: number, batch: number, tokens: number) => kvBytesPerToken(a, bytes) * batch * tokens;

// Largest batch whose cache fits next to the weights (rounded down), and the decode step time when
// every step reads all weights and the whole cache once: decoding is bound by memory bandwidth.
export function maxBatch(a: ArchCfg, weightBytes: number, cacheBytes: number, tokens: number, capacity: number) {
  const free = capacity - a.params * weightBytes;
  return free <= 0 ? 0 : Math.floor(free / kvBytes(a, cacheBytes, 1, tokens));
}
export const decodeStepSeconds = (a: ArchCfg, weightBytes: number, kv: number, bw: number) => (a.params * weightBytes + kv) / bw;

const GB = 2 ** 30;

export default function KVCacheMeter({ props }: WidgetProps) {
  const [arch, setArch] = useState<string>(props.model in ARCHS ? props.model : 'llama7');
  const [gpu, setGpu] = useState<InferGpu>('a100');
  const [prec, setPrec] = useState<CachePrecision>('fp16');
  const [weights, setWeights] = useState<'2' | '1' | '0.5'>('2');
  const [batchLog, setBatchLog] = useState(4);
  const [ctxLog, setCtxLog] = useState(12);
  const a = ARCHS[arch];
  const g = INFER_GPUS[gpu];
  const wb = Number(weights);
  const cb = CACHE_BYTES[prec];
  const batch = 2 ** batchLog;
  const tokens = 2 ** ctxLog;
  const kv = kvBytes(a, cb, batch, tokens);
  const wTotal = a.params * wb;
  const fits = wTotal + kv <= g.bytes;
  const step = decodeStepSeconds(a, wb, kv, g.bw);
  const xs: [number, number] = [256, 131072];
  const curve = (b: number): [number, number][] =>
    Array.from({ length: 81 }, (_, i) => {
      const t = xs[0] * (xs[1] / xs[0]) ** (i / 80);
      return [t, (wTotal + kvBytes(a, cb, b, t)) / GB];
    });
  const series: Series[] = [
    { points: curve(batch), cls: 'series-a', label: `weights + cache, batch ${batch}` },
    { points: curve(1), cls: 'series-b', label: 'batch 1', dashed: true },
  ];
  const yMax = Math.max(g.bytes / GB, wTotal / GB) * 1.6;
  return (
    <Frame
      title="KV cache: memory per token, per sequence, per batch"
      caption={
        <>
          Each generated token stores a key and a value per layer and per key-value head: {fmt(kvBytesPerToken(a, cb) / 2 ** 10, 1)} KiB per token for{' '}
          {a.label} in {prec}. Grouped-query attention shares each key-value head among several query heads and divides the cache accordingly. The
          decode estimate assumes each step reads all weights and the whole cache once.
        </>
      }
    >
      <LinePlot
        series={series}
        xDomain={xs}
        yDomain={[0.1, yMax]}
        xlog
        ylog
        xlabel="tokens per sequence"
        ylabel="memory (GiB)"
        label="Weights plus KV cache memory against sequence length"
      >
        {(x, y) => (
          <g>
            <line x1={x(xs[0])} x2={x(xs[1])} y1={y(g.bytes / GB)} y2={y(g.bytes / GB)} className="cap-line" />
            <line x1={x(tokens)} x2={x(tokens)} y1={y(0.1)} y2={y(yMax)} className="cursor-line" />
          </g>
        )}
      </LinePlot>
      <div className="widget-stats" aria-live="polite">
        <span>
          weights {fmt(wTotal / GB, 2)} GiB + cache {fmt(kv / GB, 2)} GiB = {fmt((wTotal + kv) / GB, 2)} GiB of {fmt(g.bytes / GB, 0)}:{' '}
          {fits ? 'fits' : 'does not fit'}
        </span>
        <span>
          at {tokens.toLocaleString('en-US')} tokens, at most {maxBatch(a, wb, cb, tokens, g.bytes).toLocaleString('en-US')} sequences fit
        </span>
        <span>
          decode step {fmt(step * 1000, 2)} ms: {fmt(1 / step, 1)} tokens/s per sequence, {fmt(batch / step, 0)} tokens/s in total
        </span>
      </div>
      <div className="widget-controls grid2">
        <Select label="Model" value={arch} options={Object.entries(ARCHS).map(([k, v]) => ({ value: k, label: v.label }))} onChange={setArch} />
        <Select label="GPU" value={gpu} options={(Object.keys(INFER_GPUS) as InferGpu[]).map((k) => ({ value: k, label: INFER_GPUS[k].label }))} onChange={setGpu} />
        <Select
          label="Weights"
          value={weights}
          options={[
            { value: '2', label: '16-bit' },
            { value: '1', label: 'int8' },
            { value: '0.5', label: 'int4' },
          ]}
          onChange={setWeights}
        />
        <Select
          label="Cache"
          value={prec}
          options={(Object.keys(CACHE_BYTES) as CachePrecision[]).map((k) => ({ value: k, label: k }))}
          onChange={setPrec}
        />
        <Slider label="Batch (sequences)" value={batchLog} min={0} max={8} step={1} onChange={setBatchLog} format={(v) => String(2 ** v)} />
        <Slider label="Tokens per sequence" value={ctxLog} min={8} max={17} step={1} onChange={setCtxLog} format={(v) => (2 ** v).toLocaleString('en-US')} />
      </div>
    </Frame>
  );
}
