import { useMemo, useState } from 'react';
import { Frame, Slider, Toggle, gauss, num, rng, type WidgetProps, fmt } from './common';

// A two-dimensional Gaussian (M23): samples, the ellipses of equal density at 1, 2 and
// 3 standard deviations (their axes are the eigenvectors of the covariance, with
// half-lengths k times the square roots of the eigenvalues), and the conditional
// distribution of y given x: mean on the regression line, spread sigma_y sqrt(1 - rho^2).

export type Cov = [number, number, number]; // [sxx, sxy, syy]

export function eigSym(c: Cov) {
  const [a, b, d] = c;
  const m = (a + d) / 2;
  const r = Math.hypot((a - d) / 2, b);
  const l1 = m + r;
  const l2 = m - r;
  const angle = Math.abs(b) < 1e-15 ? (a >= d ? 0 : Math.PI / 2) : Math.atan2(l1 - a, b);
  return { l1, l2, angle };
}

export function ellipse(c: Cov, k: number, n = 96): [number, number][] {
  const { l1, l2, angle } = eigSym(c);
  const ca = Math.cos(angle);
  const sa = Math.sin(angle);
  return Array.from({ length: n + 1 }, (_, i) => {
    const t = (i / n) * 2 * Math.PI;
    const u = k * Math.sqrt(Math.max(l1, 0)) * Math.cos(t);
    const v = k * Math.sqrt(Math.max(l2, 0)) * Math.sin(t);
    return [ca * u - sa * v, sa * u + ca * v];
  });
}

export function conditional(sx: number, sy: number, rho: number, x0: number) {
  return { mean: (rho * sy * x0) / sx, sd: sy * Math.sqrt(1 - rho * rho) };
}

export default function GaussianEllipse({ props }: WidgetProps) {
  const [sx, setSx] = useState(num(props, 'sx', 1.5));
  const [sy, setSy] = useState(num(props, 'sy', 1));
  const [rho, setRho] = useState(num(props, 'rho', 0.7));
  const [x0, setX0] = useState(num(props, 'x0', 1.5));
  const [showCond, setShowCond] = useState(props.cond !== 'false');
  const c: Cov = [sx * sx, rho * sx * sy, sy * sy];
  const pts = useMemo(() => {
    const r = rng(17);
    return Array.from({ length: 500 }, () => {
      const z1 = gauss(r);
      const z2 = gauss(r);
      return [sx * z1, sy * (rho * z1 + Math.sqrt(1 - rho * rho) * z2)] as [number, number];
    });
  }, [sx, sy, rho]);
  const W = 340;
  const B = 4.5;
  const P = ([x, y]: [number, number]) => [W / 2 + (x / B) * (W / 2), W / 2 - (y / B) * (W / 2)] as const;
  const cond = conditional(sx, sy, rho, x0);
  const { l1, l2 } = eigSym(c);
  return (
    <Frame
      title="The two-dimensional Gaussian"
      caption={
        <>
          Covariance [[{fmt(c[0], 2)}, {fmt(c[1], 2)}], [{fmt(c[1], 2)}, {fmt(c[2], 2)}]], eigenvalues {fmt(l1, 2)} and {fmt(l2, 2)}: the ellipses' half-axes
          are 1, 2 and 3 times their square roots. Given x = {fmt(x0, 2)}, y has mean {fmt(cond.mean, 2)} and standard deviation {fmt(cond.sd, 2)}, down
          from {fmt(sy, 2)} without the information.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${W}`} className="widget-svg" role="img" aria-label="Samples of a 2D Gaussian with its density ellipses and a conditional slice">
        <line x1={0} x2={W} y1={W / 2} y2={W / 2} className="grid-line" />
        <line x1={W / 2} x2={W / 2} y1={0} y2={W} className="grid-line" />
        {pts.map((p, i) => (
          <circle key={i} cx={P(p)[0]} cy={P(p)[1]} r={1.6} className="dot-a" opacity={0.45} />
        ))}
        {[1, 2, 3].map((k) => (
          <polyline key={k} points={ellipse(c, k).map((q) => P(q).join(',')).join(' ')} className="iso-curve" />
        ))}
        {showCond && (
          <>
            <line x1={P([-B, (-B * rho * sy) / sx])[0]} y1={P([-B, (-B * rho * sy) / sx])[1]} x2={P([B, (B * rho * sy) / sx])[0]} y2={P([B, (B * rho * sy) / sx])[1]} className="ref-curve" />
            <line x1={P([x0, cond.mean - 2 * cond.sd])[0]} y1={P([x0, cond.mean - 2 * cond.sd])[1]} x2={P([x0, cond.mean + 2 * cond.sd])[0]} y2={P([x0, cond.mean + 2 * cond.sd])[1]} className="main-curve" />
            <circle cx={P([x0, cond.mean])[0]} cy={P([x0, cond.mean])[1]} r={4} className="dot-c" />
          </>
        )}
      </svg>
      <div className="widget-controls grid2">
        <Slider label="Standard deviation of x" value={sx} min={0.3} max={2} step={0.05} onChange={setSx} />
        <Slider label="Standard deviation of y" value={sy} min={0.3} max={2} step={0.05} onChange={setSy} />
        <Slider label="Correlation rho" value={rho} min={-0.95} max={0.95} step={0.05} onChange={setRho} />
        <Slider label="Observed x" value={x0} min={-3} max={3} step={0.1} onChange={setX0} />
      </div>
      <div className="widget-controls">
        <Toggle label="Show the regression line and the conditional range (mean plus or minus 2 sd)" checked={showCond} onChange={setShowCond} />
      </div>
    </Frame>
  );
}
