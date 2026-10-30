import { useMemo, useState } from 'react';
import { Frame, Select, Slider, num, type WidgetProps, fmt } from './common';

// Power iteration on a 2x2 matrix (M13, M23). Apply A again and again to a vector and
// rescale: the direction settles on the eigenvector of the largest |eigenvalue|, and
// the angle to it shrinks by |lambda2 / lambda1| per step. Rotations have no real
// eigenvector, a shear has only one, and equal magnitudes never settle.

export type V = [number, number];

export interface Eig2 {
  real: boolean;
  l1: number;
  l2: number;
  v1: V | null;
  v2: V | null;
  im: number;
  defective: boolean;
}

const unit = (v: V): V => {
  const n = Math.hypot(v[0], v[1]);
  return [v[0] / n, v[1] / n];
};

export function eig2(a: number, b: number, c: number, d: number): Eig2 {
  const tr = a + d;
  const det = a * d - b * c;
  const disc = (tr * tr) / 4 - det;
  if (disc < -1e-12) return { real: false, l1: tr / 2, l2: tr / 2, v1: null, v2: null, im: Math.sqrt(-disc), defective: false };
  const s = Math.sqrt(Math.max(0, disc));
  let [l1, l2] = [tr / 2 + s, tr / 2 - s];
  if (Math.abs(l2) > Math.abs(l1)) [l1, l2] = [l2, l1];
  const vec = (l: number): V => {
    if (Math.abs(b) > 1e-12) return unit([b, l - a]);
    if (Math.abs(c) > 1e-12) return unit([l - d, c]);
    return Math.abs(l - a) <= Math.abs(l - d) ? [1, 0] : [0, 1];
  };
  const v1 = vec(l1);
  let v2 = vec(l2);
  const defective = s < 1e-9 && (Math.abs(b) > 1e-12 || Math.abs(c) > 1e-12);
  if (s < 1e-9 && !defective) v2 = [-v1[1], v1[0]];
  return { real: true, l1, l2, v1, v2: defective ? null : v2, im: 0, defective };
}

export function powerIterate(A: [number, number, number, number], v0: V, steps: number): V[] {
  const [a, b, c, d] = A;
  const out: V[] = [unit(v0)];
  for (let k = 0; k < steps; k++) {
    const [x, y] = out[out.length - 1];
    out.push(unit([a * x + b * y, c * x + d * y]));
  }
  return out;
}

export const PRESETS: Record<string, { label: string; m: [number, number, number, number] }> = {
  sym: { label: 'Symmetric, eigenvalues 3 and 1', m: [2, 1, 1, 2] },
  close: { label: 'Symmetric, eigenvalues 1.1 and 1', m: [1.05, 0.05, 0.05, 1.05] },
  markov: { label: 'Markov chain (columns sum to 1)', m: [0.9, 0.5, 0.1, 0.5] },
  shear: { label: 'Shear (one eigenvector)', m: [1, 1, 0, 1] },
  rotation: { label: 'Rotation by 30 degrees', m: [Math.cos(Math.PI / 6), -Math.sin(Math.PI / 6), Math.sin(Math.PI / 6), Math.cos(Math.PI / 6)] },
  flip: { label: 'Eigenvalues 1 and -1', m: [1, 0, 0, -1] },
};

export default function EigenFlow({ props }: WidgetProps) {
  const [preset, setPreset] = useState(props.preset && PRESETS[props.preset] ? props.preset : 'sym');
  const [start, setStart] = useState(num(props, 'start', 100));
  const [steps, setSteps] = useState(num(props, 'steps', 8));
  const m = PRESETS[preset].m;
  const e = useMemo(() => eig2(...m), [m]);
  const it = useMemo(() => powerIterate(m, [Math.cos((start * Math.PI) / 180), Math.sin((start * Math.PI) / 180)], steps), [m, start, steps]);
  const W = 340;
  const S = 120;
  const P = (p: V) => [W / 2 + p[0] * S, W / 2 - p[1] * S] as const;
  const last = it[it.length - 1];
  const angleTo = (v: V | null) => (v ? (Math.acos(Math.min(1, Math.abs(last[0] * v[0] + last[1] * v[1]))) * 180) / Math.PI : NaN);
  const line = (v: V, key: string) => <line key={key} x1={P([-1.4 * v[0], -1.4 * v[1]])[0]} y1={P([-1.4 * v[0], -1.4 * v[1]])[1]} x2={P([1.4 * v[0], 1.4 * v[1]])[0]} y2={P([1.4 * v[0], 1.4 * v[1]])[1]} className="ref-curve" />;
  const circle = Array.from({ length: 97 }, (_, i) => P([Math.cos((i / 96) * 2 * Math.PI), Math.sin((i / 96) * 2 * Math.PI)]).join(',')).join(' ');
  let caption: string;
  if (!e.real) caption = `Complex eigenvalues ${fmt(e.l1)} plus or minus ${fmt(e.im)}i: no real direction is kept, so the iterates go round for ever.`;
  else if (e.defective) caption = `Eigenvalue ${fmt(e.l1)} twice, with only one eigenvector: the iterates creep towards it, with an angle that shrinks like 1/k rather than geometrically. Angle now ${fmt(angleTo(e.v1), 2)} degrees.`;
  else if (Math.abs(Math.abs(e.l1) - Math.abs(e.l2)) < 1e-9) caption = `Eigenvalues ${fmt(e.l1)} and ${fmt(e.l2)} have equal magnitude: neither wins, and the direction never settles.`;
  else
    caption = `Eigenvalues ${fmt(e.l1)} and ${fmt(e.l2)}; ratio |lambda2 / lambda1| = ${fmt(Math.abs(e.l2 / e.l1))}. After ${steps} steps the angle to the dominant eigenvector is ${fmt(angleTo(e.v1), 3)} degrees; each step multiplies its tangent by the ratio.`;
  return (
    <Frame title="Power iteration and eigenvectors" caption={caption}>
      <svg viewBox={`0 0 ${W} ${W}`} className="widget-svg" role="img" aria-label="Successive directions of A to the k times v on the unit circle, with the eigenvector lines">
        <defs>
          <marker id="ef-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" className="arrowhead" />
          </marker>
        </defs>
        <polyline points={circle} className="grid-line" fill="none" />
        {e.v1 && line(e.v1, 'e1')}
        {e.v2 && line(e.v2, 'e2')}
        {it.map((v, i) => (
          <circle key={i} cx={P(v)[0]} cy={P(v)[1]} r={i === it.length - 1 ? 5 : 3} className={i === it.length - 1 ? 'dot-c' : 'dot-a'} opacity={0.35 + (0.65 * i) / it.length} />
        ))}
        <line x1={W / 2} y1={W / 2} x2={P(it[0])[0]} y2={P(it[0])[1]} className="basis-2" markerEnd="url(#ef-arrow)" />
        <line x1={W / 2} y1={W / 2} x2={P(last)[0]} y2={P(last)[1]} className="main-curve" markerEnd="url(#ef-arrow)" />
      </svg>
      <div className="widget-controls grid2">
        <Slider label="Starting direction (degrees)" value={start} min={0} max={180} step={1} onChange={setStart} format={(v) => String(v)} />
        <Slider label="Steps k" value={steps} min={0} max={50} step={1} onChange={setSteps} format={(v) => String(v)} />
      </div>
      <div className="widget-controls">
        <Select label="Matrix" value={preset} onChange={setPreset} options={Object.entries(PRESETS).map(([value, p]) => ({ value, label: p.label }))} />
      </div>
    </Frame>
  );
}
