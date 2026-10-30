import { useMemo, useState } from 'react';
import { Frame, Select, Slider, num, rng, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// The central limit theorem by simulation (M24). Average n draws of a distribution,
// many times, standardize the averages with the predicted mean and sigma / sqrt(n), and
// compare their histogram with the standard normal density. The Cauchy distribution
// has no variance, and its averages never settle.

export type Dist = 'die' | 'coin' | 'exponential' | 'skewed' | 'cauchy';

export const DISTS: Record<Dist, { label: string; draw: (r: () => number) => number; mean: number; sd: number }> = {
  die: { label: 'a fair die', draw: (r) => 1 + Math.floor(6 * r()), mean: 3.5, sd: Math.sqrt(35 / 12) },
  coin: { label: 'a coin with P(heads) = 0.1', draw: (r) => (r() < 0.1 ? 1 : 0), mean: 0.1, sd: Math.sqrt(0.09) },
  exponential: { label: 'exponential', draw: (r) => -Math.log(1 - r()), mean: 1, sd: 1 },
  skewed: { label: 'skewed: 10 with chance 0.05, else 0', draw: (r) => (r() < 0.05 ? 10 : 0), mean: 0.5, sd: Math.sqrt(100 * 0.05 * 0.95) },
  cauchy: { label: 'Cauchy (no variance)', draw: (r) => Math.tan(Math.PI * (r() - 0.5)), mean: 0, sd: 1 },
};

export function averages(dist: Dist, n: number, m: number, seed = 3): number[] {
  const r = rng(seed);
  const d = DISTS[dist];
  return Array.from({ length: m }, () => {
    let s = 0;
    for (let i = 0; i < n; i++) s += d.draw(r);
    return s / n;
  });
}

export function standardize(avgs: number[], dist: Dist, n: number) {
  const d = DISTS[dist];
  return avgs.map((a) => ((a - d.mean) * Math.sqrt(n)) / d.sd);
}

export function histogram(z: number[], lo: number, hi: number, bins: number) {
  const w = (hi - lo) / bins;
  const c = new Array(bins).fill(0);
  for (const v of z) {
    const k = Math.floor((v - lo) / w);
    if (k >= 0 && k < bins) c[k] += 1;
  }
  return c.map((k, i) => ({ x: lo + (i + 0.5) * w, density: k / (z.length * w) }));
}

export const normalPdf = (x: number) => Math.exp(-x * x / 2) / Math.sqrt(2 * Math.PI);

export default function CLTMachine({ props }: WidgetProps) {
  const [dist, setDist] = useState<Dist>((props.dist as Dist) in DISTS ? (props.dist as Dist) : 'die');
  const [n, setN] = useState(num(props, 'n', 1));
  const m = 4000;
  const avgs = useMemo(() => averages(dist, n, m), [dist, n]);
  const z = useMemo(() => standardize(avgs, dist, n), [avgs, dist, n]);
  const h = histogram(z, -4, 4, 32);
  const mean = avgs.reduce((a, b) => a + b, 0) / m;
  const sd = Math.sqrt(avgs.reduce((a, b) => a + (b - mean) ** 2, 0) / (m - 1));
  const d = DISTS[dist];
  const curve = Array.from({ length: 161 }, (_, i) => {
    const x = -4 + i / 20;
    return [x, normalPdf(x)] as [number, number];
  });
  return (
    <Frame
      title="Averages become bell curves"
      caption={
        dist === 'cauchy' ? (
          <>
            Averages of {n} Cauchy draws are again Cauchy: their spread does not shrink with n, and their histogram never approaches the bell curve. Sample
            standard deviation of the {m} averages: {fmt(sd, 2)}.
          </>
        ) : (
          <>
            {m} averages of {n} {n === 1 ? 'draw' : 'draws'} of {d.label}: their standard deviation is {fmt(sd, 4)}, against the predicted sigma / sqrt(n) = {fmt(d.sd / Math.sqrt(n), 4)}.
            Standardized, their histogram approaches the standard normal density as n grows, faster for symmetric distributions.
          </>
        )
      }
    >
      <LinePlot label="Histogram of standardized averages with the normal density" xDomain={[-4, 4]} yDomain={[0, 0.8]} xlabel="standardized average" ylabel="density" series={[{ points: curve, cls: 'series-c', label: 'standard normal' }]}>
        {(sx, sy) =>
          h.map((b, i) => (
            <rect key={i} x={sx(b.x - 0.125) + 0.5} width={Math.max(0, sx(b.x + 0.125) - sx(b.x - 0.125) - 1)} y={sy(Math.min(b.density, 0.8))} height={Math.max(0, sy(0) - sy(Math.min(b.density, 0.8)))} className="hist" />
          ))
        }
      </LinePlot>
      <div className="widget-controls grid2">
        <Slider label="Draws per average n" value={n} min={1} max={100} step={1} onChange={setN} format={(v) => String(v)} />
      </div>
      <div className="widget-controls">
        <Select<Dist> label="Distribution" value={dist} onChange={setDist} options={(Object.keys(DISTS) as Dist[]).map((k) => ({ value: k, label: DISTS[k].label }))} />
      </div>
    </Frame>
  );
}
