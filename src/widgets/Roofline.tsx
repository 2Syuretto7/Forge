import { useState } from 'react';
import { Frame, Select, Slider, Toggle, type WidgetProps, fmt } from './common';
import { LinePlot, type Series } from './plot';

// Peak dense throughput (FLOP/s) and memory bandwidth (bytes/s) from the
// vendors' public datasheets. "fp16" means tensor-core half precision
// (fp16 on the T4, bf16 or fp16 on A100 and H100), without sparsity.
export const HARDWARE = {
  t4: { label: 'NVIDIA T4 (Colab)', peak: { fp32: 8.1e12, fp16: 65e12 }, bw: 320e9 },
  a100: { label: 'NVIDIA A100 80GB SXM', peak: { fp32: 19.5e12, fp16: 312e12 }, bw: 2039e9 },
  h100: { label: 'NVIDIA H100 SXM', peak: { fp32: 67e12, fp16: 989e12 }, bw: 3350e9 },
} as const;
export type HardwareId = keyof typeof HARDWARE;
export type Precision = 'fp32' | 'fp16';

export const attainable = (peak: number, bw: number, intensity: number) => Math.min(peak, bw * intensity);
export const ridge = (peak: number, bw: number) => peak / bw;

export interface Kernel {
  name: string;
  short: string;
  flops: number;
  bytes: number;
}

// FLOPs and the minimum bytes moved to and from memory, each operand read once
// and each result written once.
export function kernels(n: number, bytesPer: number, seq = 2048, headDim = 64): Kernel[] {
  const N = 1 << 24; // elements for the elementwise kernels
  return [
    { name: 'vector add', short: 'add', flops: N, bytes: 3 * N * bytesPer },
    { name: 'softmax (rows)', short: 'softmax', flops: 5 * N, bytes: 2 * N * bytesPer },
    { name: 'layer norm', short: 'layer norm', flops: 8 * N, bytes: 2 * N * bytesPer },
    { name: `attention scores QK^T (L=${seq})`, short: 'QK^T', flops: 2 * seq * seq * headDim, bytes: bytesPer * (2 * seq * headDim + seq * seq) },
    { name: `matmul ${n}x${n}x${n}`, short: `matmul ${n}`, flops: 2 * n * n * n, bytes: 3 * n * n * bytesPer },
  ];
}

export const intensity = (k: Kernel) => k.flops / k.bytes;

export default function Roofline({ props }: WidgetProps) {
  const [hw, setHw] = useState<HardwareId>((props.hardware as HardwareId) in HARDWARE ? (props.hardware as HardwareId) : 't4');
  const [prec, setPrec] = useState<Precision>(props.precision === 'fp32' ? 'fp32' : 'fp16');
  const [logN, setLogN] = useState(Math.log2(Number(props.n) || 1024));
  const [both, setBoth] = useState(false);
  const h = HARDWARE[hw];
  const peak = h.peak[prec];
  const n = Math.round(2 ** logN);
  const bytesPer = prec === 'fp32' ? 4 : 2;
  const ks = kernels(n, bytesPer);
  const xs: [number, number] = [0.05, 2000];
  const curve = (p: number): [number, number][] =>
    Array.from({ length: 121 }, (_, i) => {
      const I = xs[0] * (xs[1] / xs[0]) ** (i / 120);
      return [I, attainable(p, h.bw, I) / 1e12];
    });
  const other: Precision = prec === 'fp32' ? 'fp16' : 'fp32';
  const series: Series[] = [{ points: curve(peak), cls: 'series-a', label: `roofline, ${prec}` }];
  if (both) series.push({ points: curve(h.peak[other]), cls: 'series-b', label: `roofline, ${other}`, dashed: true });
  const R = ridge(peak, h.bw);
  return (
    <Frame
      title="The roofline: arithmetic intensity against achievable throughput"
      caption={
        <>
          {h.label}, {prec}: peak {fmt(peak / 1e12, 1)} TFLOP/s, bandwidth {fmt(h.bw / 1e9, 0)} GB/s, ridge point {fmt(R, 1)} FLOP/byte. Kernels left of the ridge are
          memory-bound: no amount of extra compute speeds them up, only moving fewer bytes does.
        </>
      }
    >
      <LinePlot
        series={series}
        xDomain={xs}
        yDomain={[0.01, 2000]}
        xlog
        ylog
        xlabel="arithmetic intensity (FLOP per byte)"
        ylabel="TFLOP/s"
        label="Roofline plot with kernels placed by arithmetic intensity"
      >
        {(x, y) => (
          <g>
            <line x1={x(R)} x2={x(R)} y1={y(0.01)} y2={y(peak / 1e12)} className="grid-line" strokeDasharray="3 3" />
            {ks.map((k, i) => {
              const I = intensity(k);
              const perf = attainable(peak, h.bw, I) / 1e12;
              return (
                <g key={k.name}>
                  <circle cx={x(I)} cy={y(perf)} r={4.5} className={i === ks.length - 1 ? 'dot-c' : 'dot-b'} />
                  <text x={x(I) + (x(I) > 300 ? -7 : 7)} y={y(perf) + (i % 2 ? 14 : -7)} textAnchor={x(I) > 300 ? 'end' : 'start'}>
                    {k.short}
                  </text>
                </g>
              );
            })}
          </g>
        )}
      </LinePlot>
      <table className="widget-table">
        <thead>
          <tr>
            <th>kernel</th>
            <th>FLOP/byte</th>
            <th>attainable TFLOP/s</th>
            <th>bound by</th>
          </tr>
        </thead>
        <tbody>
          {ks.map((k) => {
            const I = intensity(k);
            return (
              <tr key={k.name}>
                <td>{k.name}</td>
                <td>{fmt(I, 2)}</td>
                <td>{fmt(attainable(peak, h.bw, I) / 1e12, 2)}</td>
                <td>{I < R ? 'memory' : 'compute'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <div className="widget-controls grid2">
        <Select
          label="GPU"
          value={hw}
          options={(Object.keys(HARDWARE) as HardwareId[]).map((k) => ({ value: k, label: HARDWARE[k].label }))}
          onChange={setHw}
        />
        <Select
          label="Precision"
          value={prec}
          options={[
            { value: 'fp16', label: 'fp16 / bf16 tensor cores' },
            { value: 'fp32', label: 'fp32' },
          ]}
          onChange={setPrec}
        />
        <Slider label="Matmul size n" value={logN} min={4} max={14} step={1} onChange={setLogN} format={(v) => String(2 ** v)} />
      </div>
      <div className="widget-controls">
        <Toggle label="Show the other precision's roof" checked={both} onChange={setBoth} />
      </div>
    </Frame>
  );
}
