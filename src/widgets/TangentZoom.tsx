import { useState } from 'react';
import { Frame, Select, Slider, num, type WidgetProps, fmt } from './common';
import { LinePlot, type Series } from './plot';

// Zoom in on a graph around x = a (M15). A differentiable function looks more and
// more like its tangent line, and the secant slopes from the left and the right agree
// in the limit. At a corner they never agree, however far you zoom.

type F = { label: string; f: (x: number) => number; df: (x: number) => number };

export const FUNCS: Record<string, F> = {
  square: { label: 'x squared', f: (x) => x * x, df: (x) => 2 * x },
  sin: { label: 'sin x', f: Math.sin, df: Math.cos },
  exp: { label: 'e to the x', f: Math.exp, df: Math.exp },
  abs: { label: '|x|', f: Math.abs, df: (x) => (x === 0 ? NaN : Math.sign(x)) },
  relu: { label: 'ReLU, max(0, x)', f: (x) => Math.max(0, x), df: (x) => (x === 0 ? NaN : x > 0 ? 1 : 0) },
  cbrt: { label: 'cube root of x', f: Math.cbrt, df: (x) => (x === 0 ? NaN : 1 / (3 * Math.cbrt(x) ** 2)) },
};

export function secantSlopes(f: (x: number) => number, a: number, h: number) {
  return { left: (f(a) - f(a - h)) / h, right: (f(a + h) - f(a)) / h, central: (f(a + h) - f(a - h)) / (2 * h) };
}

export default function TangentZoom({ props }: WidgetProps) {
  const [name, setName] = useState(props.f && FUNCS[props.f] ? props.f : 'square');
  const [a, setA] = useState(num(props, 'a', 1));
  const [zoom, setZoom] = useState(num(props, 'zoom', 0));
  const { f, df } = FUNCS[name];
  const w = 2 / 2 ** zoom;
  const fa = f(a);
  const d = df(a);
  const m = Number.isFinite(d) ? Math.max(1, Math.abs(d)) : 1.5;
  const pts: [number, number][] = Array.from({ length: 201 }, (_, i) => {
    const u = -w + (2 * w * i) / 200;
    return [u, f(a + u) - fa];
  });
  const s = secantSlopes(f, a, w);
  const series: Series[] = [{ points: pts, cls: 'series-a', label: FUNCS[name].label }];
  if (Number.isFinite(d)) series.push({ points: [[-w, -d * w], [w, d * w]], cls: 'series-c', label: 'tangent line', dashed: true });
  return (
    <Frame
      title="Zoom until the curve looks straight"
      caption={
        <>
          Window half-width h = {fmt(w)}. Slope from the left {fmt(s.left)}, from the right {fmt(s.right)}.{' '}
          {Number.isFinite(d) ? (
            <>
              Derivative f&apos;({fmt(a, 2)}) = {fmt(d)}: both secants approach it as h shrinks, and the curve becomes indistinguishable from the tangent.
            </>
          ) : (
            <>No derivative at this point: the two one-sided slopes do not approach a common value, however far you zoom.</>
          )}
        </>
      }
    >
      <LinePlot label={`Graph of ${FUNCS[name].label} near x = ${a}`} series={series} xDomain={[-w, w]} yDomain={[-1.3 * m * w, 1.3 * m * w]} xlabel="x - a" ylabel="f(x) - f(a)">
        {(sx, sy) => <circle cx={sx(0)} cy={sy(0)} r={4} className="dot-c" />}
      </LinePlot>
      <div className="widget-controls grid2">
        <Slider label="Zoom (halvings of the window)" value={zoom} min={0} max={16} step={1} onChange={setZoom} format={(v) => String(v)} />
        <Slider label="Point a" value={a} min={-2} max={2} step={0.25} onChange={setA} />
      </div>
      <div className="widget-controls">
        <Select label="Function" value={name} onChange={setName} options={Object.entries(FUNCS).map(([value, g]) => ({ value, label: g.label }))} />
      </div>
    </Frame>
  );
}
