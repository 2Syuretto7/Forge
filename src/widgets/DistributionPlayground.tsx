import { useMemo, useState } from 'react';
import { Frame, Select, Slider, gauss, num, rng, type WidgetProps, fmt } from './common';
import { LinePlot, scale, Axes } from './plot';

type Dist = 'gaussian' | 'bernoulli';

function sample(dist: Dist, n: number, mu: number, sigma: number, p: number, seed: number) {
  const r = rng(seed);
  return Array.from({ length: n }, () => (dist === 'gaussian' ? mu + sigma * gauss(r) : r() < p ? 1 : 0));
}

export default function DistributionPlayground({ props }: WidgetProps) {
  const [dist, setDist] = useState<Dist>((props.dist as Dist) === 'bernoulli' ? 'bernoulli' : 'gaussian');
  const [n, setN] = useState(num(props, 'n', 20));
  const [mu, setMu] = useState(num(props, 'mu', 1));
  const [sigma, setSigma] = useState(num(props, 'sigma', 1.5));
  const [p, setP] = useState(num(props, 'p', 0.3));
  const [seed, setSeed] = useState(1);
  const xs = useMemo(() => sample(dist, n, mu, sigma, p, seed), [dist, n, mu, sigma, p, seed]);

  const mean = xs.reduce((a, b) => a + b, 0) / xs.length;
  const mleVar = xs.reduce((a, b) => a + (b - mean) ** 2, 0) / xs.length;
  const mleSigma = Math.sqrt(Math.max(mleVar, 1e-12));

  // Log-likelihood as a function of the location parameter (mu, or p).
  const ll = (theta: number) => {
    if (dist === 'gaussian') {
      return xs.reduce((a, x) => a - 0.5 * Math.log(2 * Math.PI * mleSigma ** 2) - (x - theta) ** 2 / (2 * mleSigma ** 2), 0);
    }
    const k = xs.reduce((a, b) => a + b, 0);
    return k * Math.log(theta) + (xs.length - k) * Math.log(1 - theta);
  };
  const [t0, t1] = dist === 'gaussian' ? [mu - 3 * sigma, mu + 3 * sigma] : [0.005, 0.995];
  const curve: [number, number][] = Array.from({ length: 121 }, (_, i) => {
    const t = t0 + ((t1 - t0) * i) / 120;
    return [t, ll(t)];
  });
  const llMax = ll(dist === 'gaussian' ? mean : Math.min(0.995, Math.max(0.005, mean)));
  const yLo = Math.max(Math.min(...curve.map((c) => c[1])), llMax - 40);

  // Histogram with fitted density (Gaussian) or bar chart (Bernoulli).
  const W = 420;
  const H = 200;
  const pad = { l: 48, r: 12, t: 10, b: 34 };
  let hist: React.ReactNode;
  if (dist === 'gaussian') {
    const lo = mu - 4 * sigma;
    const hi = mu + 4 * sigma;
    const bins = 20;
    const bw = (hi - lo) / bins;
    const counts = Array(bins).fill(0);
    for (const x of xs) {
      const b = Math.floor((x - lo) / bw);
      if (b >= 0 && b < bins) counts[b]++;
    }
    const dens = counts.map((c) => c / (xs.length * bw));
    const pdf = (x: number, m: number, s: number) => Math.exp(-((x - m) ** 2) / (2 * s * s)) / (s * Math.sqrt(2 * Math.PI));
    const ymax = Math.max(...dens, pdf(mu, mu, sigma), pdf(mean, mean, mleSigma)) * 1.1;
    const x = scale([lo, hi], [pad.l, W - pad.r]);
    const y = scale([0, ymax], [H - pad.b, pad.t]);
    const line = (m: number, s: number) =>
      Array.from({ length: 101 }, (_, i) => {
        const v = lo + ((hi - lo) * i) / 100;
        return `${i ? 'L' : 'M'}${x(v)},${y(pdf(v, m, s))}`;
      }).join(' ');
    hist = (
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Histogram of samples with true and fitted densities">
        <Axes x={x} y={y} width={W} height={H} pad={pad} xlabel="x" ylabel="density" />
        {dens.map((d, i) => (
          <rect key={i} x={x(lo + i * bw)} y={y(d)} width={x(lo + bw) - x(lo) - 1} height={y(0) - y(d)} className="hist" />
        ))}
        <path d={line(mu, sigma)} className="series-b" strokeDasharray="5 4" />
        <path d={line(mean, mleSigma)} className="series-c" />
      </svg>
    );
  } else {
    const k = xs.reduce((a, b) => a + b, 0);
    const x = scale([-0.5, 1.5], [pad.l, W - pad.r]);
    const y = scale([0, 1], [H - pad.b, pad.t]);
    hist = (
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Observed frequencies of 0 and 1">
        <Axes x={x} y={y} width={W} height={H} pad={pad} xlabel="outcome" ylabel="frequency" />
        <rect x={x(-0.3)} width={x(0.3) - x(-0.3)} y={y(1 - k / n)} height={y(0) - y(1 - k / n)} className="hist" />
        <rect x={x(0.7)} width={x(1.3) - x(0.7)} y={y(k / n)} height={y(0) - y(k / n)} className="hist" />
        <line x1={x(0.7)} x2={x(1.3)} y1={y(p)} y2={y(p)} className="series-b" strokeDasharray="5 4" />
        <line x1={x(-0.3)} x2={x(0.3)} y1={y(1 - p)} y2={y(1 - p)} className="series-b" strokeDasharray="5 4" />
      </svg>
    );
  }

  return (
    <Frame
      title="Sample, fit by maximum likelihood, inspect the likelihood"
      caption={
        dist === 'gaussian' ? (
          <>
            MLE: mean {fmt(mean)}, standard deviation {fmt(mleSigma)} (divides by n). True: {fmt(mu)}, {fmt(sigma)}. With small n, the MLE standard
            deviation is biased low; the dashed curve is the truth, the solid curve the fit.
          </>
        ) : (
          <>
            MLE: p = {fmt(mean)} from {xs.reduce((a, b) => a + b, 0)} ones in {n} draws; true p = {fmt(p)}. The likelihood curve is flatter for
            small n, which is what an uncertain estimate looks like.
          </>
        )
      }
    >
      <div className="widget-grid">
        {hist}
        <LinePlot
          label="Log-likelihood as a function of the parameter"
          series={[{ points: curve, cls: 'series-a', label: 'log-likelihood' }]}
          xDomain={[t0, t1]}
          yDomain={[yLo, llMax + 0.05 * Math.abs(llMax - yLo) + 1e-9]}
          xlabel={dist === 'gaussian' ? 'mu (sigma fixed at its MLE)' : 'p'}
          ylabel="log L"
          height={200}
        >
          {(x, y) => <circle cx={x(dist === 'gaussian' ? mean : Math.min(0.995, Math.max(0.005, mean)))} cy={y(llMax)} r={4} className="marker" />}
        </LinePlot>
      </div>
      <div className="widget-controls">
        <Select
          label="Distribution"
          value={dist}
          options={[
            { value: 'gaussian', label: 'Gaussian' },
            { value: 'bernoulli', label: 'Bernoulli' },
          ]}
          onChange={setDist}
        />
        <Slider label="Sample size n" value={n} min={2} max={500} step={1} onChange={setN} format={(v) => String(v)} />
        {dist === 'gaussian' ? (
          <>
            <Slider label="True mean" value={mu} min={-3} max={3} step={0.1} onChange={setMu} />
            <Slider label="True standard deviation" value={sigma} min={0.2} max={3} step={0.1} onChange={setSigma} />
          </>
        ) : (
          <Slider label="True p" value={p} min={0.02} max={0.98} step={0.01} onChange={setP} />
        )}
        <button className="btn small" onClick={() => setSeed((s) => s + 1)}>
          Draw a new sample
        </button>
      </div>
    </Frame>
  );
}
