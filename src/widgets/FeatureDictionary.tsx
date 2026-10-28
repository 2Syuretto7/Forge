import { useMemo, useState } from 'react';
import { Frame, Slider, fmt, gauss, rng, type WidgetProps } from './common';

// Toy activations in superposition: n sparse features stored as unit directions in 2D, more
// features than dimensions. Each sample activates each feature independently with probability p,
// with a magnitude uniform in [0, 1].
export function featureDirections(n: number): [number, number][] {
  return Array.from({ length: n }, (_, i) => [Math.cos((2 * Math.PI * i) / n), Math.sin((2 * Math.PI * i) / n)]);
}

export function sampleActivations(n: number, p: number, count: number, seed: number): [number, number][] {
  const r = rng(seed);
  const dirs = featureDirections(n);
  return Array.from({ length: count }, () => {
    let x = 0;
    let y = 0;
    for (const [dx, dy] of dirs) {
      if (r() < p) {
        const a = r();
        x += a * dx;
        y += a * dy;
      }
    }
    return [x, y] as [number, number];
  });
}

export interface Sae {
  We: number[][]; // m x 2 encoder
  be: number[];
  Wd: number[][]; // m x 2 decoder directions (unit length)
  bd: [number, number];
}

export function encode(s: Sae, x: [number, number]) {
  const u = [x[0] - s.bd[0], x[1] - s.bd[1]];
  return s.We.map((w, j) => Math.max(0, w[0] * u[0] + w[1] * u[1] + s.be[j]));
}

export function decode(s: Sae, z: number[]): [number, number] {
  let a = s.bd[0];
  let b = s.bd[1];
  z.forEach((v, j) => {
    a += v * s.Wd[j][0];
    b += v * s.Wd[j][1];
  });
  return [a, b];
}

const unit = (v: number[]) => {
  const n = Math.hypot(v[0], v[1]) || 1;
  return [v[0] / n, v[1] / n];
};

// Train min E |x - decode(encode(x))|^2 + l1 * sum(z) with Adam on minibatches, renormalizing the
// decoder directions to unit length after every step so the L1 penalty cannot be dodged by
// shrinking z and growing the decoder. Every `resample` steps (in the first two thirds of training),
// latents that never fired are re-initialized toward the worst-reconstructed input of a batch, the
// resampling of dead latents used by Bricken et al. (2023).
export function trainSae(data: [number, number][], m: number, l1: number, steps: number, seed: number, lr = 0.01, resample = 250): Sae {
  const r = rng(seed);
  const init = Array.from({ length: m }, () => unit([gauss(r), gauss(r)]));
  const s: Sae = { We: init.map((d) => [d[0], d[1]]), be: Array(m).fill(0), Wd: init.map((d) => [d[0], d[1]]), bd: [0, 0] };
  const nP = m * 2 + m + m * 2 + 2;
  const mom = new Float64Array(nP);
  const vel = new Float64Array(nP);
  const B = 32;
  let fired = new Array(m).fill(false);
  for (let t = 1; t <= steps; t++) {
    if (t % resample === 0 && t < (2 * steps) / 3) {
      for (let j = 0; j < m; j++) {
        if (fired[j]) continue;
        let worst: [number, number] = data[0];
        let worstErr = -1;
        for (let k = 0; k < 64; k++) {
          const x = data[Math.floor(r() * data.length)];
          const xh = decode(s, encode(s, x));
          const err = (xh[0] - x[0]) ** 2 + (xh[1] - x[1]) ** 2;
          if (err > worstErr) [worst, worstErr] = [x, err];
        }
        const d = unit([worst[0] - s.bd[0] + 1e-6, worst[1] - s.bd[1]]);
        s.Wd[j] = d;
        s.We[j] = [0.2 * d[0], 0.2 * d[1]];
        s.be[j] = 0;
        for (const i of [j * 2, j * 2 + 1, 2 * m + j, 3 * m + j * 2, 3 * m + j * 2 + 1]) mom[i] = vel[i] = 0;
      }
      fired = new Array(m).fill(false);
    }
    const g = new Float64Array(nP);
    for (let k = 0; k < B; k++) {
      const x = data[Math.floor(r() * data.length)];
      const u = [x[0] - s.bd[0], x[1] - s.bd[1]];
      const pre = s.We.map((w, j) => w[0] * u[0] + w[1] * u[1] + s.be[j]);
      const z = pre.map((v) => Math.max(0, v));
      z.forEach((v, j) => {
        if (v > 0) fired[j] = true;
      });
      const xh = decode(s, z);
      const e = [xh[0] - x[0], xh[1] - x[1]];
      // d/dbd through the decoder output (+1) and through the encoder input (-1).
      for (let j = 0; j < m; j++) {
        const dz = 2 * (e[0] * s.Wd[j][0] + e[1] * s.Wd[j][1]) + l1;
        const dpre = pre[j] > 0 ? dz : 0;
        g[j * 2] += dpre * u[0];
        g[j * 2 + 1] += dpre * u[1];
        g[2 * m + j] += dpre;
        g[3 * m + j * 2] += 2 * e[0] * z[j];
        g[3 * m + j * 2 + 1] += 2 * e[1] * z[j];
        g[5 * m] -= dpre * s.We[j][0];
        g[5 * m + 1] -= dpre * s.We[j][1];
      }
      g[5 * m] += 2 * e[0];
      g[5 * m + 1] += 2 * e[1];
    }
    const flat = [...s.We.flat(), ...s.be, ...s.Wd.flat(), ...s.bd];
    for (let i = 0; i < nP; i++) {
      const gi = g[i] / B;
      mom[i] = 0.9 * mom[i] + 0.1 * gi;
      vel[i] = 0.999 * vel[i] + 0.001 * gi * gi;
      flat[i] -= (lr * (mom[i] / (1 - 0.9 ** t))) / (Math.sqrt(vel[i] / (1 - 0.999 ** t)) + 1e-8);
    }
    for (let j = 0; j < m; j++) {
      s.We[j] = [flat[j * 2], flat[j * 2 + 1]];
      s.be[j] = flat[2 * m + j];
      s.Wd[j] = unit([flat[3 * m + j * 2], flat[3 * m + j * 2 + 1]]);
    }
    s.bd = [flat[5 * m], flat[5 * m + 1]];
  }
  return s;
}

export function evaluateSae(s: Sae, data: [number, number][], n: number) {
  let mse = 0;
  let l0 = 0;
  for (const x of data) {
    const z = encode(s, x);
    const xh = decode(s, z);
    mse += (xh[0] - x[0]) ** 2 + (xh[1] - x[1]) ** 2;
    l0 += z.filter((v) => v > 1e-9).length;
  }
  const dirs = featureDirections(n);
  const alive = s.Wd.filter((_, j) => data.some((x) => encode(s, x)[j] > 1e-9));
  const recovered = dirs.map((d) => Math.max(0, ...alive.map((w) => w[0] * d[0] + w[1] * d[1])));
  return { mse: mse / data.length, l0: l0 / data.length, recovered, alive: alive.length };
}

const W = 300;
const S = 110;

export default function FeatureDictionary({ props }: WidgetProps) {
  const [n, setN] = useState(Number(props.features) || 4);
  const [p, setP] = useState(0.15);
  const [m, setM] = useState(Number(props.latents) || 8);
  const [logL1, setLogL1] = useState(-1.5);
  const data = useMemo(() => sampleActivations(n, p, 600, 11), [n, p]);
  const sae = useMemo(() => trainSae(data, m, 10 ** logL1, 1500, 5), [data, m, logL1]);
  const ev = evaluateSae(sae, data, n);
  const dirs = featureDirections(n);
  const sx = (v: number) => W / 2 + v * S;
  const sy = (v: number) => W / 2 - v * S;
  const found = ev.recovered.filter((c) => c > 0.95).length;
  return (
    <Frame
      title="A sparse autoencoder finds the features in superposition"
      caption={
        <>
          Points: 600 activations made of {n} sparse features squeezed into 2 dimensions (dashed: the true directions). Solid arrows: the directions
          of the sparse autoencoder's latents that ever fire, trained here in your browser. With enough sparsity the latents line up with the
          features even though no single coordinate does. Squeeze five or six features into two dimensions and some latents settle between
          neighbouring features instead: the dictionary is only as good as the features are sparse and separated.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${W}`} className="widget-svg" role="img" aria-label={`Activations with ${n} true feature directions and ${ev.alive} learned latent directions`}>
        <line x1={0} x2={W} y1={W / 2} y2={W / 2} className="grid-line" />
        <line x1={W / 2} x2={W / 2} y1={0} y2={W} className="grid-line" />
        {data.map(([x, y], i) => (
          <circle key={i} cx={sx(x)} cy={sy(y)} r={1.6} className="hist" />
        ))}
        {dirs.map(([x, y], i) => (
          <line key={'t' + i} x1={sx(0)} y1={sy(0)} x2={sx(x * 1.2)} y2={sy(y * 1.2)} className="ref-curve" />
        ))}
        {sae.Wd.map(([x, y], j) =>
          data.some((d) => encode(sae, d)[j] > 1e-9) ? (
            <line key={'w' + j} x1={sx(sae.bd[0])} y1={sy(sae.bd[1])} x2={sx(sae.bd[0] + x)} y2={sy(sae.bd[1] + y)} className="main-curve" />
          ) : null,
        )}
      </svg>
      <div className="widget-stats" aria-live="polite">
        <span>
          {found} of {n} features recovered (cosine above 0.95); {ev.alive} of {m} latents ever fire
        </span>
        <span>
          reconstruction error {fmt(ev.mse, 4)}; on average {fmt(ev.l0, 2)} latents active per input
        </span>
      </div>
      <div className="widget-controls grid2">
        <Slider label="True features" value={n} min={3} max={6} step={1} onChange={setN} format={(v) => String(v)} />
        <Slider label="Feature probability" value={p} min={0.05} max={0.6} step={0.05} onChange={setP} format={(v) => v.toFixed(2)} />
        <Slider label="Latents" value={m} min={2} max={12} step={1} onChange={setM} format={(v) => String(v)} />
        <Slider label="L1 penalty (log10)" value={logL1} min={-3} max={0} step={0.25} onChange={setLogL1} format={(v) => fmt(10 ** v, 3)} />
      </div>
    </Frame>
  );
}
