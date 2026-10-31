import { useMemo, useState } from 'react';
import { Frame, Slider, num, rng as makeRng, gauss, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// Two ways to estimate a gradient of an expectation (M36). For x ~ N(mu, I) in d dimensions
// and f(x) = |x|^2, the gradient of E f(x) with respect to mu_1 is 2 mu_1. The score-function
// (REINFORCE) estimator f(x) (x_1 - mu_1) needs only values of f; the reparameterization
// estimator 2 (mu_1 + eps_1) differentiates through the sample. At mu = 0 their per-sample
// variances are (d + 2)(d + 4), 2d + 8 with the baseline b = E f, and 4.

export type Estimator = 'score' | 'baseline' | 'reparam';

export function sampleVariance(est: Estimator, d: number, mu: number, n: number, seed = 3) {
  const r = makeRng(seed);
  const meanF = d * (1 + mu * mu);
  let s = 0;
  let s2 = 0;
  for (let k = 0; k < n; k++) {
    let f = 0;
    let e1 = 0;
    for (let i = 0; i < d; i++) {
      const e = gauss(r);
      if (i === 0) e1 = e;
      const x = mu + e;
      f += x * x;
    }
    const g = est === 'reparam' ? 2 * (mu + e1) : (est === 'baseline' ? f - meanF : f) * e1;
    s += g;
    s2 += g * g;
  }
  const m = s / n;
  return { mean: m, variance: s2 / n - m * m };
}

// Exact per-sample variances at mu = 0.
export function theoryVariance(est: Estimator, d: number) {
  if (est === 'score') return (d + 2) * (d + 4);
  if (est === 'baseline') return 2 * d + 8;
  return 4;
}

export default function EstimatorVariance({ props }: WidgetProps) {
  const [maxD, setMaxD] = useState(num(props, 'maxd', 256));
  const [mu, setMu] = useState(num(props, 'mu', 0));
  const [n, setN] = useState(num(props, 'n', 2000));
  const ds = useMemo(() => {
    const out: number[] = [];
    for (let d = 1; d <= maxD; d = Math.max(d + 1, Math.round(d * 1.5))) out.push(d);
    return out;
  }, [maxD]);
  const curves = useMemo(
    () =>
      (['score', 'baseline', 'reparam'] as Estimator[]).map((est) =>
        ds.map((d) => [d, Math.max(1e-3, sampleVariance(est, d, mu, n).variance)] as [number, number]),
      ),
    [ds, mu, n],
  );
  const last = ds[ds.length - 1];
  const at = (k: number) => curves[k][curves[k].length - 1][1];
  return (
    <Frame
      title="Variance of gradient estimators"
      caption={
        <>
          Per-sample variance of three unbiased estimates of the gradient of E|x|^2 with respect to the first coordinate of the mean, for x ~ N(mu, I) in d dimensions,
          from {n} samples at each d. At d = {last}: score function {fmt(at(0), 1)}, with the baseline E f {fmt(at(1), 1)}, reparameterization {fmt(at(2), 2)}. The
          score function sees only f, which sums noise from all d coordinates; the reparameterized gradient sees the one coordinate that matters.
        </>
      }
    >
      <LinePlot
        label="Per-sample variance against dimension on log scales, for the score-function estimator with and without a baseline and for the reparameterization estimator"
        series={[
          { points: curves[0], cls: 'series-a', label: 'score function' },
          { points: curves[1], cls: 'series-b', label: 'score function with baseline' },
          { points: curves[2], cls: 'series-c', label: 'reparameterization' },
        ]}
        xDomain={[1, last]}
        yDomain={[1, Math.max(10, ...curves[0].map((p) => p[1])) * 1.5]}
        xlog
        ylog
        xlabel="dimension d"
        ylabel="variance per sample"
      />
      <div className="widget-controls grid2">
        <Slider label="Largest dimension" value={maxD} min={8} max={512} step={8} onChange={setMaxD} format={(v) => String(v)} />
        <Slider label="Mean mu (every coordinate)" value={mu} min={0} max={2} step={0.1} onChange={setMu} />
        <Slider label="Samples per point" value={n} min={200} max={5000} step={200} onChange={setN} format={(v) => String(v)} />
      </div>
    </Frame>
  );
}
