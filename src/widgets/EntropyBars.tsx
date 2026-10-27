import { useState } from 'react';
import { Frame, Slider, Toggle, type WidgetProps, fmt } from './common';

function parse(s: string | undefined, k: number, dflt: number[]) {
  const v = (s ?? '').split(',').map(Number).filter((x) => Number.isFinite(x) && x > 0);
  return v.length === k ? v : dflt;
}
const normalize = (v: number[]) => {
  const s = v.reduce((a, b) => a + b, 0);
  return v.map((x) => x / s);
};

export function entropy(p: number[], base = Math.E) {
  return -p.reduce((a, x) => a + (x > 0 ? x * Math.log(x) : 0), 0) / Math.log(base);
}
export function crossEntropy(p: number[], q: number[], base = Math.E) {
  return -p.reduce((a, x, i) => a + (x > 0 ? x * Math.log(q[i]) : 0), 0) / Math.log(base);
}

export default function EntropyBars({ props }: WidgetProps) {
  const k = Math.max(2, Math.min(6, Math.round(Number(props.k ?? 4))));
  const [pw, setPw] = useState(() => parse(props.p, k, Array.from({ length: k }, (_, i) => k - i)));
  const [qw, setQw] = useState(() => parse(props.q, k, Array(k).fill(1)));
  const [bits, setBits] = useState(props.units === 'bits');
  const p = normalize(pw);
  const q = normalize(qw);
  const base = bits ? 2 : Math.E;
  const u = bits ? 'bits' : 'nats';
  const H = entropy(p, base);
  const CE = crossEntropy(p, q, base);
  const W = 420;
  const Hh = 170;
  const bw = (W - 40) / k;
  return (
    <Frame
      title="Entropy, cross-entropy and KL divergence"
      caption={
        <>
          H(p) = {fmt(H)} {u}; H(q) = {fmt(entropy(q, base))} {u}; cross-entropy H(p, q) = {fmt(CE)} {u}; KL(p || q) = H(p, q) - H(p) ={' '}
          {fmt(CE - H)} {u}; KL(q || p) = {fmt(crossEntropy(q, p, base) - entropy(q, base))} {u}. KL is zero only when the bars match, and the two
          directions differ.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${Hh}`} className="widget-svg" role="img" aria-label="Bar chart of distributions p and q">
        <line x1={20} x2={W - 20} y1={Hh - 20} y2={Hh - 20} className="axis" />
        {p.map((v, i) => (
          <g key={i}>
            <rect x={20 + i * bw + 4} y={Hh - 20 - v * (Hh - 40)} width={bw / 2 - 6} height={v * (Hh - 40)} className="bar-a" />
            <rect x={20 + i * bw + bw / 2} y={Hh - 20 - q[i] * (Hh - 40)} width={bw / 2 - 6} height={q[i] * (Hh - 40)} className="bar-b" />
            <text x={20 + i * bw + bw / 2} y={Hh - 6} textAnchor="middle">
              {i + 1}
            </text>
          </g>
        ))}
      </svg>
      <ul className="legend-row">
        <li>
          <svg width="12" height="12" aria-hidden="true" className="widget-svg legend-swatch">
            <rect width="12" height="12" className="bar-a" />
          </svg>
          p (data)
        </li>
        <li>
          <svg width="12" height="12" aria-hidden="true" className="widget-svg legend-swatch">
            <rect width="12" height="12" className="bar-b" />
          </svg>
          q (model)
        </li>
      </ul>
      <div className="widget-controls grid2">
        {pw.map((v, i) => (
          <Slider key={'p' + i} label={`p weight ${i + 1}`} value={v} min={0.01} max={10} step={0.01} onChange={(x) => setPw((a) => a.map((y, j) => (j === i ? x : y)))} />
        ))}
        {qw.map((v, i) => (
          <Slider key={'q' + i} label={`q weight ${i + 1}`} value={v} min={0.01} max={10} step={0.01} onChange={(x) => setQw((a) => a.map((y, j) => (j === i ? x : y)))} />
        ))}
      </div>
      <div className="widget-controls">
        <Toggle label="Measure in bits (log base 2) instead of nats" checked={bits} onChange={setBits} />
      </div>
    </Frame>
  );
}
