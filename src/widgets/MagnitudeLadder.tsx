import { useState } from 'react';
import { Frame, Slider, Toggle, type WidgetProps } from './common';

// A Fermi estimate as a product of uncertain factors, placed on a ladder of powers of ten.
// Each factor has a low and a high guess; in log units the estimate's centre is the sum of
// the factors' centres, the worst case adds their half-widths, and a typical error adds
// them in quadrature because independent errors partly cancel (M01, Derivation).

export interface Factor {
  name: string;
  lo: number; // log10 of the low guess
  hi: number; // log10 of the high guess
  divide?: boolean;
}

export function combine(fs: Factor[]) {
  let mid = 0;
  let worst = 0;
  let sq = 0;
  for (const f of fs) {
    const c = (f.lo + f.hi) / 2;
    const h = Math.abs(f.hi - f.lo) / 2;
    mid += f.divide ? -c : c;
    worst += h;
    sq += h * h;
  }
  return { mid, worst, typical: Math.sqrt(sq) };
}

const L = Math.log10;

export const PRESETS: Record<string, { title: string; unit: string; truth: number; truthLabel: string; factors: Factor[] }> = {
  forward: {
    title: 'FLOPs of one forward pass of a 1-billion-parameter model over a 1,000-token prompt',
    unit: 'FLOPs',
    truth: 2e12,
    truthLabel: '2 x 10^9 x 10^3 = 2 x 10^12',
    factors: [
      { name: 'Parameters touched per token', lo: L(5e8), hi: L(2e9) },
      { name: 'FLOPs per parameter per token', lo: L(1), hi: L(4) },
      { name: 'Tokens in the prompt', lo: L(1e3), hi: L(1e3) },
    ],
  },
  train: {
    title: 'GPU-hours to pretrain a 100-million-parameter model on 2 billion tokens',
    unit: 'GPU-hours',
    truth: (6 * 1e8 * 2e9) / 1e14 / 3600,
    truthLabel: '6 x 10^8 x 2 x 10^9 / 10^14 / 3600, about 3.3',
    factors: [
      { name: 'Parameters', lo: L(1e8), hi: L(1e8) },
      { name: 'Training tokens', lo: L(2e9), hi: L(2e9) },
      { name: 'FLOPs per parameter per token, forward and backward', lo: L(3), hi: L(10) },
      { name: 'Sustained FLOP/s of one GPU (divide)', lo: L(3e13), hi: L(3e14), divide: true },
      { name: 'Seconds per hour (divide)', lo: L(3600), hi: L(3600), divide: true },
    ],
  },
};

// Reference quantities, at least 1.8 decades apart so their labels never collide.
export const LADDER: [number, string][] = [
  [1, 'one'],
  [8.64e4, 'seconds in a day'],
  [1.24e8, 'parameters of GPT-2 small'],
  [8e9, 'people on Earth'],
  [2e12, 'tokens used to train Llama 2'],
  [1e15, 'FLOP/s of one H100 GPU, bf16'],
  [8.4e22, 'FLOPs to train 7B parameters on 2T tokens'],
];

const pow10 = (e: number) => {
  const k = Math.floor(e + 1e-9);
  const m = 10 ** (e - k);
  return `${m.toFixed(1)} x 10^${k}`;
};

export default function MagnitudeLadder({ props }: WidgetProps) {
  const preset = PRESETS[props.preset ?? 'forward'] ?? PRESETS.forward;
  const [fs, setFs] = useState<Factor[]>(preset.factors);
  const [showTruth, setShowTruth] = useState(false);
  const { mid, worst, typical } = combine(fs);
  const W = 440;
  const H = 400;
  const top = 18;
  const bot = H - 18;
  const lo = -2;
  const hi = 24;
  const y = (e: number) => bot - ((e - lo) / (hi - lo)) * (bot - top);
  const set = (i: number, key: 'lo' | 'hi', v: number) => setFs((a) => a.map((f, j) => (j === i ? { ...f, [key]: v } : f)));
  const truthE = L(preset.truth);
  return (
    <Frame
      title={preset.title}
      caption={
        <>
          Estimate {pow10(mid)} {preset.unit}. Worst case: within a factor of {(10 ** worst).toFixed(1)} either way. Typical error, if the factors
          are independent: a factor of {(10 ** typical).toFixed(1)}, because errors in a product partly cancel.
          {showTruth && (
            <>
              {' '}
              Computed value: {preset.truthLabel} {preset.unit}; your estimate is off by a factor of {(10 ** Math.abs(mid - truthE)).toFixed(1)}.
            </>
          )}
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Ladder of powers of ten with the estimate and its error bars">
        <line x1={70} x2={70} y1={top} y2={bot} className="axis" />
        {Array.from({ length: (hi - lo) / 2 + 1 }, (_, i) => lo + 2 * i).map((e) => (
          <g key={e}>
            <line x1={64} x2={70} y1={y(e)} y2={y(e)} className="axis" />
            <text x={60} y={y(e) + 4} textAnchor="end">
              1e{e}
            </text>
          </g>
        ))}
        {LADDER.map(([v, label]) => (
          <g key={label}>
            <circle cx={70} cy={y(L(v))} r={3} className="dot-b" />
            <text x={80} y={y(L(v)) + 4}>{label}</text>
          </g>
        ))}
        <rect x={300} y={y(mid + worst)} width={14} height={Math.max(1, y(mid - worst) - y(mid + worst))} className="bar-a" opacity={0.55} />
        <rect x={318} y={y(mid + typical)} width={14} height={Math.max(1, y(mid - typical) - y(mid + typical))} className="bar-c" opacity={0.75} />
        <line x1={292} x2={340} y1={y(mid)} y2={y(mid)} className="main-curve" />
        <text x={346} y={y(mid) + 4}>estimate</text>
        {showTruth && (
          <g>
            <line x1={292} x2={340} y1={y(truthE)} y2={y(truthE)} className="ref-curve" strokeDasharray="4 3" />
            <text x={346} y={y(truthE) + 4}>computed</text>
          </g>
        )}
      </svg>
      <ul className="legend-row">
        <li>Left bar: worst case</li>
        <li>Right bar: typical error</li>
      </ul>
      <div className="widget-controls grid2">
        {fs.map((f, i) => (
          <div key={f.name}>
            <Slider label={`${f.name}: low`} value={f.lo} min={-1} max={16} step={0.05} onChange={(v) => set(i, 'lo', v)} format={pow10} />
            <Slider label={`${f.name}: high`} value={f.hi} min={-1} max={16} step={0.05} onChange={(v) => set(i, 'hi', v)} format={pow10} />
          </div>
        ))}
      </div>
      <div className="widget-controls">
        <Toggle label="Show the computed value" checked={showTruth} onChange={setShowTruth} />
      </div>
    </Frame>
  );
}
