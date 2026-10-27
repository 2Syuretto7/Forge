import { useMemo, useState } from 'react';
import { Frame, Slider, Toggle, num, type WidgetProps, fmt } from './common';

// 2x2 SVD by eigen-decomposition of A^T A (closed form for 2x2 symmetric).
export function svd2(a: number, b: number, c: number, d: number) {
  const p = a * a + c * c;
  const q = a * b + c * d;
  const r = b * b + d * d;
  const tr = p + r;
  const disc = Math.sqrt(Math.max(0, ((p - r) * (p - r)) / 4 + q * q));
  const l1 = tr / 2 + disc;
  const l2 = Math.max(0, tr / 2 - disc);
  let v1: [number, number];
  if (Math.abs(q) > 1e-12) v1 = [l1 - r, q];
  else v1 = p >= r ? [1, 0] : [0, 1];
  const n1 = Math.hypot(...v1);
  v1 = [v1[0] / n1, v1[1] / n1];
  const v2: [number, number] = [-v1[1], v1[0]];
  const s1 = Math.sqrt(l1);
  const s2 = Math.sqrt(l2);
  const u1: [number, number] = s1 > 1e-12 ? [(a * v1[0] + b * v1[1]) / s1, (c * v1[0] + d * v1[1]) / s1] : [1, 0];
  const u2: [number, number] = s2 > 1e-12 ? [(a * v2[0] + b * v2[1]) / s2, (c * v2[0] + d * v2[1]) / s2] : [-u1[1], u1[0]];
  return { s1, s2, v1, v2, u1, u2 };
}

export default function MatrixTransform({ props }: WidgetProps) {
  const [a, setA] = useState(num(props, 'a', 1.5));
  const [b, setB] = useState(num(props, 'b', 0.5));
  const [c, setC] = useState(num(props, 'c', 0.3));
  const [d, setD] = useState(num(props, 'd', 1));
  const [showSvd, setShowSvd] = useState(props.svd !== 'false');
  const [showGrid, setShowGrid] = useState(true);
  const S = 60;
  const W = 340;
  const tx = (x: number, y: number): [number, number] => [a * x + b * y, c * x + d * y];
  const P = (x: number, y: number) => `${W / 2 + x * S},${W / 2 - y * S}`;
  const { s1, s2, v1, v2, u1, u2 } = useMemo(() => svd2(a, b, c, d), [a, b, c, d]);
  const det = a * d - b * c;
  const cond = s2 > 1e-12 ? s1 / s2 : Infinity;

  const gridLines: string[] = [];
  for (let k = -3; k <= 3; k++) {
    const h: string[] = [];
    const v: string[] = [];
    for (let t = -3; t <= 3; t += 0.25) {
      h.push(P(...tx(t, k)));
      v.push(P(...tx(k, t)));
    }
    gridLines.push(h.join(' '), v.join(' '));
  }
  const circle: string[] = [];
  const ellipse: string[] = [];
  for (let i = 0; i <= 96; i++) {
    const th = (i / 96) * 2 * Math.PI;
    circle.push(P(Math.cos(th), Math.sin(th)));
    ellipse.push(P(...tx(Math.cos(th), Math.sin(th))));
  }
  const arrow = (x: number, y: number, cls: string, key: string) => (
    <line key={key} x1={W / 2} y1={W / 2} x2={W / 2 + x * S} y2={W / 2 - y * S} className={cls} markerEnd="url(#mt-arrow)" />
  );

  return (
    <Frame
      title="Linear map acting on the plane"
      caption={
        <>
          det = {fmt(det)}; singular values {fmt(s1)}, {fmt(s2)}; condition number {Number.isFinite(cond) ? fmt(cond) : 'infinite'}. The unit circle
          maps to an ellipse whose semi-axes are the singular values along the left singular vectors.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${W}`} className="widget-svg" role="img" aria-label="Grid and unit circle before and after the linear map">
        <defs>
          <marker id="mt-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" className="arrowhead" />
          </marker>
        </defs>
        {showGrid && gridLines.map((pts, i) => <polyline key={i} points={pts} className="grid-line" fill="none" />)}
        <polyline points={circle.join(' ')} className="ref-curve" fill="none" />
        <polyline points={ellipse.join(' ')} className="main-curve" fill="none" />
        {arrow(...tx(1, 0), 'basis-1', 'e1')}
        {arrow(...tx(0, 1), 'basis-2', 'e2')}
        {showSvd && (
          <>
            {arrow(v1[0], v1[1], 'svd-v', 'v1')}
            {arrow(v2[0], v2[1], 'svd-v', 'v2')}
            {arrow(s1 * u1[0], s1 * u1[1], 'svd-u', 'u1')}
            {arrow(s2 * u2[0], s2 * u2[1], 'svd-u', 'u2')}
          </>
        )}
      </svg>
      <div className="widget-controls grid2">
        <Slider label="a (row 1, col 1)" value={a} min={-2} max={2} step={0.05} onChange={setA} />
        <Slider label="b (row 1, col 2)" value={b} min={-2} max={2} step={0.05} onChange={setB} />
        <Slider label="c (row 2, col 1)" value={c} min={-2} max={2} step={0.05} onChange={setC} />
        <Slider label="d (row 2, col 2)" value={d} min={-2} max={2} step={0.05} onChange={setD} />
      </div>
      <div className="widget-controls">
        <Toggle label="Show SVD axes (v dashed, sigma times u solid)" checked={showSvd} onChange={setShowSvd} />
        <Toggle label="Show transformed grid" checked={showGrid} onChange={setShowGrid} />
      </div>
    </Frame>
  );
}
