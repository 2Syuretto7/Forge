import { useMemo, useState } from 'react';
import { Frame, Slider, num, rng as makeRng, gauss, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// A one-dimensional diffusion model run backwards (M37). Data from a two-component Gaussian
// mixture are noised by the Ornstein-Uhlenbeck process dx = -x dt + sqrt(2) dW, whose
// marginal at time t is again a mixture, with means m e^-t and variances s^2 e^-2t + 1 - e^-2t.
// Its score is known exactly, so the reverse-time SDE
//   dx = [-x - 2 d/dx log p_t(x)] dt + sqrt(2) dW,  run from t = T down to 0,
// turns standard normal noise back into the mixture. The widget shows the samples at any
// point of the reverse run against the exact marginal density at that time.

export const MIX = { w: [0.4, 0.6], m: [-2, 1.5], s: [0.4, 0.6] };

export function noisedParams(t: number) {
  const a = Math.exp(-t);
  return { w: MIX.w, m: MIX.m.map((m) => m * a), v: MIX.s.map((s) => s * s * a * a + 1 - a * a) };
}

export function density(x: number, t: number) {
  const { w, m, v } = noisedParams(t);
  return w.reduce((acc, wk, k) => acc + (wk * Math.exp(-((x - m[k]) ** 2) / (2 * v[k]))) / Math.sqrt(2 * Math.PI * v[k]), 0);
}

export function score(x: number, t: number) {
  const { w, m, v } = noisedParams(t);
  let num0 = 0;
  let den = 0;
  for (let k = 0; k < w.length; k++) {
    const p = (w[k] * Math.exp(-((x - m[k]) ** 2) / (2 * v[k]))) / Math.sqrt(v[k]);
    num0 += (p * -(x - m[k])) / v[k];
    den += p;
  }
  return den > 0 ? num0 / den : -x;
}

// Euler-Maruyama on the reverse SDE over a geometric time grid; returns the samples after
// each step, with the time each corresponds to.
export function reverseRun(n: number, steps: number, T: number, seed = 4, tmin = 1e-3) {
  const r = makeRng(seed);
  const ts = Array.from({ length: steps + 1 }, (_, i) => T * Math.pow(tmin / T, i / steps));
  let x = Array.from({ length: n }, () => gauss(r));
  const snaps: { t: number; x: number[] }[] = [{ t: T, x }];
  for (let i = 0; i < steps; i++) {
    const t = ts[i];
    const h = ts[i] - ts[i + 1];
    const c = Math.sqrt(2 * h);
    x = x.map((xi) => xi + h * (xi + 2 * score(xi, t)) + c * gauss(r));
    snaps.push({ t: ts[i + 1], x });
  }
  return snaps;
}

// One-dimensional Wasserstein distance between samples and the exact mixture at time t,
// through quantiles on a fine grid of the exact CDF.
export function w1ToMixture(xs: number[], t: number) {
  const sorted = [...xs].sort((a, b) => a - b);
  const lo = -8;
  const hi = 8;
  const N = 4000;
  const dx = (hi - lo) / N;
  let F = 0;
  const cdf: number[] = [];
  for (let i = 0; i < N; i++) {
    F += density(lo + (i + 0.5) * dx, t) * dx;
    cdf.push(F);
  }
  let j = 0;
  let total = 0;
  for (let i = 0; i < sorted.length; i++) {
    const q = (i + 0.5) / sorted.length;
    while (j < N - 1 && cdf[j] < q * F) j++;
    total += Math.abs(sorted[i] - (lo + (j + 0.5) * dx));
  }
  return total / sorted.length;
}

export default function DiffusionStepper({ props }: WidgetProps) {
  const [steps, setSteps] = useState(num(props, 'steps', 60));
  const [T, setT] = useState(num(props, 'T', 4));
  const [frac, setFrac] = useState(num(props, 'frac', 1));
  const snaps = useMemo(() => reverseRun(1500, steps, T), [steps, T]);
  const k = Math.round(frac * steps);
  const snap = snaps[k];
  const lo = -5;
  const hi = 5;
  const bins = 40;
  const bw = (hi - lo) / bins;
  const counts = new Array(bins).fill(0);
  for (const x of snap.x) {
    const b = Math.floor((x - lo) / bw);
    if (b >= 0 && b < bins) counts[b]++;
  }
  const hist = counts.map((c, b) => [lo + (b + 0.5) * bw, c / (snap.x.length * bw)] as [number, number]);
  const curve = Array.from({ length: 201 }, (_, i) => {
    const x = lo + ((hi - lo) * i) / 200;
    return [x, density(x, snap.t)] as [number, number];
  });
  const ymax = Math.max(...hist.map((h) => h[1]), ...curve.map((c) => c[1])) * 1.15;
  const w1 = useMemo(() => w1ToMixture(snap.x, snap.t), [snap]);
  return (
    <Frame
      title="Running the noise backwards"
      caption={
        <>
          Step {k} of {steps}, time t = {fmt(snap.t, 3)}: the histogram of 1,500 samples of the reverse process against the exact density of the noised data at that time
          (Wasserstein distance {fmt(w1, 3)}). At t = T the samples are pure noise; each step moves them along the score, the direction in which the noised density
          increases, plus fresh noise. Few steps or a short T leave visible errors.
        </>
      }
    >
      <LinePlot
        label="Histogram of reverse-process samples against the exact noised density"
        series={[
          { points: hist, cls: 'series-a', label: 'samples' },
          { points: curve, cls: 'series-c', label: 'exact density at time t', dashed: true },
        ]}
        xDomain={[lo, hi]}
        yDomain={[0, ymax]}
        xlabel="x"
        ylabel="density"
      />
      <div className="widget-controls grid2">
        <Slider label="Progress of the reverse run" value={frac} min={0} max={1} step={0.01} onChange={setFrac} format={(v) => `${Math.round(v * 100)}%`} />
        <Slider label="Steps" value={steps} min={5} max={200} step={5} onChange={setSteps} format={(v) => String(v)} />
        <Slider label="End time T of the noising" value={T} min={0.25} max={6} step={0.25} onChange={setT} />
      </div>
    </Frame>
  );
}
