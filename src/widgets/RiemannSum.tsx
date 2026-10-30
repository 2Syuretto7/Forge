import { useState } from 'react';
import { Frame, Select, Slider, num, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// Riemann sums and their refinements (M17). Halving the width of the strips divides
// the error by 2 for the left and right rules, by 4 for the midpoint and trapezoid
// rules and by 16 for Simpson's rule, as long as the function is smooth.

export type Rule = 'left' | 'right' | 'mid' | 'trap' | 'simpson';

export function riemann(f: (x: number) => number, a: number, b: number, n: number, rule: Rule): number {
  const h = (b - a) / n;
  let s = 0;
  if (rule === 'simpson') {
    const m = n % 2 ? n + 1 : n;
    const k = (b - a) / m;
    for (let i = 0; i <= m; i++) s += (i === 0 || i === m ? 1 : i % 2 ? 4 : 2) * f(a + i * k);
    return (s * k) / 3;
  }
  for (let i = 0; i < n; i++) {
    const x0 = a + i * h;
    if (rule === 'left') s += f(x0);
    else if (rule === 'right') s += f(x0 + h);
    else if (rule === 'mid') s += f(x0 + h / 2);
    else s += (f(x0) + f(x0 + h)) / 2;
  }
  return s * h;
}

export const FUNCS: Record<string, { label: string; f: (x: number) => number; a: number; b: number; exact: number; y: [number, number] }> = {
  square: { label: 'x squared on [0, 1]', f: (x) => x * x, a: 0, b: 1, exact: 1 / 3, y: [0, 1.1] },
  sin: { label: 'sin x on [0, pi]', f: Math.sin, a: 0, b: Math.PI, exact: 2, y: [0, 1.1] },
  gauss: { label: 'standard normal density on [-2, 2]', f: (x) => Math.exp((-x * x) / 2) / Math.sqrt(2 * Math.PI), a: -2, b: 2, exact: 0.9544997361036416, y: [0, 0.45] },
  beta: { label: 'density 6x(1 - x) on [0.2, 0.3]', f: (x) => 6 * x * (1 - x), a: 0.2, b: 0.3, exact: 0.112, y: [0, 1.6] },
  rsqrt: { label: '1 / sqrt(x) on [0, 1] (infinite at 0)', f: (x) => 1 / Math.sqrt(x), a: 0, b: 1, exact: 2, y: [0, 8] },
  wiggle: { label: 'sin(25x) on [0, 1]', f: (x) => Math.sin(25 * x), a: 0, b: 1, exact: (1 - Math.cos(25)) / 25, y: [-1.1, 1.1] },
};

export default function RiemannSum({ props }: WidgetProps) {
  const [name, setName] = useState(props.f && FUNCS[props.f] ? props.f : 'square');
  const [rule, setRule] = useState<Rule>((props.rule as Rule) || 'left');
  const [n, setN] = useState(num(props, 'n', 8));
  const F = FUNCS[name];
  const approx = riemann(F.f, F.a, F.b, n, rule);
  const err = Math.abs(approx - F.exact);
  const err2 = Math.abs(riemann(F.f, F.a, F.b, 2 * n, rule) - F.exact);
  const h = (F.b - F.a) / n;
  const xs = Array.from({ length: 301 }, (_, i) => F.a + ((F.b - F.a) * i) / 300);
  const curve = xs.map((x) => [x, F.f(x)] as [number, number]);
  const pad = (F.b - F.a) * 0.04;
  return (
    <Frame
      title="Riemann sums"
      caption={
        <>
          {n} strips of width {fmt(h)}: sum {Number.isFinite(approx) ? fmt(approx, 6) : 'infinite'}, exact integral {fmt(F.exact, 6)}, error {Number.isFinite(err) ? fmt(err) : 'infinite'}.{' '}
          {Number.isFinite(err) && Number.isFinite(err2) && err2 > 0 && <>Doubling to {2 * n} strips divides the error by {fmt(err / err2, 2)}.</>}
        </>
      }
    >
      <LinePlot label={`Strips under ${F.label}`} xDomain={[F.a - pad, F.b + pad]} yDomain={F.y} xlabel="x" ylabel="f(x)" series={[{ points: curve, cls: 'series-a', label: F.label }]}>
        {(sx, sy) =>
          rule === 'simpson'
            ? Array.from({ length: n + 1 }, (_, i) => F.a + i * h).map((x, i) => Number.isFinite(F.f(x)) && <circle key={i} cx={sx(x)} cy={sy(F.f(x))} r={3} className="dot-c" />)
            : Array.from({ length: n }, (_, i) => {
                const x0 = F.a + i * h;
                const y0 = sy(0);
                if (rule === 'trap') {
                  const p = [[x0, 0], [x0, F.f(x0)], [x0 + h, F.f(x0 + h)], [x0 + h, 0]].map(([u, v]) => `${sx(u)},${Number.isFinite(v) ? sy(v) : sy(F.y[1] * 2)}`).join(' ');
                  return <polygon key={i} points={p} fill="var(--practice)" fillOpacity={0.18} stroke="var(--practice)" />;
                }
                const v = F.f(rule === 'left' ? x0 : rule === 'right' ? x0 + h : x0 + h / 2);
                const top = Number.isFinite(v) ? sy(v) : sy(F.y[1] * 2);
                return <rect key={i} x={sx(x0)} width={sx(x0 + h) - sx(x0)} y={Math.min(top, y0)} height={Math.abs(y0 - top)} fill="var(--practice)" fillOpacity={0.18} stroke="var(--practice)" />;
              })
        }
      </LinePlot>
      <div className="widget-controls grid2">
        <Slider label="Strips n" value={n} min={1} max={128} step={1} onChange={setN} format={(v) => String(v)} />
      </div>
      <div className="widget-controls">
        <Select label="Function" value={name} onChange={setName} options={Object.entries(FUNCS).map(([value, g]) => ({ value, label: g.label }))} />
        <Select<Rule>
          label="Rule"
          value={rule}
          onChange={setRule}
          options={[
            { value: 'left', label: 'Left endpoints' },
            { value: 'right', label: 'Right endpoints' },
            { value: 'mid', label: 'Midpoints' },
            { value: 'trap', label: 'Trapezoids' },
            { value: 'simpson', label: 'Simpson (parabolas)' },
          ]}
        />
      </div>
    </Frame>
  );
}
