import { useState } from 'react';
import { Frame, Select, Slider, num, type WidgetProps, fmt } from './common';

// KKT conditions in two dimensions (M30). Minimize f(x) = (1/2)(x - c)^T A (x - c) subject
// to one constraint g(x) <= 0: a half-plane a^T x <= b or a disc |x|^2 <= r^2. At the
// constrained minimum the gradient of f is a nonnegative multiple of minus the gradient of
// g (stationarity), and the multiplier is zero unless the constraint is active
// (complementary slackness).

export type V2 = [number, number];
export type M2 = [number, number, number]; // symmetric [a11, a12, a22]

export const A: M2 = [2, 0.6, 1];

const mul = (m: M2, v: V2): V2 => [m[0] * v[0] + m[1] * v[1], m[1] * v[0] + m[2] * v[1]];
const inv = (m: M2): M2 => {
  const d = m[0] * m[2] - m[1] * m[1];
  return [m[2] / d, -m[1] / d, m[0] / d];
};
const dot = (u: V2, v: V2) => u[0] * v[0] + u[1] * v[1];

export function fval(c: V2, x: V2) {
  const d: V2 = [x[0] - c[0], x[1] - c[1]];
  return 0.5 * dot(d, mul(A, d));
}

export function gradF(c: V2, x: V2): V2 {
  return mul(A, [x[0] - c[0], x[1] - c[1]]);
}

// Half-plane a^T x <= b: inactive if the free minimum c is feasible, else project in the A-metric.
export function solveHalfPlane(c: V2, a: V2, b: number) {
  const slack = dot(a, c) - b;
  if (slack <= 0) return { x: c, lambda: 0, active: false };
  const Ainv_a = mul(inv(A), a);
  const lambda = slack / dot(a, Ainv_a);
  return { x: [c[0] - lambda * Ainv_a[0], c[1] - lambda * Ainv_a[1]] as V2, lambda, active: true };
}

// Disc |x|^2 <= r^2, g(x) = |x|^2 - r^2, grad g = 2x: x(lambda) = (A + 2 lambda I)^{-1} A c,
// whose norm decreases in lambda; bisect for |x| = r when c is outside the disc.
export function solveDisc(c: V2, r: number) {
  if (dot(c, c) <= r * r) return { x: c, lambda: 0, active: false };
  const at = (lam: number): V2 => mul(inv([A[0] + 2 * lam, A[1], A[2] + 2 * lam]), mul(A, c));
  let lo = 0;
  let hi = 1;
  while (Math.hypot(...at(hi)) > r) hi *= 2;
  for (let i = 0; i < 100; i++) {
    const mid = (lo + hi) / 2;
    if (Math.hypot(...at(mid)) > r) lo = mid;
    else hi = mid;
  }
  const lambda = (lo + hi) / 2;
  return { x: at(lambda), lambda, active: true };
}

// Largest violation among stationarity, primal feasibility, dual feasibility and
// complementary slackness, for g with gradient gradG.
export function kktResidual(c: V2, x: V2, lambda: number, g: number, gradG: V2) {
  const gf = gradF(c, x);
  const stat = Math.hypot(gf[0] + lambda * gradG[0], gf[1] + lambda * gradG[1]);
  return Math.max(stat, Math.max(0, g), Math.max(0, -lambda), Math.abs(lambda * g));
}

type Kind = 'halfplane' | 'disc';

export default function KKTGeometry({ props }: WidgetProps) {
  const [kind, setKind] = useState<Kind>(props.constraint === 'disc' ? 'disc' : 'halfplane');
  const [cx, setCx] = useState(num(props, 'cx', 1.6));
  const [cy, setCy] = useState(num(props, 'cy', 1.2));
  const [level, setLevel] = useState(num(props, 'level', 1));
  const c: V2 = [cx, cy];
  const a: V2 = [0.8, 0.6];
  const sol = kind === 'halfplane' ? solveHalfPlane(c, a, level) : solveDisc(c, level);
  const g = kind === 'halfplane' ? dot(a, sol.x) - level : dot(sol.x, sol.x) - level * level;
  const gradG: V2 = kind === 'halfplane' ? a : [2 * sol.x[0], 2 * sol.x[1]];
  const res = kktResidual(c, sol.x, sol.lambda, g, gradG);
  const W = 340;
  const B = 3;
  const P = ([x, y]: V2) => [W / 2 + (x / B) * (W / 2), W / 2 - (y / B) * (W / 2)] as const;
  const fx = fval(c, sol.x);
  // Level sets of f through the optimum and at two larger values, as ellipses around c.
  const ellipse = (val: number) => {
    const pts: string[] = [];
    for (let i = 0; i <= 96; i++) {
      const t = (i / 96) * 2 * Math.PI;
      const u: V2 = [Math.cos(t), Math.sin(t)];
      const s = Math.sqrt((2 * val) / Math.max(dot(u, mul(A, u)), 1e-12));
      pts.push(P([c[0] + s * u[0], c[1] + s * u[1]]).join(','));
    }
    return pts.join(' ');
  };
  const gf = gradF(c, sol.x);
  const arrow = (v: V2, scale: number, cls: string, key: string, dashed = false) => {
    const [x0, y0] = P(sol.x);
    const [x1, y1] = P([sol.x[0] + scale * v[0], sol.x[1] + scale * v[1]]);
    return <line key={key} x1={x0} y1={y0} x2={x1} y2={y1} className={cls} strokeDasharray={dashed ? '5 4' : undefined} markerEnd="url(#kkt-arrow)" />;
  };
  // Half-plane boundary a^T x = level, drawn across the box.
  const boundary = () => {
    const d: V2 = [-a[1], a[0]];
    const p0: V2 = [a[0] * level, a[1] * level];
    const [x1, y1] = P([p0[0] - 5 * d[0], p0[1] - 5 * d[1]]);
    const [x2, y2] = P([p0[0] + 5 * d[0], p0[1] + 5 * d[1]]);
    return <line x1={x1} y1={y1} x2={x2} y2={y2} className="ref-curve" />;
  };
  return (
    <Frame
      title="Stationarity and complementary slackness"
      caption={
        <>
          Free minimum at ({fmt(cx, 2)}, {fmt(cy, 2)}); constrained minimum at ({fmt(sol.x[0], 3)}, {fmt(sol.x[1], 3)}) with f = {fmt(fx, 3)}. The constraint is{' '}
          {sol.active ? 'active' : 'inactive'} and the multiplier is {fmt(sol.lambda, 3)}
          {sol.active ? ': the gradient of f (solid) and the multiplier times the constraint gradient (dashed) are equal and opposite' : ', as complementary slackness requires'}. KKT
          residual {res.toExponential(1)}.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${W}`} className="widget-svg" role="img" aria-label="Level sets of a quadratic, a constraint region, and the gradients at the constrained minimum">
        <defs>
          <marker id="kkt-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" className="arrowhead" />
          </marker>
        </defs>
        <line x1={0} x2={W} y1={W / 2} y2={W / 2} className="grid-line" />
        <line x1={W / 2} x2={W / 2} y1={0} y2={W} className="grid-line" />
        {kind === 'disc' ? <circle cx={W / 2} cy={W / 2} r={(level / B) * (W / 2)} className="ref-curve" /> : boundary()}
        {[fx, fx + 0.5, fx + 1.5].filter((v) => v > 1e-9).map((v, i) => (
          <polyline key={i} points={ellipse(v)} className="iso-curve" />
        ))}
        {arrow(gf, 0.6, 'main-curve', 'f')}
        {sol.active && arrow(gradG, sol.lambda * 0.6, 'series-b', 'g', true)}
        <circle cx={P(c)[0]} cy={P(c)[1]} r={3} className="dot-a" />
        <circle cx={P(sol.x)[0]} cy={P(sol.x)[1]} r={4.5} className="dot-c" />
      </svg>
      <div className="widget-controls grid2">
        <Slider label="Free minimum, x" value={cx} min={-2.5} max={2.5} step={0.05} onChange={setCx} />
        <Slider label="Free minimum, y" value={cy} min={-2.5} max={2.5} step={0.05} onChange={setCy} />
        <Slider label={kind === 'disc' ? 'Disc radius r' : 'Constraint level b'} value={level} min={kind === 'disc' ? 0.3 : -1.5} max={2} step={0.05} onChange={setLevel} />
      </div>
      <div className="widget-controls">
        <Select<Kind>
          label="Constraint"
          value={kind}
          onChange={setKind}
          options={[
            { value: 'halfplane', label: 'Half-plane 0.8 x + 0.6 y <= b' },
            { value: 'disc', label: 'Disc x^2 + y^2 <= r^2' },
          ]}
        />
      </div>
    </Frame>
  );
}
