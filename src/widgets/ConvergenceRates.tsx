import { useMemo, useState } from 'react';
import { Frame, Slider, Toggle, num, type WidgetProps, fmt } from './common';
import { LinePlot, type Series } from './plot';

// Gradient descent, heavy-ball momentum and Nesterov on a quadratic with condition
// number kappa (M29). Each method runs with its textbook-optimal constants, the error
// is plotted on a log scale, and the measured late rate is compared with the proved
// one: (kappa - 1)/(kappa + 1) for gradient descent, (sqrt(kappa) - 1)/(sqrt(kappa) + 1)
// for heavy ball, and 1 - 1/sqrt(kappa) for Nesterov.

export type Method = 'gd' | 'heavy' | 'nesterov';

export function spectrum(kappa: number, d = 24) {
  return Array.from({ length: d }, (_, i) => Math.pow(kappa, i / (d - 1)));
}

export function predictedRate(m: Method, kappa: number) {
  const s = Math.sqrt(kappa);
  if (m === 'gd') return (kappa - 1) / (kappa + 1);
  if (m === 'heavy') return (s - 1) / (s + 1);
  return 1 - 1 / s;
}

// Error norms of each method on the diagonal quadratic (1/2) sum lambda_i x_i^2, from x = 1.
// Heavy ball takes an optional momentum override; otherwise its optimal value.
export function runMethod(m: Method, kappa: number, iters: number, beta?: number): number[] {
  const lam = spectrum(kappa);
  const L = kappa;
  const mu = 1;
  let x = lam.map(() => 1);
  let prev = x.slice();
  const out = [Math.hypot(...x)];
  for (let k = 0; k < iters; k++) {
    let next: number[];
    if (m === 'gd') {
      const a = 2 / (L + mu);
      next = x.map((v, i) => v - a * lam[i] * v);
    } else if (m === 'heavy') {
      const a = 4 / (Math.sqrt(L) + Math.sqrt(mu)) ** 2;
      const b = beta ?? ((Math.sqrt(kappa) - 1) / (Math.sqrt(kappa) + 1)) ** 2;
      next = x.map((v, i) => v - a * lam[i] * v + b * (v - prev[i]));
    } else {
      const a = 1 / L;
      const b = (Math.sqrt(kappa) - 1) / (Math.sqrt(kappa) + 1);
      const y = x.map((v, i) => v + b * (v - prev[i]));
      next = y.map((v, i) => v - a * lam[i] * v);
    }
    prev = x;
    x = next;
    out.push(Math.hypot(...x));
  }
  return out;
}

// Late per-step rate: geometric mean of the error ratio over the last window steps.
export function measuredRate(errors: number[], window = 40) {
  const n = errors.length - 1;
  const a = errors[Math.max(0, n - window)];
  const b = errors[n];
  if (!(a > 0) || !(b > 0)) return NaN;
  return Math.pow(b / a, 1 / Math.min(window, n));
}

const LABEL: Record<Method, string> = { gd: 'gradient descent', heavy: 'heavy ball', nesterov: 'Nesterov' };
const CLS: Record<Method, Series['cls']> = { gd: 'series-a', heavy: 'series-b', nesterov: 'series-c' };

export default function ConvergenceRates({ props }: WidgetProps) {
  const [logKappa, setLogKappa] = useState(num(props, 'logkappa', 2));
  const [iters, setIters] = useState(num(props, 'iters', 300));
  const [useBeta, setUseBeta] = useState(props.beta !== undefined);
  const [beta, setBeta] = useState(num(props, 'beta', 0.5));
  const kappa = Math.pow(10, logKappa);
  const runs = useMemo(
    () =>
      ({
        gd: runMethod('gd', kappa, iters),
        heavy: runMethod('heavy', kappa, iters, useBeta ? beta : undefined),
        nesterov: runMethod('nesterov', kappa, iters),
      }) as Record<Method, number[]>,
    [kappa, iters, useBeta, beta],
  );
  const floor = 1e-16;
  const methods: Method[] = ['gd', 'heavy', 'nesterov'];
  const series = methods.map((m) => ({
    points: runs[m].map((e, k) => [k, Math.max(e / runs[m][0], floor)] as [number, number]),
    cls: CLS[m],
    label: LABEL[m],
  }));
  return (
    <Frame
      title="Convergence rates of first-order methods"
      caption={
        <>
          Condition number {fmt(kappa, 0)}. Late rate per step, measured against proved:{' '}
          {methods
            .map((m) => `${LABEL[m]} ${fmt(measuredRate(runs[m]), 4)} vs ${fmt(m === 'heavy' && useBeta ? NaN : predictedRate(m, kappa), 4)}`)
            .join('; ')}
          . Momentum turns the dependence on kappa into one on its square root; a momentum above the optimum makes heavy ball oscillate, below it slows it down.
        </>
      }
    >
      <LinePlot
        label="Relative error against iteration on a log scale for three methods"
        series={series}
        xDomain={[0, iters]}
        yDomain={[1e-12, 2]}
        ylog
        xlabel="iteration"
        ylabel="relative error"
      />
      <div className="widget-controls grid2">
        <Slider label="log10 condition number" value={logKappa} min={0.5} max={4} step={0.1} onChange={setLogKappa} format={(v) => `10^${v.toFixed(1)}`} />
        <Slider label="Iterations" value={iters} min={50} max={2000} step={50} onChange={setIters} format={(v) => String(v)} />
        <Slider label="Heavy-ball momentum" value={beta} min={0} max={0.999} step={0.001} onChange={setBeta} format={(v) => v.toFixed(3)} />
      </div>
      <div className="widget-controls">
        <Toggle label="Use the momentum slider instead of the optimal momentum" checked={useBeta} onChange={setUseBeta} />
      </div>
    </Frame>
  );
}
