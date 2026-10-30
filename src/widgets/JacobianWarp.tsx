import { useMemo, useState } from 'react';
import { Frame, Select, Slider, num, rng, type WidgetProps, fmt } from './common';

// A map from the plane to the plane, applied to uniform samples (M20). Near a point the
// map acts like its Jacobian J: a small square becomes nearly a parallelogram with area
// |det J| times the square's, so the samples' density there is divided by |det J|.

export type P2 = [number, number];

export const MAPS: Record<string, { label: string; f: (p: P2) => P2; dom: [number, number]; out: number }> = {
  polar: { label: 'Polar: r = u, angle = 2 pi v', f: ([u, v]) => [u * Math.cos(2 * Math.PI * v), u * Math.sin(2 * Math.PI * v)], dom: [0, 1], out: 1.1 },
  disc: { label: 'Uniform disc: r = sqrt(u), angle = 2 pi v', f: ([u, v]) => [Math.sqrt(u) * Math.cos(2 * Math.PI * v), Math.sqrt(u) * Math.sin(2 * Math.PI * v)], dom: [0, 1], out: 1.1 },
  boxmuller: {
    label: 'Box-Muller: r = sqrt(-2 log u), angle = 2 pi v',
    f: ([u, v]) => {
      const r = Math.sqrt(-2 * Math.log(Math.max(u, 1e-12)));
      return [r * Math.cos(2 * Math.PI * v), r * Math.sin(2 * Math.PI * v)];
    },
    dom: [0, 1],
    out: 3.2,
  },
  square: { label: 'Squash: (u squared, v)', f: ([u, v]) => [u * u, v], dom: [0, 1], out: 1.1 },
  tanh: { label: 'A tanh layer: tanh(2x + 0.5y), tanh(1.5y - x)', f: ([x, y]) => [Math.tanh(2 * x + 0.5 * y), Math.tanh(1.5 * y - x)], dom: [-1, 1], out: 1.1 },
};

export function jacobian(f: (p: P2) => P2, [x, y]: P2, h = 1e-6): [number, number, number, number] {
  const fx1 = f([x + h, y]);
  const fx0 = f([x - h, y]);
  const fy1 = f([x, y + h]);
  const fy0 = f([x, y - h]);
  return [(fx1[0] - fx0[0]) / (2 * h), (fy1[0] - fy0[0]) / (2 * h), (fx1[1] - fx0[1]) / (2 * h), (fy1[1] - fy0[1]) / (2 * h)];
}

// Shoelace formula.
export function polygonArea(pts: P2[]) {
  let s = 0;
  for (let i = 0; i < pts.length; i++) {
    const [a, b] = pts[i];
    const [c, d] = pts[(i + 1) % pts.length];
    s += a * d - b * c;
  }
  return Math.abs(s) / 2;
}

export function squareBoundary([u, v]: P2, h: number, per = 16): P2[] {
  const out: P2[] = [];
  const corners: P2[] = [[u, v], [u + h, v], [u + h, v + h], [u, v + h]];
  for (let k = 0; k < 4; k++) {
    const [a, b] = corners[k];
    const [c, d] = corners[(k + 1) % 4];
    for (let i = 0; i < per; i++) out.push([a + ((c - a) * i) / per, b + ((d - b) * i) / per]);
  }
  return out;
}

export default function JacobianWarp({ props }: WidgetProps) {
  const [name, setName] = useState(props.map && MAPS[props.map] ? props.map : 'polar');
  const M = MAPS[name];
  const [lo, hi] = M.dom;
  const [s0, setS0] = useState(num(props, 's', 0.3));
  const [t0, setT0] = useState(num(props, 't', 0.6));
  const [size, setSize] = useState(num(props, 'size', 0.1));
  const pick = (t: number) => lo + (hi - lo) * t;
  const p: P2 = [pick(s0), pick(t0)];
  const h = size * (hi - lo);
  const samples = useMemo(() => {
    const r = rng(5);
    return Array.from({ length: 700 }, () => [lo + (hi - lo) * r(), lo + (hi - lo) * r()] as P2);
  }, [lo, hi]);
  const W = 180;
  const Pin = ([u, v]: P2) => [6 + ((u - lo) / (hi - lo)) * (W - 12), W - 6 - ((v - lo) / (hi - lo)) * (W - 12)] as const;
  const Pout = ([x, y]: P2) => [W + 10 + W / 2 + (x / M.out) * (W / 2 - 6), W / 2 - (y / M.out) * (W / 2 - 6)] as const;
  const J = jacobian(M.f, [p[0] + h / 2, p[1] + h / 2]);
  const det = J[0] * J[3] - J[1] * J[2];
  const boundary = squareBoundary(p, h);
  const image = boundary.map(M.f);
  const ratio = polygonArea(image) / (h * h);
  const c = M.f([p[0] + h / 2, p[1] + h / 2]);
  const lin = [[-h / 2, -h / 2], [h / 2, -h / 2], [h / 2, h / 2], [-h / 2, h / 2]].map(([a, b]) => [c[0] + J[0] * a + J[1] * b, c[1] + J[2] * a + J[3] * b] as P2);
  const grid: P2[][] = [];
  for (let k = 0; k <= 8; k++) {
    const a = lo + ((hi - lo) * k) / 8;
    grid.push(Array.from({ length: 41 }, (_, i) => [a, lo + ((hi - lo) * i) / 40] as P2));
    grid.push(Array.from({ length: 41 }, (_, i) => [lo + ((hi - lo) * i) / 40, a] as P2));
  }
  const pts = (arr: P2[], P: (q: P2) => readonly [number, number]) => arr.map((q) => P(q).join(',')).join(' ');
  return (
    <Frame
      title="How a map moves area, and probability"
      caption={
        <>
          Jacobian at the small square: [[{fmt(J[0])}, {fmt(J[1])}], [{fmt(J[2])}, {fmt(J[3])}]], det J = {fmt(det)}. The image of the square has{' '}
          {fmt(ratio)} times its area, close to |det J| when the square is small. Samples that were spread evenly land {fmt(1 / Math.max(Math.abs(det), 1e-12))} times
          as densely there as in the input square.
        </>
      }
    >
      <svg viewBox={`0 0 ${2 * W + 10} ${W}`} className="widget-svg" role="img" aria-label="Uniform samples in a square, left, and their images under the map, right">
        <rect x={6} y={6} width={W - 12} height={W - 12} className="grid-line" fill="none" />
        {grid.map((g, i) => (
          <polyline key={'gi' + i} points={pts(g, Pin)} className="grid-line" fill="none" />
        ))}
        {grid.map((g, i) => (
          <polyline key={'go' + i} points={pts(g.map(M.f), Pout)} className="grid-line" fill="none" />
        ))}
        {samples.map((q, i) => (
          <circle key={'si' + i} cx={Pin(q)[0]} cy={Pin(q)[1]} r={1.2} className="dot-a" opacity={0.6} />
        ))}
        {samples.map((q, i) => {
          const [x, y] = Pout(M.f(q));
          return <circle key={'so' + i} cx={x} cy={y} r={1.2} className="dot-a" opacity={0.6} />;
        })}
        <polygon points={pts(boundary, Pin)} fill="var(--accent)" fillOpacity={0.25} stroke="var(--accent)" strokeWidth={2} />
        <polygon points={pts(image, Pout)} fill="var(--accent)" fillOpacity={0.25} stroke="var(--accent)" strokeWidth={2} />
        <polygon points={pts(lin, Pout)} fill="none" className="ref-curve" />
      </svg>
      <div className="widget-controls grid2">
        <Slider label="Square position, first coordinate" value={s0} min={0} max={0.9} step={0.01} onChange={setS0} />
        <Slider label="Square position, second coordinate" value={t0} min={0} max={0.9} step={0.01} onChange={setT0} />
        <Slider label="Square size" value={size} min={0.02} max={0.1} step={0.01} onChange={setSize} />
      </div>
      <div className="widget-controls">
        <Select label="Map" value={name} onChange={setName} options={Object.entries(MAPS).map(([value, m]) => ({ value, label: m.label }))} />
      </div>
    </Frame>
  );
}
