import { useState } from 'react';
import { Frame, Select, Slider, Toggle, fmt, type WidgetProps } from './common';

export interface ModelCfg {
  label: string;
  layers: number;
  d: number;
  heads: number;
  vocab: number;
}

export const MODELS: Record<string, ModelCfg> = {
  m124: { label: '124M: 12 layers, d=768', layers: 12, d: 768, heads: 12, vocab: 50257 },
  b1_3: { label: '1.3B: 24 layers, d=2048', layers: 24, d: 2048, heads: 16, vocab: 50257 },
  b6_7: { label: '6.7B: 32 layers, d=4096', layers: 32, d: 4096, heads: 32, vocab: 50257 },
  b13: { label: '13B: 40 layers, d=5120', layers: 40, d: 5120, heads: 40, vocab: 50257 },
  b175: { label: '175B: 96 layers, d=12288', layers: 96, d: 12288, heads: 96, vocab: 50257 },
};

// Capacities in bytes: the cards are sold as 16, 40 and 80 GB but hold 15,360, 40,960 and 81,920 MiB.
export const GPUS = {
  t4: { label: 'T4, 16.1 GB', bytes: 15360 * 2 ** 20 },
  a100_40: { label: 'A100 40GB, 42.9 GB', bytes: 40960 * 2 ** 20 },
  gpu80: { label: 'A100 or H100 80GB, 85.9 GB', bytes: 81920 * 2 ** 20 },
} as const;
export type GpuId = keyof typeof GPUS;

// Weights and the 4h MLP: 12 d^2 per layer, plus the (tied) embedding.
export const paramCount = (m: ModelCfg) => 12 * m.layers * m.d ** 2 + m.vocab * m.d;

// Mixed-precision Adam (Rajbhandari et al. 2020): 2 bytes of 16-bit weights, 2 of 16-bit gradients
// and 12 of fp32 master weights, momentum and variance per parameter. ZeRO stage k shards the first
// k of {optimizer states, gradients, weights} over the nd data-parallel ranks.
export function modelStates(psi: number, zero: number, nd: number) {
  return {
    weights: zero >= 3 ? (2 * psi) / nd : 2 * psi,
    grads: zero >= 2 ? (2 * psi) / nd : 2 * psi,
    optim: zero >= 1 ? (12 * psi) / nd : 12 * psi,
  };
}

// Activation bytes stored per transformer layer for one micro-batch in 16-bit training
// (Korthikanti et al. 2022): s b h (34 + 5 a s / h), divided by t under tensor and sequence parallelism.
// FlashAttention does not store the s x s attention matrices, removing the 5 a s / h term.
export function activationsPerLayer(s: number, b: number, h: number, a: number, t: number, flash: boolean) {
  return (s * b * h * (34 + (flash ? 0 : (5 * a * s) / h))) / t;
}

export interface Plan {
  model: ModelCfg;
  dp: number;
  tp: number;
  pp: number;
  zero: number;
  micro: number; // micro-batch size b
  seq: number;
  accum: number; // micro-batches per step per data-parallel rank, m
  checkpoint: boolean;
  flash: boolean;
}

export function planMemory(p: Plan) {
  const { model: m, dp, tp, pp } = p;
  const psi = paramCount(m) / (tp * pp);
  const states = modelStates(psi, p.zero, dp);
  const layersPerStage = Math.ceil(m.layers / pp);
  // 1F1B pipeline schedule: the first stage holds activations of up to pp micro-batches at once.
  const inFlight = Math.min(pp, p.accum);
  const full = activationsPerLayer(p.seq, p.micro, m.d, m.heads, tp, p.flash);
  // Full checkpointing keeps only each layer's 16-bit input, and rebuilds one layer at a time in backward.
  const activations = p.checkpoint
    ? layersPerStage * inFlight * ((2 * p.seq * p.micro * m.d) / tp) + full
    : layersPerStage * inFlight * full;
  const total = states.weights + states.grads + states.optim + activations;
  return { psi, ...states, activations, total, layersPerStage };
}

export const bubbleFraction = (pp: number, m: number) => (pp - 1) / (m + pp - 1);

// Bytes each GPU sends per optimizer step. Ring all-reduce of 16-bit gradients: 2 (n-1)/n of them;
// ZeRO-3 also all-gathers the weights in forward and in backward: 3 (n-1)/n.
export function dpTraffic(psi: number, zero: number, nd: number) {
  if (nd === 1) return 0;
  return ((zero >= 3 ? 3 : 2) * (nd - 1) * 2 * psi) / nd;
}

// Tensor parallelism: per layer and micro-batch, two all-reduces of the s x b x h activations in
// forward and two in backward, each costing 2 (t-1)/t of the message per GPU.
export function tpTraffic(p: Plan) {
  if (p.tp === 1) return 0;
  const msg = 2 * p.seq * p.micro * p.model.d;
  return 4 * Math.ceil(p.model.layers / p.pp) * p.accum * ((2 * (p.tp - 1)) / p.tp) * msg;
}

const GB = 1e9;
const PARTS = [
  { key: 'weights', label: 'weights', cls: 'bar-a' },
  { key: 'grads', label: 'gradients', cls: 'bar-b' },
  { key: 'optim', label: 'optimizer states', cls: 'bar-c' },
  { key: 'activations', label: 'activations', cls: 'bar-d' },
] as const;

export default function ParallelismPlanner({ props }: WidgetProps) {
  const [modelId, setModelId] = useState<string>(props.model in MODELS ? props.model : 'b6_7');
  const [gpu, setGpu] = useState<GpuId>('gpu80');
  const [dpLog, setDpLog] = useState(Number(props.dp ?? 3));
  const [tpLog, setTpLog] = useState(0);
  const [ppLog, setPpLog] = useState(0);
  const [zero, setZero] = useState('0');
  const [microLog, setMicroLog] = useState(0);
  const [seqLog, setSeqLog] = useState(11);
  const [accLog, setAccLog] = useState(3);
  const [checkpoint, setCheckpoint] = useState(false);
  const [flash, setFlash] = useState(true);
  const model = MODELS[modelId];
  const plan: Plan = {
    model,
    dp: 2 ** dpLog,
    tp: 2 ** tpLog,
    pp: 2 ** ppLog,
    zero: Number(zero),
    micro: 2 ** microLog,
    seq: 2 ** seqLog,
    accum: 2 ** accLog,
    checkpoint,
    flash,
  };
  const mem = planMemory(plan);
  const cap = GPUS[gpu].bytes;
  const gpus = plan.dp * plan.tp * plan.pp;
  const scaleMax = Math.max(cap, mem.total) * 1.05;
  const W = 420;
  const status = mem.total > cap ? 'does not fit' : mem.total > 0.9 * cap ? 'tight: over 90% of the card' : 'fits';
  const warnings = [
    model.heads % plan.tp ? `${model.heads} heads do not split evenly over ${plan.tp} tensor-parallel ranks` : '',
    model.layers % plan.pp ? `${model.layers} layers do not split evenly over ${plan.pp} pipeline stages` : '',
  ].filter(Boolean);
  let x0 = 0;
  return (
    <Frame
      title="Parallelism planner: memory per GPU"
      caption={
        <>
          Mixed-precision Adam at 16 bytes per parameter, ZeRO sharding over the data-parallel ranks, activations of the first pipeline stage under
          a 1F1B schedule. Output logits, temporary buffers and the framework's own reserve are not counted. GB means 10^9 bytes.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} 54`} className="widget-svg" role="img" aria-label={`Memory per GPU: ${fmt(mem.total / GB, 1)} GB of ${fmt(cap / GB, 1)} GB`}>
        {PARTS.map((part) => {
          const w = (mem[part.key] / scaleMax) * (W - 2);
          const r = <rect key={part.key} x={1 + x0} y={8} width={Math.max(0, w)} height={24} className={part.cls} />;
          x0 += w;
          return r;
        })}
        <line x1={1 + (cap / scaleMax) * (W - 2)} x2={1 + (cap / scaleMax) * (W - 2)} y1={2} y2={38} className="cap-line" />
        <text x={Math.min(W - 4, 1 + (cap / scaleMax) * (W - 2))} y={50} textAnchor="end">
          card capacity
        </text>
      </svg>
      <ul className="legend-row">
        {PARTS.map((part) => (
          <li key={part.key}>
            <svg width="12" height="12" aria-hidden="true" className="widget-svg legend-swatch">
              <rect width="12" height="12" className={part.cls} />
            </svg>
            {part.label} {fmt(mem[part.key] / GB, 2)} GB
          </li>
        ))}
      </ul>
      <div className="widget-stats" aria-live="polite">
        <span>
          {fmt(mem.total / GB, 2)} GB per GPU: {status}
        </span>
        <span>
          {gpus} GPUs, {fmt(paramCount(model) / 1e9, 2)}B parameters, {fmt(mem.psi / 1e9, 3)}B per model-parallel shard
        </span>
        <span>
          tokens per step {(plan.dp * plan.accum * plan.micro * plan.seq).toLocaleString('en-US')}; pipeline bubble{' '}
          {fmt(100 * bubbleFraction(plan.pp, plan.accum), 1)}%
        </span>
        <span>
          traffic per GPU per step: data parallel {fmt(dpTraffic(mem.psi, plan.zero, plan.dp) / GB, 2)} GB, tensor parallel{' '}
          {fmt(tpTraffic(plan) / GB, 2)} GB
        </span>
        {warnings.map((w) => (
          <span key={w} className="warn">
            {w}
          </span>
        ))}
      </div>
      <div className="widget-controls grid2">
        <Select
          label="Model"
          value={modelId}
          options={Object.entries(MODELS).map(([k, v]) => ({ value: k, label: v.label }))}
          onChange={setModelId}
        />
        <Select label="GPU" value={gpu} options={(Object.keys(GPUS) as GpuId[]).map((k) => ({ value: k, label: GPUS[k].label }))} onChange={setGpu} />
        <Select
          label="ZeRO stage"
          value={zero}
          options={[
            { value: '0', label: '0: plain data parallel' },
            { value: '1', label: '1: shard optimizer states' },
            { value: '2', label: '2: + gradients' },
            { value: '3', label: '3: + weights (FSDP)' },
          ]}
          onChange={setZero}
        />
        <Slider label="Data parallel" value={dpLog} min={0} max={10} step={1} onChange={setDpLog} format={(v) => String(2 ** v)} />
        <Slider label="Tensor parallel" value={tpLog} min={0} max={3} step={1} onChange={setTpLog} format={(v) => String(2 ** v)} />
        <Slider label="Pipeline stages" value={ppLog} min={0} max={4} step={1} onChange={setPpLog} format={(v) => String(2 ** v)} />
        <Slider label="Micro-batch size" value={microLog} min={0} max={4} step={1} onChange={setMicroLog} format={(v) => String(2 ** v)} />
        <Slider label="Sequence length" value={seqLog} min={9} max={13} step={1} onChange={setSeqLog} format={(v) => String(2 ** v)} />
        <Slider label="Micro-batches per step" value={accLog} min={0} max={6} step={1} onChange={setAccLog} format={(v) => String(2 ** v)} />
      </div>
      <div className="widget-controls">
        <Toggle label="Activation checkpointing" checked={checkpoint} onChange={setCheckpoint} />
        <Toggle label="FlashAttention" checked={flash} onChange={setFlash} />
      </div>
    </Frame>
  );
}
