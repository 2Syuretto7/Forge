import { useMemo, useState } from 'react';
import { Frame, Select, Slider, num, type WidgetProps, fmt } from './common';

// Contours and gradients of f(x, y) (M18). The gradient at a point is perpendicular to
// the contour through it and points uphill; the slope in direction u is grad f . u,
// largest along the gradient (Cauchy-Schwarz). Where the gradient vanishes, the
// eigenvalues of the Hessian say minimum, maximum or saddle.

export type P2 = [number, number];
type Fn = (p: P2) => number;

export const SURFACES: Record<string, { label: string; f: Fn; box: number }> = {
  bowl: { label: 'Round bowl x^2 + y^2', f: ([x, y]) => x * x + y * y, box: 2 },
  valley: { label: 'Narrow valley x^2 + 8y^2', f: ([x, y]) => x * x + 8 * y * y, box: 2 },
  saddle: { label: 'Saddle x^2 - y^2', f: ([x, y]) => x * x - y * y, box: 2 },
  hidden: { label: 'Hidden saddle x^2 + y^2 - 3xy', f: ([x, y]) => x * x + y * y - 3 * x * y, box: 2 },
  banana: { label: 'Banana (1 - x)^2 + 5(y - x^2)^2', f: ([x, y]) => (1 - x) ** 2 + 5 * (y - x * x) ** 2, box: 2 },
  hills: {
    label: 'Two hills',
    f: ([x, y]) => 2 * Math.exp(-((x - 0.8) ** 2 + (y - 0.5) ** 2)) + 1.2 * Math.exp(-((x + 0.9) ** 2 + (y + 0.7) ** 2) / 0.6),
    box: 2.5,
  },
};

export function numGrad(f: Fn, [x, y]: P2, h = 1e-5): P2 {
  return [(f([x + h, y]) - f([x - h, y])) / (2 * h), (f([x, y + h]) - f([x, y - h])) / (2 * h)];
}

export function hessian(f: Fn, [x, y]: P2, h = 1e-4): [number, number, number] {
  const fxx = (f([x + h, y]) - 2 * f([x, y]) + f([x - h, y])) / (h * h);
  const fyy = (f([x, y + h]) - 2 * f([x, y]) + f([x, y - h])) / (h * h);
  const fxy = (f([x + h, y + h]) - f([x + h, y - h]) - f([x - h, y + h]) + f([x - h, y - h])) / (4 * h * h);
  return [fxx, fxy, fyy];
}

export function eigSym2(a: number, b: number, d: number): [number, number] {
  const m = (a + d) / 2;
  const r = Math.hypot((a - d) / 2, b);
  return [m + r, m - r];
}

// Marching squares: line segments of the level set f = level on an n x n grid.
export function contourSegments(f: Fn, box: number, n: number, level: number): [P2, P2][] {
  const xs = Array.from({ length: n + 1 }, (_, i) => -box + (2 * box * i) / n);
  const v = xs.map((y) => xs.map((x) => f([x, y]) - level));
  const segs: [P2, P2][] = [];
  const cross = (p: P2, q: P2, a: number, b: number): P2 => {
    const t = a / (a - b);
    return [p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])];
  };
  for (let j = 0; j < n; j++)
    for (let i = 0; i < n; i++) {
      const c: P2[] = [[xs[i], xs[j]], [xs[i + 1], xs[j]], [xs[i + 1], xs[j + 1]], [xs[i], xs[j + 1]]];
      const val = [v[j][i], v[j][i + 1], v[j + 1][i + 1], v[j + 1][i]];
      const pts: P2[] = [];
      for (let e = 0; e < 4; e++) {
        const a = val[e];
        const b = val[(e + 1) % 4];
        if ((a < 0) !== (b < 0)) pts.push(cross(c[e], c[(e + 1) % 4], a, b));
      }
      if (pts.length >= 2) segs.push([pts[0], pts[1]]);
      if (pts.length === 4) segs.push([pts[2], pts[3]]);
    }
  return segs;
}

export default function GradientField({ props }: WidgetProps) {
  const [name, setName] = useState(props.f && SURFACES[props.f] ? props.f : 'bowl');
  const [px, setPx] = useState(num(props, 'x', 1));
  const [py, setPy] = useState(num(props, 'y', 0.5));
  const [phi, setPhi] = useState(num(props, 'phi', 45));
  const S = SURFACES[name];
  const B = S.box;
  const W = 340;
  const P = ([x, y]: P2) => [W / 2 + (x / B) * (W / 2 - 10), W / 2 - (y / B) * (W / 2 - 10)] as const;
  const levels = useMemo(() => {
    const vals: number[] = [];
    for (let i = 0; i <= 30; i++) for (let j = 0; j <= 30; j++) vals.push(S.f([-B + (2 * B * i) / 30, -B + (2 * B * j) / 30]));
    vals.sort((a, b) => a - b);
    return Array.from({ length: 9 }, (_, k) => vals[Math.floor(((k + 0.5) / 9) * 0.9 * vals.length)]);
  }, [S, B]);
  const contours = useMemo(() => levels.map((l) => contourSegments(S.f, B, 48, l)), [S, B, levels]);
  const p: P2 = [px, py];
  const g = numGrad(S.f, p);
  const gn = Math.hypot(...g);
  const u: P2 = [Math.cos((phi * Math.PI) / 180), Math.sin((phi * Math.PI) / 180)];
  const dd = g[0] * u[0] + g[1] * u[1];
  const [hxx, hxy, hyy] = hessian(S.f, p);
  const [l1, l2] = eigSym2(hxx, hxy, hyy);
  const arrows: { a: P2; b: P2 }[] = [];
  for (let i = -3; i <= 3; i++)
    for (let j = -3; j <= 3; j++) {
      const q: P2 = [(i * B) / 3.5, (j * B) / 3.5];
      const gq = numGrad(S.f, q);
      const n = Math.hypot(...gq);
      if (n < 1e-9) continue;
      const L = (0.22 * B * Math.min(1, n)) / n;
      arrows.push({ a: q, b: [q[0] + L * gq[0], q[1] + L * gq[1]] });
    }
  const scaleG = gn > 0 ? (0.6 * B) / Math.max(gn, 1) : 0;
  const kind =
    gn > 1e-3 ? 'not a critical point' : l1 > 1e-6 && l2 > 1e-6 ? 'a minimum' : l1 < -1e-6 && l2 < -1e-6 ? 'a maximum' : l1 * l2 < 0 ? 'a saddle' : 'degenerate';
  return (
    <Frame
      title="Gradients and contour lines"
      caption={
        <>
          At ({fmt(px, 2)}, {fmt(py, 2)}): f = {fmt(S.f(p))}, gradient ({fmt(g[0])}, {fmt(g[1])}) of length {fmt(gn)}. Slope in your direction: grad f . u ={' '}
          {fmt(dd)}, at most {fmt(gn)} (Cauchy-Schwarz), reached when u points along the gradient. Hessian eigenvalues {fmt(l1)} and {fmt(l2)}: this point is{' '}
          {kind}.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${W}`} className="widget-svg" role="img" aria-label="Contour lines with gradient arrows and a chosen point and direction">
        <defs>
          <marker id="gf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" className="arrowhead" />
          </marker>
        </defs>
        {contours.map((segs, k) => (
          <g key={k}>
            {segs.map(([a, b], i) => (
              <line key={i} x1={P(a)[0]} y1={P(a)[1]} x2={P(b)[0]} y2={P(b)[1]} className="iso-curve" />
            ))}
          </g>
        ))}
        {arrows.map(({ a, b }, i) => (
          <line key={i} x1={P(a)[0]} y1={P(a)[1]} x2={P(b)[0]} y2={P(b)[1]} className="svd-v" markerEnd="url(#gf-arrow)" />
        ))}
        <line x1={P(p)[0]} y1={P(p)[1]} x2={P([px + scaleG * g[0], py + scaleG * g[1]])[0]} y2={P([px + scaleG * g[0], py + scaleG * g[1]])[1]} className="main-curve" markerEnd="url(#gf-arrow)" />
        <line x1={P(p)[0]} y1={P(p)[1]} x2={P([px + 0.45 * B * u[0], py + 0.45 * B * u[1]])[0]} y2={P([px + 0.45 * B * u[0], py + 0.45 * B * u[1]])[1]} className="basis-2" markerEnd="url(#gf-arrow)" />
        <circle cx={P(p)[0]} cy={P(p)[1]} r={4} className="dot-c" />
      </svg>
      <div className="widget-controls grid2">
        <Slider label="x" value={px} min={-B} max={B} step={0.05} onChange={setPx} />
        <Slider label="y" value={py} min={-B} max={B} step={0.05} onChange={setPy} />
        <Slider label="Direction u (degrees)" value={phi} min={-180} max={180} step={1} onChange={setPhi} format={(v) => String(v)} />
      </div>
      <div className="widget-controls">
        <Select label="Function" value={name} onChange={setName} options={Object.entries(SURFACES).map(([value, s]) => ({ value, label: s.label }))} />
      </div>
    </Frame>
  );
}
