import { useMemo, useState } from 'react';
import { Frame, Slider, gauss, num, rng, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';
import { ridge } from './linalg';

// Linear random-features regression (the model derived in L06):
// inputs x in R^D with variances lambda_j = j^-1.5, target y = beta^T x + noise,
// features phi = W x with random Gaussian W (p rows), fit by ridge / min-norm
// least squares. Test error is the exact excess risk (beta - W^T w)^T Sigma (beta - W^T w).
const D = 200;

export function curve(n: number, noise: number, logLambda: number, seeds: number, maxP = 80) {
  const lambda = 10 ** logLambda;
  const lamX = Array.from({ length: D }, (_, j) => (j + 1) ** -1.5);
  const train = Array(maxP).fill(0);
  const test = Array(maxP).fill(0);
  for (let s = 0; s < seeds; s++) {
    const r = rng(101 + 7919 * s);
    let beta = lamX.map((l) => gauss(r) * Math.sqrt(l));
    const sig = Math.sqrt(beta.reduce((a, b, j) => a + lamX[j] * b * b, 0));
    beta = beta.map((b) => b / sig);
    const X = Array.from({ length: n }, () => lamX.map((l) => gauss(r) * Math.sqrt(l)));
    const y = X.map((x) => x.reduce((a, v, j) => a + v * beta[j], 0) + noise * gauss(r));
    const W = Array.from({ length: maxP }, () => Array.from({ length: D }, () => gauss(r)));
    const PhiAll = X.map((x) => W.map((wr) => wr.reduce((a, v, j) => a + v * x[j], 0)));
    for (let p = 1; p <= maxP; p++) {
      const Phi = PhiAll.map((row) => row.slice(0, p));
      const w = ridge(Phi, y, lambda);
      train[p - 1] += Phi.reduce((a, row, i) => a + (row.reduce((b, v, k) => b + v * w[k], 0) - y[i]) ** 2, 0) / n;
      let risk = 0;
      for (let j = 0; j < D; j++) {
        let fit = 0;
        for (let k = 0; k < p; k++) fit += W[k][j] * w[k];
        risk += lamX[j] * (beta[j] - fit) ** 2;
      }
      test[p - 1] += risk;
    }
  }
  return {
    train: train.map((v, i) => [i + 1, Math.max(v / seeds, 1e-6)] as [number, number]),
    test: test.map((v, i) => [i + 1, Math.max(v / seeds, 1e-6)] as [number, number]),
  };
}

export default function BiasVarianceCurve({ props }: WidgetProps) {
  const n = Math.round(num(props, 'n', 20));
  const [noise, setNoise] = useState(num(props, 'noise', 0.3));
  const [logLambda, setLogLambda] = useState(num(props, 'loglambda', -9));
  const { train, test } = useMemo(() => curve(n, noise, logLambda, 8), [n, noise, logLambda]);
  const under = test.slice(0, n - 2).reduce((b, pt) => (pt[1] < b[1] ? pt : b));
  const over = test.slice(n + 2).reduce((b, pt) => (pt[1] < b[1] ? pt : b));
  const peak = test.reduce((b, pt) => (pt[1] > b[1] ? pt : b));
  return (
    <Frame
      title="Train and test error as capacity grows (linear random features)"
      caption={
        <>
          n = {n} training points; the model has p random features of a 200-dimensional input, fit by least squares (minimum norm once p &gt; n), averaged
          over 8 draws. Best underparameterized test error {fmt(under[1])} at p = {under[0]}; peak {fmt(peak[1])} at p = {peak[0]}; best
          overparameterized {fmt(over[1])} at p = {over[0]}. Raise the ridge penalty to flatten the peak.
        </>
      }
    >
      <LinePlot
        label="Train and test error against number of features"
        series={[
          { points: train, cls: 'series-a', label: 'train error' },
          { points: test, cls: 'series-c', label: 'test error (excess risk)' },
        ]}
        xDomain={[1, 80]}
        yDomain={[1e-3, 100]}
        ylog
        xlabel="number of random features p"
        ylabel="mean squared error"
        height={260}
      >
        {(x, y) => <line x1={x(n)} x2={x(n)} y1={y(100)} y2={y(1e-3)} className="series-d" strokeDasharray="3 3" />}
      </LinePlot>
      <div className="widget-controls grid2">
        <Slider label="Label noise (standard deviation)" value={noise} min={0} max={1} step={0.01} onChange={setNoise} />
        <Slider label="Ridge penalty (log10 lambda)" value={logLambda} min={-9} max={1} step={0.25} onChange={setLogLambda} format={(v) => `1e${v}`} />
      </div>
    </Frame>
  );
}
