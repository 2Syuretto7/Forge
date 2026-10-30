import { useMemo, useState } from 'react';
import { Frame, Select, Slider, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// Two modes (M04). compose: functions as machines; f(g(x)) and g(f(x)) are different
// machines. relu: a sum of shifted ReLUs is the piecewise-linear curve through n + 1
// points of a target, and its worst error shrinks as the pieces multiply.

export const MACHINES: Record<string, [string, (x: number) => number]> = {
  square: ['square it', (x) => x * x],
  plus1: ['add 1', (x) => x + 1],
  double: ['double it', (x) => 2 * x],
  relu: ['ReLU: max(0, x)', (x) => Math.max(0, x)],
  abs: ['absolute value', (x) => Math.abs(x)],
  sin: ['sine', (x) => Math.sin(x)],
  neg: ['negate', (x) => -x],
};

export const TARGETS: Record<string, [string, (x: number) => number]> = {
  bump: ['a smooth hill, exp(-x^2)', (x) => Math.exp(-x * x)],
  sine: ['sin(x)', (x) => Math.sin(x)],
  cube: ['x^3 / 9', (x) => (x * x * x) / 9],
};

const relu = (x: number) => Math.max(0, x);

// The interpolant through (t_k, f(t_k)) on n equal pieces of [a, b], written as
// f(t_0) + s_0 (x - t_0) + sum over interior knots of (s_k - s_{k-1}) relu(x - t_k).
export function reluInterp(f: (x: number) => number, n: number, a: number, b: number) {
  const t = Array.from({ length: n + 1 }, (_, k) => a + ((b - a) * k) / n);
  const y = t.map(f);
  const s = Array.from({ length: n }, (_, k) => (y[k + 1] - y[k]) / (t[k + 1] - t[k]));
  const w = s.map((sk, k) => (k === 0 ? sk : sk - s[k - 1]));
  const evaluate = (x: number) => y[0] + w[0] * (x - t[0]) + w.slice(1).reduce((acc, wk, k) => acc + wk * relu(x - t[k + 1]), 0);
  return { knots: t, weights: w, evaluate };
}

export function maxError(f: (x: number) => number, g: (x: number) => number, a: number, b: number, m = 2000) {
  let e = 0;
  for (let i = 0; i <= m; i++) {
    const x = a + ((b - a) * i) / m;
    e = Math.max(e, Math.abs(f(x) - g(x)));
  }
  return e;
}

const grid = (a: number, b: number, m = 240) => Array.from({ length: m + 1 }, (_, i) => a + ((b - a) * i) / m);

export default function FunctionMachine({ props }: WidgetProps) {
  const [mode, setMode] = useState<'compose' | 'relu'>(props.mode === 'relu' ? 'relu' : 'compose');
  const [f, setF] = useState(props.f && MACHINES[props.f] ? props.f : 'square');
  const [g, setG] = useState(props.g && MACHINES[props.g] ? props.g : 'plus1');
  const [target, setTarget] = useState(props.target && TARGETS[props.target] ? props.target : 'bump');
  const [n, setN] = useState(Number(props.n) || 4);
  const [x0, setX0] = useState(1);
  const xs = grid(-3, 3);
  const F = MACHINES[f][1];
  const G = MACHINES[g][1];
  const fit = useMemo(() => reluInterp(TARGETS[target][1], n, -3, 3), [target, n]);
  const err = useMemo(() => maxError(TARGETS[target][1], fit.evaluate, -3, 3), [target, fit]);

  if (mode === 'relu') {
    const T = TARGETS[target][1];
    return (
      <Frame
        title="A sum of shifted ReLUs draws a curve"
        caption={
          <>
            {n} piece{n === 1 ? '' : 's'}: {n - 1} ReLU{n - 1 === 1 ? '' : 's'} plus a straight line. Largest error on [-3, 3]: {fmt(err)}. Doubling the
            pieces cuts the error of a smooth curve by about four.
          </>
        }
      >
        <LinePlot
          label="Target curve and its ReLU approximation"
          xDomain={[-3, 3]}
          yDomain={target === 'bump' ? [-0.2, 1.2] : [-3.2, 3.2]}
          xlabel="x"
          ylabel="y"
          series={[
            { label: 'target', cls: 'series-a', points: xs.map((x) => [x, T(x)]) },
            { label: 'sum of ReLUs', cls: 'series-c', points: xs.map((x) => [x, fit.evaluate(x)]) },
          ]}
        />
        <div className="widget-controls grid2">
          <Select
            label="Target"
            value={target}
            options={Object.entries(TARGETS).map(([k, [l]]) => ({ value: k, label: l }))}
            onChange={setTarget}
          />
          <Slider label="Pieces" value={n} min={1} max={40} step={1} onChange={setN} format={(v) => String(v)} />
        </div>
        <div className="widget-controls">
          <button className="btn small ghost" onClick={() => setMode('compose')}>
            Switch to composing machines
          </button>
        </div>
      </Frame>
    );
  }
  return (
    <Frame
      title="Functions as machines: the order of composition matters"
      caption={
        <>
          At x = {fmt(x0)}: g first, then f gives f(g(x)) = {fmt(F(G(x0)))}; f first, then g gives g(f(x)) = {fmt(G(F(x0)))}.{' '}
          {Math.abs(F(G(x0)) - G(F(x0))) < 1e-12 ? 'Here the two orders agree.' : 'The two orders give different machines.'}
        </>
      }
    >
      <LinePlot
        label="Graphs of f(g(x)) and g(f(x))"
        xDomain={[-3, 3]}
        yDomain={[-4, 10]}
        xlabel="x"
        ylabel="output"
        series={[
          { label: 'f(g(x))', cls: 'series-a', points: xs.map((x) => [x, F(G(x))]) },
          { label: 'g(f(x))', cls: 'series-b', points: xs.map((x) => [x, G(F(x))]) },
        ]}
      />
      <div className="widget-controls grid2">
        <Select label="f" value={f} options={Object.entries(MACHINES).map(([k, [l]]) => ({ value: k, label: l }))} onChange={setF} />
        <Select label="g" value={g} options={Object.entries(MACHINES).map(([k, [l]]) => ({ value: k, label: l }))} onChange={setG} />
        <Slider label="x" value={x0} min={-3} max={3} step={0.1} onChange={setX0} />
      </div>
      <div className="widget-controls">
        <button className="btn small ghost" onClick={() => setMode('relu')}>
          Switch to drawing with ReLUs
        </button>
      </div>
    </Frame>
  );
}
