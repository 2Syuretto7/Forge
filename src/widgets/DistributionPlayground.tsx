import { useMemo, useState } from 'react';
import { Frame, Select, Slider, gauss, num, rng, type WidgetProps, fmt } from './common';
import { LinePlot, scale, Axes } from './plot';

// Draw a sample from a distribution, compare its mean and variance with the theory
// (M22), and fit the parameter by maximum likelihood, with the log-likelihood curve
// (M25). Continuous distributions get a histogram with the true and fitted densities,
// discrete ones bars of observed frequencies with the true and fitted probabilities.

export type Dist = 'gaussian' | 'bernoulli' | 'exponential' | 'poisson';

export interface Params {
  mu: number;
  sigma: number;
  p: number;
  lam: number;
}

export function draw(dist: Dist, n: number, q: Params, seed: number): number[] {
  const r = rng(seed);
  return Array.from({ length: n }, () => {
    if (dist === 'gaussian') return q.mu + q.sigma * gauss(r);
    if (dist === 'bernoulli') return r() < q.p ? 1 : 0;
    if (dist === 'exponential') return -Math.log(1 - r()) / q.lam;
    // Poisson by counting unit-rate exponential arrivals before time lam.
    let k = 0;
    let t = -Math.log(1 - r());
    while (t < q.lam) {
      k += 1;
      t -= Math.log(1 - r());
    }
    return k;
  });
}

// The theoretical mean and variance.
export function theory(dist: Dist, q: Params) {
  if (dist === 'gaussian') return { mean: q.mu, variance: q.sigma * q.sigma };
  if (dist === 'bernoulli') return { mean: q.p, variance: q.p * (1 - q.p) };
  if (dist === 'exponential') return { mean: 1 / q.lam, variance: 1 / (q.lam * q.lam) };
  return { mean: q.lam, variance: q.lam };
}

export function sampleMoments(xs: number[]) {
  const n = xs.length;
  const mean = xs.reduce((a, b) => a + b, 0) / n;
  const ss = xs.reduce((a, b) => a + (b - mean) ** 2, 0);
  return { mean, mle: ss / n, unbiased: n > 1 ? ss / (n - 1) : 0 };
}

const logFact = (k: number) => {
  let s = 0;
  for (let i = 2; i <= k; i++) s += Math.log(i);
  return s;
};

// Log-likelihood of the location or rate parameter theta (mu, p or lam); for the
// Gaussian, sigma is held at its maximum-likelihood value.
export function logLik(dist: Dist, xs: number[], theta: number) {
  const n = xs.length;
  const { mean, mle } = sampleMoments(xs);
  const sum = mean * n;
  if (dist === 'gaussian') {
    const s2 = Math.max(mle, 1e-12);
    return xs.reduce((a, x) => a - 0.5 * Math.log(2 * Math.PI * s2) - (x - theta) ** 2 / (2 * s2), 0);
  }
  if (dist === 'bernoulli') return sum * Math.log(theta) + (n - sum) * Math.log(1 - theta);
  if (dist === 'exponential') return n * Math.log(theta) - theta * sum;
  return sum * Math.log(theta) - n * theta - xs.reduce((a, x) => a + logFact(x), 0);
}

// The maximum-likelihood estimate of theta.
export function mle(dist: Dist, xs: number[]) {
  const { mean } = sampleMoments(xs);
  if (dist === 'exponential') return 1 / Math.max(mean, 1e-12);
  if (dist === 'bernoulli') return Math.min(0.995, Math.max(0.005, mean));
  if (dist === 'poisson') return Math.max(mean, 1e-3);
  return mean;
}

const pmf = (dist: Dist, k: number, theta: number) =>
  dist === 'bernoulli' ? (k === 1 ? theta : 1 - theta) : Math.exp(k * Math.log(theta) - theta - logFact(k));

const pdf = (dist: Dist, x: number, theta: number, sigma: number) =>
  dist === 'gaussian' ? Math.exp(-((x - theta) ** 2) / (2 * sigma * sigma)) / (sigma * Math.sqrt(2 * Math.PI)) : x < 0 ? 0 : theta * Math.exp(-theta * x);

const LABELS: Record<Dist, string> = { gaussian: 'Gaussian', bernoulli: 'Bernoulli', exponential: 'Exponential', poisson: 'Poisson' };
const PARAM: Record<Dist, string> = { gaussian: 'mu (sigma fixed at its MLE)', bernoulli: 'p', exponential: 'rate lambda', poisson: 'lambda' };

export default function DistributionPlayground({ props }: WidgetProps) {
  const initial = props.dist as Dist;
  const [dist, setDist] = useState<Dist>(initial in LABELS ? initial : 'gaussian');
  const [n, setN] = useState(num(props, 'n', 20));
  const [mu, setMu] = useState(num(props, 'mu', 1));
  const [sigma, setSigma] = useState(num(props, 'sigma', 1.5));
  const [p, setP] = useState(num(props, 'p', 0.3));
  const [lam, setLam] = useState(num(props, 'lam', 2));
  const [seed, setSeed] = useState(1);
  const q: Params = { mu, sigma, p, lam };
  const xs = useMemo(() => draw(dist, n, { mu, sigma, p, lam }, seed), [dist, n, mu, sigma, p, lam, seed]);
  const m = sampleMoments(xs);
  const th = theory(dist, q);
  const trueTheta = dist === 'gaussian' ? mu : dist === 'bernoulli' ? p : lam;
  const hat = mle(dist, xs);
  const sHat = Math.sqrt(Math.max(m.mle, 1e-12));

  const [t0, t1] =
    dist === 'gaussian' ? [mu - 3 * sigma, mu + 3 * sigma] : dist === 'bernoulli' ? [0.005, 0.995] : [Math.max(0.02, 0.2 * trueTheta), 2.5 * trueTheta + 0.5];
  const curve: [number, number][] = Array.from({ length: 121 }, (_, i) => {
    const t = t0 + ((t1 - t0) * i) / 120;
    return [t, logLik(dist, xs, t)];
  });
  const llMax = logLik(dist, xs, hat);
  const yLo = Math.max(Math.min(...curve.map((c) => c[1])), llMax - 40);

  const W = 420;
  const H = 200;
  const pad = { l: 48, r: 12, t: 10, b: 34 };
  let hist: React.ReactNode;
  if (dist === 'gaussian' || dist === 'exponential') {
    const [lo, hi] = dist === 'gaussian' ? [mu - 4 * sigma, mu + 4 * sigma] : [0, 5 / lam];
    const bins = 20;
    const bw = (hi - lo) / bins;
    const counts = Array(bins).fill(0);
    for (const x of xs) {
      const b = Math.floor((x - lo) / bw);
      if (b >= 0 && b < bins) counts[b]++;
    }
    const dens = counts.map((c) => c / (xs.length * bw));
    const sTrue = sigma;
    const peak = dist === 'gaussian' ? Math.max(pdf(dist, mu, mu, sTrue), pdf(dist, hat, hat, sHat)) : Math.max(lam, hat);
    const ymax = Math.max(...dens, peak) * 1.1;
    const x = scale([lo, hi], [pad.l, W - pad.r]);
    const y = scale([0, ymax], [H - pad.b, pad.t]);
    const line = (theta: number, s: number) =>
      Array.from({ length: 101 }, (_, i) => {
        const v = lo + ((hi - lo) * i) / 100;
        return `${i ? 'L' : 'M'}${x(v)},${y(Math.min(pdf(dist, v, theta, s), ymax))}`;
      }).join(' ');
    hist = (
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Histogram of samples with true and fitted densities">
        <Axes x={x} y={y} width={W} height={H} pad={pad} xlabel="x" ylabel="density" />
        {dens.map((d, i) => (
          <rect key={i} x={x(lo + i * bw)} y={y(Math.min(d, ymax))} width={Math.max(0, x(lo + bw) - x(lo) - 1)} height={y(0) - y(Math.min(d, ymax))} className="hist" />
        ))}
        <path d={line(trueTheta, sTrue)} className="series-b" strokeDasharray="5 4" />
        <path d={line(hat, sHat)} className="series-c" />
      </svg>
    );
  } else {
    const K = dist === 'bernoulli' ? 1 : Math.max(4, Math.ceil(lam + 4 * Math.sqrt(lam)));
    const freq = Array.from({ length: K + 1 }, (_, k) => xs.filter((v) => v === k).length / xs.length);
    const ymax = Math.min(1, Math.max(...freq, ...freq.map((_, k) => pmf(dist, k, trueTheta))) * 1.15);
    const x = scale([-0.5, K + 0.5], [pad.l, W - pad.r]);
    const y = scale([0, ymax], [H - pad.b, pad.t]);
    const half = 0.32;
    hist = (
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Observed frequencies with true and fitted probabilities">
        <Axes x={x} y={y} width={W} height={H} pad={pad} xlabel="outcome" ylabel="frequency" />
        {freq.map((f, k) => (
          <g key={k}>
            <rect x={x(k - half)} width={x(k + half) - x(k - half)} y={y(f)} height={y(0) - y(f)} className="hist" />
            <line x1={x(k - half)} x2={x(k + half)} y1={y(pmf(dist, k, trueTheta))} y2={y(pmf(dist, k, trueTheta))} className="series-b" strokeDasharray="5 4" />
            <circle cx={x(k)} cy={y(pmf(dist, k, hat))} r={3} className="dot-c" />
          </g>
        ))}
      </svg>
    );
  }

  return (
    <Frame
      title="Sample a distribution, check its moments, fit it by maximum likelihood"
      caption={
        <>
          {n} draws from the {LABELS[dist].toLowerCase()}: sample mean {fmt(m.mean)} (theory {fmt(th.mean)}), sample variance {fmt(m.unbiased)} (theory{' '}
          {fmt(th.variance)}). The maximum-likelihood estimate of {PARAM[dist].split(' (')[0]} is {fmt(hat)}; the truth is {fmt(trueTheta)}. Dashed:
          the true {dist === 'gaussian' || dist === 'exponential' ? 'density' : 'probabilities'}; solid: the fit. The likelihood curve is flatter for
          small n, which is what an uncertain estimate looks like.
        </>
      }
    >
      <div className="widget-grid">
        {hist}
        <LinePlot
          label="Log-likelihood as a function of the parameter"
          series={[{ points: curve, cls: 'series-a', label: 'log-likelihood' }]}
          xDomain={[t0, t1]}
          yDomain={[yLo, llMax + 0.05 * Math.abs(llMax - yLo) + 1e-9]}
          xlabel={PARAM[dist]}
          ylabel="log L"
          height={200}
        >
          {(x, y) => <circle cx={x(hat)} cy={y(llMax)} r={4} className="marker" />}
        </LinePlot>
      </div>
      <div className="widget-controls">
        <Select label="Distribution" value={dist} options={(Object.keys(LABELS) as Dist[]).map((k) => ({ value: k, label: LABELS[k] }))} onChange={setDist} />
        <Slider label="Sample size n" value={n} min={2} max={2000} step={1} onChange={setN} format={(v) => String(v)} />
        {dist === 'gaussian' && (
          <>
            <Slider label="True mean" value={mu} min={-3} max={3} step={0.1} onChange={setMu} />
            <Slider label="True standard deviation" value={sigma} min={0.2} max={3} step={0.1} onChange={setSigma} />
          </>
        )}
        {dist === 'bernoulli' && <Slider label="True p" value={p} min={0.02} max={0.98} step={0.01} onChange={setP} />}
        {(dist === 'exponential' || dist === 'poisson') && <Slider label="True lambda" value={lam} min={0.2} max={10} step={0.1} onChange={setLam} />}
        <button className="btn small" onClick={() => setSeed((s) => s + 1)}>
          Draw a new sample
        </button>
      </div>
    </Frame>
  );
}
