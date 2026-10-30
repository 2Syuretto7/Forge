import { useState } from 'react';
import { Frame, Slider, Toggle, type WidgetProps, fmt } from './common';

// The unit circle and complex multiplication (M07). The point at angle theta is
// (cos theta, sin theta) = e^(i theta); multiplying by r e^(i phi) scales by r and turns
// by phi, so rotations compose by adding angles.

export type C = [number, number];
export const mul = (a: C, b: C): C => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
export const polar = (z: C) => ({ r: Math.hypot(z[0], z[1]), theta: Math.atan2(z[1], z[0]) });
export const cis = (theta: number, r = 1): C => [r * Math.cos(theta), r * Math.sin(theta)];

const DEG = Math.PI / 180;

export default function UnitCircle({ props }: WidgetProps) {
  const [a, setA] = useState(Number(props.theta) || 30);
  const [b, setB] = useState(Number(props.phi) || 45);
  const [r, setR] = useState(Number(props.r) || 1);
  const [rad, setRad] = useState(false);
  const z = cis(a * DEG);
  const w = cis(b * DEG, r);
  const zw = mul(z, w);
  const pw = polar(zw);
  const W = 360;
  const S = 110;
  const P = (p: C) => [W / 2 + p[0] * S, W / 2 - p[1] * S] as const;
  const ang = (d: number) => (rad ? `${fmt(d * DEG)} rad` : `${fmt(d, 1)} degrees`);
  const arrow = (p: C, cls: string, key: string) => {
    const [x, y] = P(p);
    return <line key={key} x1={W / 2} y1={W / 2} x2={x} y2={y} className={cls} markerEnd="url(#uc-arrow)" />;
  };
  const circle = Array.from({ length: 97 }, (_, i) => P(cis((i / 96) * 2 * Math.PI)).join(',')).join(' ');
  const [zx, zy] = P(z);
  return (
    <Frame
      title="Angles, the unit circle and complex multiplication"
      caption={
        <>
          z = cos {ang(a)} + i sin {ang(a)} = {fmt(z[0])} + {fmt(z[1])}i. w has length {fmt(r)} and angle {ang(b)}. Their product z w has length{' '}
          {fmt(pw.r)} and angle {ang(((pw.theta / DEG) % 360 + 360) % 360)}: lengths multiply and angles add.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${W}`} className="widget-svg" role="img" aria-label="Unit circle with the points z, w and their product">
        <defs>
          <marker id="uc-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" className="arrowhead" />
          </marker>
        </defs>
        <line x1={10} x2={W - 10} y1={W / 2} y2={W / 2} className="grid-line" />
        <line x1={W / 2} x2={W / 2} y1={10} y2={W - 10} className="grid-line" />
        <polyline points={circle} className="ref-curve" fill="none" />
        <line x1={zx} y1={zy} x2={zx} y2={W / 2} className="cursor-line" />
        <line x1={zx} y1={zy} x2={W / 2} y2={zy} className="cursor-line" />
        {arrow(z, 'basis-1', 'z')}
        {arrow(w, 'basis-2', 'w')}
        {arrow(zw, 'main-curve', 'zw')}
        <text x={P(z)[0] + 6} y={P(z)[1] - 6}>z</text>
        <text x={P(w)[0] + 6} y={P(w)[1] - 6}>w</text>
        <text x={P(zw)[0] + 6} y={P(zw)[1] - 6}>z w</text>
        <text x={zx} y={W / 2 + 14} textAnchor="middle">
          cos
        </text>
        <text x={W / 2 - 6} y={zy + 4} textAnchor="end">
          sin
        </text>
      </svg>
      <div className="widget-controls grid2">
        <Slider label="Angle of z (degrees)" value={a} min={-180} max={180} step={1} onChange={setA} format={(v) => String(v)} />
        <Slider label="Angle of w (degrees)" value={b} min={-180} max={180} step={1} onChange={setB} format={(v) => String(v)} />
        <Slider label="Length of w" value={r} min={0.2} max={1.5} step={0.05} onChange={setR} />
      </div>
      <div className="widget-controls">
        <Toggle label="Show angles in radians" checked={rad} onChange={setRad} />
      </div>
    </Frame>
  );
}
