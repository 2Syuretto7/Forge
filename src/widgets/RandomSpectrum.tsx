import { useMemo, useState } from 'react';
import { Frame, Slider, num, rng as makeRng, gauss, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';
import { symEigvals } from './SpectrumBars';

// Eigenvalues of a sample covariance (M34). X has n rows of p independent standard normal
// features, gamma = p / n, and S = X^T X / n. As p and n grow with gamma fixed, the
// histogram of S's eigenvalues approaches the Marchenko-Pastur density on
// [(1 - sqrt gamma)^2, (1 + sqrt gamma)^2], although the true covariance is the identity.
// A planted direction with variance 1 + ell separates from the bulk only when
// ell > sqrt(gamma), at (1 + ell)(1 + gamma / ell): the BBP transition.

export function mpEdges(gamma: number): [number, number] {
  const r = Math.sqrt(gamma);
  return [(1 - r) ** 2, (1 + r) ** 2];
}

export function mpDensity(x: number, gamma: number) {
  const [a, b] = mpEdges(gamma);
  if (x <= a || x >= b) return 0;
  return Math.sqrt((b - x) * (x - a)) / (2 * Math.PI * gamma * x);
}

// Where the top eigenvalue lands for a planted spike of strength ell.
export function bbpOutlier(ell: number, gamma: number) {
  return ell > Math.sqrt(gamma) ? (1 + ell) * (1 + gamma / ell) : mpEdges(gamma)[1];
}

export function sampleCovEigs(p: number, gamma: number, spike = 0, seed = 7) {
  const n = Math.max(p, Math.round(p / gamma));
  const r = makeRng(seed);
  const X = Array.from({ length: n }, () => Array.from({ length: p }, () => gauss(r)));
  const s0 = Math.sqrt(1 + spike);
  for (const row of X) row[0] *= s0;
  const S = Array.from({ length: p }, () => new Array<number>(p).fill(0));
  for (const row of X)
    for (let i = 0; i < p; i++) {
      const ri = row[i];
      for (let j = i; j < p; j++) S[i][j] += ri * row[j];
    }
  for (let i = 0; i < p; i++)
    for (let j = i; j < p; j++) {
      S[i][j] /= n;
      S[j][i] = S[i][j];
    }
  return symEigvals(S);
}

export default function RandomSpectrum({ props }: WidgetProps) {
  const [p, setP] = useState(num(props, 'p', 100));
  const [gamma, setGamma] = useState(num(props, 'gamma', 0.25));
  const [spike, setSpike] = useState(num(props, 'spike', 0));
  const eig = useMemo(() => sampleCovEigs(p, gamma, spike), [p, gamma, spike]);
  const [lo, hi] = mpEdges(gamma);
  const xmax = Math.max(hi * 1.15, eig[0] * 1.08);
  const bins = 30;
  const w = (hi * 1.15 - 0) / bins;
  const counts = new Array(bins).fill(0);
  for (const e of eig) {
    const k = Math.floor(e / w);
    if (k >= 0 && k < bins) counts[k]++;
  }
  const hist = counts.map((c, k) => [(k + 0.5) * w, c / (p * w)] as [number, number]);
  const curve = Array.from({ length: 241 }, (_, i) => {
    const x = (xmax * i) / 240;
    return [x, mpDensity(x, gamma)] as [number, number];
  });
  const ymax = Math.max(...hist.map((h) => h[1]), ...curve.map((c) => c[1])) * 1.1 || 1;
  const n = Math.max(p, Math.round(p / gamma));
  const predicted = bbpOutlier(spike, gamma);
  return (
    <Frame
      title="Eigenvalues of a random sample covariance"
      caption={
        <>
          {n} samples of {p} independent features with variance 1, so every true eigenvalue is 1{spike > 0 ? ` (and ${fmt(1 + spike, 2)} along the planted direction)` : ''}. The sample eigenvalues
          spread from {fmt(eig[eig.length - 1], 3)} to {fmt(eig[0], 3)}; Marchenko-Pastur predicts the edges {fmt(lo, 3)} and {fmt(hi, 3)}.{' '}
          {spike > Math.sqrt(gamma)
            ? `The planted direction is strong enough to escape the bulk: predicted top eigenvalue ${fmt(predicted, 3)}.`
            : `A planted direction weaker than sqrt(gamma) = ${fmt(Math.sqrt(gamma), 3)} hides inside the bulk.`}
        </>
      }
    >
      <LinePlot
        label="Histogram of sample-covariance eigenvalues against the Marchenko-Pastur density"
        series={[
          { points: hist, cls: 'series-a', label: 'sample eigenvalues' },
          { points: curve, cls: 'series-c', label: 'Marchenko-Pastur', dashed: true },
        ]}
        xDomain={[0, xmax]}
        yDomain={[0, ymax]}
        xlabel="eigenvalue"
        ylabel="density"
      />
      <div className="widget-controls grid2">
        <Slider label="Features p" value={p} min={20} max={150} step={10} onChange={setP} format={(v) => String(v)} />
        <Slider label="Ratio gamma = p / n" value={gamma} min={0.05} max={1} step={0.05} onChange={setGamma} format={(v) => v.toFixed(2)} />
        <Slider label="Planted spike ell" value={spike} min={0} max={4} step={0.1} onChange={setSpike} format={(v) => v.toFixed(1)} />
      </div>
    </Frame>
  );
}
