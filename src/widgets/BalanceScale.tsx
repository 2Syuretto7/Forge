import { useState } from 'react';
import { Frame, Slider, type WidgetProps, fmt } from './common';

// An equation a x + b = c x + d as a balance: each side is a pan, the beam tilts toward
// the heavier side, and the steps that solve it are "do the same to both pans" (M02).

export type Solution = { kind: 'one'; x: number } | { kind: 'none' } | { kind: 'all' };

export function solveLinear(a: number, b: number, c: number, d: number): Solution {
  if (a !== c) return { kind: 'one', x: (d - b) / (a - c) };
  return b === d ? { kind: 'all' } : { kind: 'none' };
}

const term = (k: number, v: string) => (k === 0 ? '' : k === 1 ? v : k === -1 ? `-${v}` : `${k}${v}`);
export function side(k: number, m: number) {
  const t = term(k, 'x');
  if (!t) return String(m);
  if (m === 0) return t;
  return `${t} ${m < 0 ? '-' : '+'} ${Math.abs(m)}`;
}

export default function BalanceScale({ props }: WidgetProps) {
  const p = (k: string, d: number) => (Number.isFinite(parseFloat(props[k])) ? parseFloat(props[k]) : d);
  const [a, setA] = useState(p('a', 3));
  const [b, setB] = useState(p('b', 2));
  const [c, setC] = useState(p('c', 1));
  const [d, setD] = useState(p('d', 8));
  const [x, setX] = useState(p('x', 0));
  const L = a * x + b;
  const R = c * x + d;
  const sol = solveLinear(a, b, c, d);
  const tilt = Math.max(-0.35, Math.min(0.35, Math.atan((L - R) / 12)));
  const W = 420;
  const H = 210;
  const cx = W / 2;
  const cy = 70;
  const arm = 140;
  const lx = cx - arm * Math.cos(tilt);
  const ly = cy + arm * Math.sin(tilt);
  const rx = cx + arm * Math.cos(tilt);
  const ry = cy - arm * Math.sin(tilt);
  const balanced = Math.abs(L - R) < 1e-9;
  const steps =
    sol.kind === 'one'
      ? [
          `${side(a, b)} = ${side(c, d)}`,
          `subtract ${term(c, 'x') || '0'} from both pans: ${side(a - c, b)} = ${d}`,
          `subtract ${b} from both pans: ${term(a - c, 'x')} = ${d - b}`,
          `divide both pans by ${a - c}: x = ${fmt(sol.x)}`,
        ]
      : [
          `${side(a, b)} = ${side(c, d)}`,
          `subtract ${term(c, 'x') || '0'} from both pans: ${b} = ${d}`,
          sol.kind === 'all'
            ? 'both pans now hold the same number whatever x is: every x is a solution'
            : 'the pans hold different numbers whatever x is: no x balances them, and dividing by a - c = 0 is not allowed',
        ];
  return (
    <Frame
      title="An equation is a balance"
      caption={
        <>
          At x = {fmt(x)}: left pan {fmt(L)}, right pan {fmt(R)}.{' '}
          {balanced ? 'Balanced: this x solves the equation.' : `The ${L > R ? 'left' : 'right'} pan is heavier.`}
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="A balance whose pans hold the two sides of the equation">
        <polygon points={`${cx - 22},${H - 20} ${cx + 22},${H - 20} ${cx},${cy + 6}`} className="bar-d" opacity={0.6} />
        <line x1={lx} y1={ly} x2={rx} y2={ry} className="cap-line" />
        <circle cx={cx} cy={cy} r={5} className="dot-c" />
        {[
          [lx, ly, side(a, b), L],
          [rx, ry, side(c, d), R],
        ].map(([px, py, label, v], i) => (
          <g key={i}>
            <line x1={px as number} y1={py as number} x2={px as number} y2={(py as number) + 40} className="axis" />
            <rect x={(px as number) - 52} y={(py as number) + 40} width={104} height={34} rx={6} className={i ? 'bar-b' : 'bar-a'} opacity={0.25} />
            <text x={px as number} y={(py as number) + 56} textAnchor="middle">
              {label as string}
            </text>
            <text x={px as number} y={(py as number) + 69} textAnchor="middle">
              = {fmt(v as number)}
            </text>
          </g>
        ))}
      </svg>
      <ol className="widget-steps">
        {steps.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ol>
      <div className="widget-controls grid2">
        <Slider label="a (left x coefficient)" value={a} min={-5} max={5} step={1} onChange={setA} format={(v) => String(v)} />
        <Slider label="b (left constant)" value={b} min={-10} max={10} step={1} onChange={setB} format={(v) => String(v)} />
        <Slider label="c (right x coefficient)" value={c} min={-5} max={5} step={1} onChange={setC} format={(v) => String(v)} />
        <Slider label="d (right constant)" value={d} min={-10} max={10} step={1} onChange={setD} format={(v) => String(v)} />
      </div>
      <div className="widget-controls">
        <Slider label="Try a value of x" value={x} min={-10} max={10} step={0.25} onChange={setX} />
      </div>
    </Frame>
  );
}
