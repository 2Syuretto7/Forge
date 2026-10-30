import { useState } from 'react';
import { Frame, Select, Slider, Toggle, num, type WidgetProps, fmt } from './common';

// Two arrows in the plane (M09, M12): their sum, the dot product computed from
// coordinates and from lengths and the angle, the projection of y onto x, and the
// unit balls of the L1, L2 and L-infinity norms.

export type V = [number, number];
export const dot = (x: V, y: V) => x[0] * y[0] + x[1] * y[1];
export const len = (x: V) => Math.hypot(x[0], x[1]);
// atan2 of the cross and dot products: unlike arccos of the cosine, it stays accurate
// for nearly parallel vectors.
export const angleBetween = (x: V, y: V) => Math.atan2(Math.abs(x[0] * y[1] - x[1] * y[0]), dot(x, y));
export function project(y: V, x: V): V {
  const t = dot(x, y) / dot(x, x);
  return [t * x[0], t * x[1]];
}
export const norms = (x: V) => ({ l1: Math.abs(x[0]) + Math.abs(x[1]), l2: len(x), linf: Math.max(Math.abs(x[0]), Math.abs(x[1])) });

type Ball = 'none' | 'l1' | 'l2' | 'linf';

export default function VectorPlayground({ props }: WidgetProps) {
  const [x1, setX1] = useState(num(props, 'x1', 2));
  const [x2, setX2] = useState(num(props, 'x2', 0.5));
  const [y1, setY1] = useState(num(props, 'y1', 1));
  const [y2, setY2] = useState(num(props, 'y2', 1.5));
  const [showSum, setShowSum] = useState(props.sum === 'true');
  const [showProj, setShowProj] = useState(props.proj !== 'false');
  const [ball, setBall] = useState<Ball>((props.ball as Ball) || 'none');
  const x: V = [x1, x2];
  const y: V = [y1, y2];
  const W = 360;
  const S = 50;
  const P = (p: V) => [W / 2 + p[0] * S, W / 2 - p[1] * S] as const;
  const arrow = (p: V, cls: string, key: string, from: V = [0, 0]) => {
    const [a, b] = P(from);
    const [c, d] = P(p);
    return <line key={key} x1={a} y1={b} x2={c} y2={d} className={cls} markerEnd="url(#vp-arrow)" />;
  };
  const zero = len(x) < 1e-9 || len(y) < 1e-9;
  const t = zero ? NaN : angleBetween(x, y);
  const p = zero ? ([0, 0] as V) : project(y, x);
  const n = norms(x);
  const ballPts: Record<Exclude<Ball, 'none'>, V[]> = {
    l1: [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 0]],
    linf: [[1, 1], [-1, 1], [-1, -1], [1, -1], [1, 1]],
    l2: Array.from({ length: 73 }, (_, i) => [Math.cos((i / 72) * 2 * Math.PI), Math.sin((i / 72) * 2 * Math.PI)] as V),
  };
  const ticks = [-3, -2, -1, 1, 2, 3];
  return (
    <Frame
      title="Vectors, the dot product and projection"
      caption={
        zero ? (
          <>A zero vector has no direction: the angle and the projection are undefined.</>
        ) : (
          <>
            From coordinates, x . y = {fmt(x1, 2)} x {fmt(y1, 2)} + {fmt(x2, 2)} x {fmt(y2, 2)} = {fmt(dot(x, y))}. From lengths and the angle,
            |x| |y| cos t = {fmt(len(x))} x {fmt(len(y))} x cos {fmt((t * 180) / Math.PI, 1)} degrees = {fmt(len(x) * len(y) * Math.cos(t))}. Cosine
            similarity {fmt(Math.cos(t))}. Norms of x: L1 {fmt(n.l1)}, L2 {fmt(n.l2)}, L-infinity {fmt(n.linf)}.
          </>
        )
      }
    >
      <svg viewBox={`0 0 ${W} ${W}`} className="widget-svg" role="img" aria-label="Two vectors x and y in the plane with their dot product and projection">
        <defs>
          <marker id="vp-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" className="arrowhead" />
          </marker>
        </defs>
        {ticks.map((k) => (
          <g key={k}>
            <line x1={P([k, -3.4])[0]} x2={P([k, 3.4])[0]} y1={P([k, -3.4])[1]} y2={P([k, 3.4])[1]} className="grid-line" />
            <line x1={P([-3.4, k])[0]} x2={P([3.4, k])[0]} y1={P([-3.4, k])[1]} y2={P([3.4, k])[1]} className="grid-line" />
          </g>
        ))}
        <line x1={10} x2={W - 10} y1={W / 2} y2={W / 2} className="axis" />
        <line x1={W / 2} x2={W / 2} y1={10} y2={W - 10} className="axis" />
        {ball !== 'none' && <polyline points={ballPts[ball].map((q) => P(q).join(',')).join(' ')} className="iso-curve" />}
        {showSum && (
          <>
            {arrow([x1 + y1, x2 + y2], 'svd-v', 'yx', x)}
            {arrow([x1 + y1, x2 + y2], 'main-curve', 'sum')}
            <text x={P([x1 + y1, x2 + y2])[0] + 6} y={P([x1 + y1, x2 + y2])[1] - 6}>
              x + y
            </text>
          </>
        )}
        {showProj && !zero && (
          <>
            <line x1={P(y)[0]} y1={P(y)[1]} x2={P(p)[0]} y2={P(p)[1]} className="cursor-line" />
            <line x1={P([-3.4 * x1 / len(x), -3.4 * x2 / len(x)])[0]} y1={P([-3.4 * x1 / len(x), -3.4 * x2 / len(x)])[1]} x2={P([3.4 * x1 / len(x), 3.4 * x2 / len(x)])[0]} y2={P([3.4 * x1 / len(x), 3.4 * x2 / len(x)])[1]} className="ref-curve" />
            {arrow(p, 'svd-u', 'p')}
            <text x={P(p)[0] + 6} y={P(p)[1] + 14}>
              projection
            </text>
          </>
        )}
        {arrow(x, 'basis-1', 'x')}
        {arrow(y, 'basis-2', 'y')}
        <text x={P(x)[0] + 6} y={P(x)[1] - 6}>x</text>
        <text x={P(y)[0] + 6} y={P(y)[1] - 6}>y</text>
      </svg>
      <div className="widget-controls grid2">
        <Slider label="x, first coordinate" value={x1} min={-3} max={3} step={0.1} onChange={setX1} />
        <Slider label="x, second coordinate" value={x2} min={-3} max={3} step={0.1} onChange={setX2} />
        <Slider label="y, first coordinate" value={y1} min={-3} max={3} step={0.1} onChange={setY1} />
        <Slider label="y, second coordinate" value={y2} min={-3} max={3} step={0.1} onChange={setY2} />
      </div>
      <div className="widget-controls">
        <Toggle label="Show x + y" checked={showSum} onChange={setShowSum} />
        <Toggle label="Show the projection of y onto x" checked={showProj} onChange={setShowProj} />
        <Select<Ball>
          label="Unit ball"
          value={ball}
          onChange={setBall}
          options={[
            { value: 'none', label: 'None' },
            { value: 'l1', label: 'L1 (diamond)' },
            { value: 'l2', label: 'L2 (circle)' },
            { value: 'linf', label: 'L-infinity (square)' },
          ]}
        />
      </div>
    </Frame>
  );
}
