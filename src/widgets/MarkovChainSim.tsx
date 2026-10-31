import { useMemo, useState } from 'react';
import { Frame, Slider, num, rng as makeRng, gauss, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// A Metropolis random walk on a two-peaked target (M32): propose x' = x + step * z, accept
// with probability min(1, p(x')/p(x)). The histogram of the chain approaches the target;
// the trace shows how it moves; the acceptance rate and the effective sample size say how
// well the step size suits the target.

export function logTarget(x: number, sep: number) {
  const a = -0.5 * (x + sep / 2) ** 2;
  const b = -0.5 * (x - sep / 2) ** 2;
  const m = Math.max(a, b);
  return m + Math.log(0.5 * Math.exp(a - m) + 0.5 * Math.exp(b - m));
}

export function metropolis(logp: (x: number) => number, x0: number, step: number, n: number, seed = 5) {
  const r = makeRng(seed);
  const xs = new Array<number>(n);
  let x = x0;
  let lx = logp(x);
  let acc = 0;
  for (let i = 0; i < n; i++) {
    const y = x + step * gauss(r);
    const ly = logp(y);
    if (Math.log(r()) < ly - lx) {
      x = y;
      lx = ly;
      acc++;
    }
    xs[i] = x;
  }
  return { xs, acceptance: acc / n };
}

export function autocorr(xs: number[], lag: number) {
  const n = xs.length;
  const m = xs.reduce((a, b) => a + b, 0) / n;
  let v = 0;
  for (const x of xs) v += (x - m) ** 2;
  let c = 0;
  for (let i = 0; i + lag < n; i++) c += (xs[i] - m) * (xs[i + lag] - m);
  return v > 0 ? c / v : 0;
}

// Effective sample size n / (1 + 2 sum rho_k), summing until the autocorrelation drops below 0.05.
export function ess(xs: number[], maxLag = 2000) {
  const n = xs.length;
  const m = xs.reduce((a, b) => a + b, 0) / n;
  const c = xs.map((x) => x - m);
  let v = 0;
  for (const x of c) v += x * x;
  if (v === 0) return 1;
  let s = 0;
  for (let k = 1; k < Math.min(maxLag, n - 1); k++) {
    let r = 0;
    for (let i = 0; i + k < n; i++) r += c[i] * c[i + k];
    r /= v;
    if (r < 0.05) break;
    s += r;
  }
  return n / (1 + 2 * s);
}

export default function MarkovChainSim({ props }: WidgetProps) {
  const [logStep, setLogStep] = useState(num(props, 'logstep', 0));
  const [sep, setSep] = useState(num(props, 'sep', 4));
  const [n, setN] = useState(num(props, 'n', 5000));
  const step = Math.pow(10, logStep);
  const run = useMemo(() => metropolis((x) => logTarget(x, sep), 0, step, n), [step, sep, n]);
  const effective = useMemo(() => ess(run.xs), [run]);
  const lo = -sep / 2 - 4;
  const hi = sep / 2 + 4;
  const bins = 40;
  const w = (hi - lo) / bins;
  const counts = new Array(bins).fill(0);
  for (const x of run.xs) {
    const k = Math.floor((x - lo) / w);
    if (k >= 0 && k < bins) counts[k]++;
  }
  const z = Math.sqrt(2 * Math.PI);
  const target = Array.from({ length: 161 }, (_, i) => {
    const x = lo + ((hi - lo) * i) / 160;
    return [x, Math.exp(logTarget(x, sep)) / z] as [number, number];
  });
  const hist = counts.map((c, k) => [lo + (k + 0.5) * w, c / (n * w)] as [number, number]);
  const ymax = Math.max(0.45, ...hist.map((h) => h[1])) * 1.1;
  const trace = run.xs.filter((_, i) => i % Math.max(1, Math.floor(n / 400)) === 0).map((x, i, arr) => [(i / arr.length) * n, x] as [number, number]);
  const right = run.xs.filter((x) => x > 0).length / n;
  return (
    <Frame
      title="A Metropolis random walk"
      caption={
        <>
          Step {fmt(step, 3)}: acceptance rate {fmt(100 * run.acceptance, 1)} percent, effective sample size about {fmt(effective, 0)} of {n}, and {fmt(100 * right, 1)} percent
          of the time in the right-hand peak (the target puts 50 percent there). Tiny steps are almost always accepted but crawl; huge steps are almost always rejected; in
          between the chain mixes, unless the peaks are so far apart that no step size crosses between them easily.
        </>
      }
    >
      <div className="widget-grid">
        <LinePlot
          label="Histogram of the chain against the target density"
          series={[
            { points: hist, cls: 'series-a', label: 'chain' },
            { points: target, cls: 'series-c', label: 'target', dashed: true },
          ]}
          xDomain={[lo, hi]}
          yDomain={[0, ymax]}
          xlabel="x"
          ylabel="density"
          height={200}
        />
        <LinePlot
          label="Trace of the chain against the step number"
          series={[{ points: trace, cls: 'series-b', label: 'trace' }]}
          xDomain={[0, n]}
          yDomain={[lo, hi]}
          xlabel="step"
          ylabel="x"
          height={200}
        />
      </div>
      <div className="widget-controls grid2">
        <Slider label="log10 proposal step" value={logStep} min={-2} max={1.5} step={0.05} onChange={setLogStep} format={(v) => `10^${v.toFixed(2)}`} />
        <Slider label="Distance between the peaks" value={sep} min={0} max={10} step={0.5} onChange={setSep} />
        <Slider label="Steps" value={n} min={500} max={20000} step={500} onChange={setN} format={(v) => String(v)} />
      </div>
    </Frame>
  );
}
