import { useState } from 'react';
import { Frame, Select, Slider, num, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// Taylor polynomials around a centre a (M16). Raise the order n and the polynomial
// hugs the function over a wider range; the Lagrange remainder bounds the error for
// exp, sin and cos, while log(1 + x) and 1/(1 - x) only converge within the distance
// from a to their singularity at -1 or 1.

export type Name = 'exp' | 'sin' | 'cos' | 'log1p' | 'geom';

const fact = (k: number) => {
  let p = 1;
  for (let i = 2; i <= k; i++) p *= i;
  return p;
};

export const FUNCS: Record<Name, { label: string; f: (x: number) => number; radius: (a: number) => number; y: [number, number]; centres: [number, number] }> = {
  exp: { label: 'e to the x', f: Math.exp, radius: () => Infinity, y: [-2, 12], centres: [-2, 2] },
  sin: { label: 'sin x', f: Math.sin, radius: () => Infinity, y: [-2.5, 2.5], centres: [-2, 2] },
  cos: { label: 'cos x', f: Math.cos, radius: () => Infinity, y: [-2.5, 2.5], centres: [-2, 2] },
  log1p: { label: 'log(1 + x)', f: (x) => (x > -1 ? Math.log1p(x) : NaN), radius: (a) => 1 + a, y: [-3, 2.5], centres: [-0.5, 2] },
  geom: { label: '1 / (1 - x)', f: (x) => 1 / (1 - x), radius: (a) => Math.abs(1 - a), y: [-4, 8], centres: [-2, 0.5] },
};

// c_k = f^(k)(a) / k!
export function taylorCoeffs(name: Name, a: number, n: number): number[] {
  return Array.from({ length: n + 1 }, (_, k) => {
    switch (name) {
      case 'exp':
        return Math.exp(a) / fact(k);
      case 'sin':
        return [Math.sin(a), Math.cos(a), -Math.sin(a), -Math.cos(a)][k % 4] / fact(k);
      case 'cos':
        return [Math.cos(a), -Math.sin(a), -Math.cos(a), Math.sin(a)][k % 4] / fact(k);
      case 'log1p':
        return k === 0 ? Math.log1p(a) : (-1) ** (k - 1) / (k * (1 + a) ** k);
      case 'geom':
        return 1 / (1 - a) ** (k + 1);
    }
  });
}

export function taylorEval(c: number[], a: number, x: number) {
  let s = 0;
  for (let k = c.length - 1; k >= 0; k--) s = s * (x - a) + c[k];
  return s;
}

// Lagrange: |R_n(x)| <= max |f^(n+1)| |x - a|^(n+1) / (n+1)! on the interval between a and x.
export function lagrangeBound(name: Name, a: number, x: number, n: number) {
  const M = name === 'exp' ? Math.exp(Math.max(a, x)) : name === 'sin' || name === 'cos' ? 1 : NaN;
  return (M * Math.abs(x - a) ** (n + 1)) / fact(n + 1);
}

export default function TaylorBuilder({ props }: WidgetProps) {
  const [name, setName] = useState<Name>((props.f as Name) in FUNCS ? (props.f as Name) : 'sin');
  const [a0, setA] = useState(num(props, 'a', 0));
  const [n, setN] = useState(num(props, 'n', 3));
  const [x0, setX0] = useState(num(props, 'x', 1));
  const F = FUNCS[name];
  const a = Math.min(F.centres[1], Math.max(F.centres[0], a0));
  const c = taylorCoeffs(name, a, n);
  const lo = a - 4;
  const hi = a + 4;
  const xs = Array.from({ length: 401 }, (_, i) => lo + ((hi - lo) * i) / 400);
  const clip = (v: number) => (Number.isFinite(v) && v > F.y[0] - 50 && v < F.y[1] + 50 ? v : NaN);
  const fx = F.f(x0);
  const tx = taylorEval(c, a, x0);
  const R = F.radius(a);
  const bound = lagrangeBound(name, a, x0, n);
  return (
    <Frame
      title="Taylor polynomials"
      caption={
        <>
          At x = {fmt(x0, 2)}: f = {fmt(fx, 6)}, the degree-{n} polynomial gives {fmt(tx, 6)}, error {fmt(Math.abs(fx - tx))}.{' '}
          {Number.isFinite(bound) ? (
            <>The Lagrange remainder bounds the error by {fmt(bound)}.</>
          ) : Math.abs(x0 - a) < R ? (
            <>Inside the radius of convergence {fmt(R, 2)}: the error shrinks as the degree grows.</>
          ) : (
            <>Outside the radius of convergence {fmt(R, 2)}: adding terms makes the error larger, not smaller.</>
          )}
        </>
      }
    >
      <LinePlot
        label={`${F.label} and its Taylor polynomial of degree ${n} around ${a}`}
        xDomain={[lo, hi]}
        yDomain={F.y}
        xlabel="x"
        ylabel="y"
        series={[
          { points: xs.map((x) => [x, clip(F.f(x))] as [number, number]), cls: 'series-a', label: F.label },
          { points: xs.map((x) => [x, clip(taylorEval(c, a, x))] as [number, number]), cls: 'series-c', label: `degree ${n} around a = ${fmt(a, 2)}` },
        ]}
      >
        {(sx, sy) => (
          <>
            <line x1={sx(x0)} x2={sx(x0)} y1={sy(F.y[0])} y2={sy(F.y[1])} className="cursor-line" />
            {Number.isFinite(F.f(a)) && <circle cx={sx(a)} cy={sy(F.f(a))} r={4} className="dot-c" />}
          </>
        )}
      </LinePlot>
      <div className="widget-controls grid2">
        <Slider label="Degree n" value={n} min={0} max={15} step={1} onChange={setN} format={(v) => String(v)} />
        <Slider label="Centre a" value={a} min={F.centres[0]} max={F.centres[1]} step={0.25} onChange={setA} />
        <Slider label="Evaluate at x" value={x0} min={a - 4} max={a + 4} step={0.05} onChange={setX0} />
      </div>
      <div className="widget-controls">
        <Select<Name> label="Function" value={name} onChange={setName} options={(Object.keys(FUNCS) as Name[]).map((k) => ({ value: k, label: FUNCS[k].label }))} />
      </div>
    </Frame>
  );
}
