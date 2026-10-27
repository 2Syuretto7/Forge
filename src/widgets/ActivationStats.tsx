import { useMemo, useState } from 'react';
import { Frame, Select, Slider, Toggle, gauss, num, rng, type WidgetProps, fmt } from './common';
import { LinePlot, scale, Axes } from './plot';

type Init = 'small' | 'unit' | 'xavier' | 'he';
type Act = 'tanh' | 'relu';

interface Result {
  actStd: number[];
  gradStd: number[];
  acts: Float64Array[];
  grads: Float64Array[];
}

// Root mean square: the second moment is what variance-preserving
// initialization keeps constant (for post-ReLU values it differs from the std).
function rms(a: Float64Array) {
  let s = 0;
  for (const v of a) s += v * v;
  return Math.sqrt(s / a.length);
}

// Forward a batch through `depth` blocks and backpropagate a unit-variance
// gradient from the top. Matrices are width x width, row-major.
export function simulate(depth: number, width: number, init: Init, act: Act, norm: boolean, residual: boolean): Result {
  const B = 64;
  const r = rng(5);
  const scaleW = { small: 0.01, unit: 1, xavier: Math.sqrt(1 / width), he: Math.sqrt(2 / width) }[init];
  const Ws = Array.from({ length: depth }, () => Float64Array.from({ length: width * width }, () => scaleW * gauss(r)));
  const phi = (v: number) => (act === 'tanh' ? Math.tanh(v) : Math.max(0, v));
  const dphi = (v: number) => (act === 'tanh' ? 1 - Math.tanh(v) ** 2 : v > 0 ? 1 : 0);

  const hs: Float64Array[] = [Float64Array.from({ length: B * width }, () => gauss(r))];
  const pre: Float64Array[] = []; // input to the nonlinearity
  const nIn: Float64Array[] = []; // input to layer norm
  const nStats: { mu: Float64Array; sd: Float64Array }[] = [];
  for (let l = 0; l < depth; l++) {
    const h = hs[l];
    const W = Ws[l];
    // Plain block: h' = phi(LN(h W)). Residual block (pre-norm): h' = h + phi(LN(h)) W.
    const inN = residual ? h : matmul(h, W, B, width);
    const { out: z, mu, sd } = norm ? layerNorm(inN, B, width) : { out: inN, mu: new Float64Array(B), sd: new Float64Array(B).fill(1) };
    nIn.push(inN);
    nStats.push({ mu, sd });
    pre.push(z);
    const a = z.map(phi);
    hs.push(residual ? add(h, matmul(a, W, B, width)) : a);
  }
  const grads: Float64Array[] = Array(depth + 1);
  grads[depth] = Float64Array.from({ length: B * width }, () => gauss(r));
  for (let l = depth - 1; l >= 0; l--) {
    const gOut = grads[l + 1];
    const W = Ws[l];
    let gA: Float64Array;
    if (residual) gA = matmulT(gOut, W, B, width);
    else gA = gOut;
    const gZ = gA.map((g, i) => g * dphi(pre[l][i]));
    const gIn = norm ? layerNormBack(gZ, nIn[l], nStats[l], B, width) : gZ;
    grads[l] = residual ? add(gOut, gIn) : matmulT(gIn, W, B, width);
  }
  return { actStd: hs.map(rms), gradStd: grads.map(rms), acts: hs, grads };
}

function matmul(X: Float64Array, W: Float64Array, B: number, d: number) {
  const out = new Float64Array(B * d);
  for (let b = 0; b < B; b++)
    for (let k = 0; k < d; k++) {
      const x = X[b * d + k];
      if (x === 0) continue;
      for (let j = 0; j < d; j++) out[b * d + j] += x * W[k * d + j];
    }
  return out;
}
function matmulT(G: Float64Array, W: Float64Array, B: number, d: number) {
  const out = new Float64Array(B * d);
  for (let b = 0; b < B; b++)
    for (let k = 0; k < d; k++) {
      let s = 0;
      for (let j = 0; j < d; j++) s += G[b * d + j] * W[k * d + j];
      out[b * d + k] = s;
    }
  return out;
}
function add(a: Float64Array, b: Float64Array) {
  return a.map((v, i) => v + b[i]);
}
function layerNorm(X: Float64Array, B: number, d: number) {
  const out = new Float64Array(B * d);
  const mu = new Float64Array(B);
  const sd = new Float64Array(B);
  for (let b = 0; b < B; b++) {
    let m = 0;
    for (let j = 0; j < d; j++) m += X[b * d + j];
    m /= d;
    let v = 0;
    for (let j = 0; j < d; j++) v += (X[b * d + j] - m) ** 2;
    const s = Math.sqrt(v / d + 1e-5);
    mu[b] = m;
    sd[b] = s;
    for (let j = 0; j < d; j++) out[b * d + j] = (X[b * d + j] - m) / s;
  }
  return { out, mu, sd };
}
function layerNormBack(G: Float64Array, X: Float64Array, st: { mu: Float64Array; sd: Float64Array }, B: number, d: number) {
  const out = new Float64Array(B * d);
  for (let b = 0; b < B; b++) {
    let mg = 0;
    let mgx = 0;
    for (let j = 0; j < d; j++) {
      const xh = (X[b * d + j] - st.mu[b]) / st.sd[b];
      mg += G[b * d + j];
      mgx += G[b * d + j] * xh;
    }
    mg /= d;
    mgx /= d;
    for (let j = 0; j < d; j++) {
      const xh = (X[b * d + j] - st.mu[b]) / st.sd[b];
      out[b * d + j] = (G[b * d + j] - mg - xh * mgx) / st.sd[b];
    }
  }
  return out;
}

function Histogram({ data, label, cls }: { data: Float64Array; label: string; cls: string }) {
  const W = 200;
  const H = 110;
  const pad = { l: 30, r: 6, t: 6, b: 28 };
  const s = rms(data) || 1;
  const lim = 4 * s;
  const bins = 30;
  const counts = Array(bins).fill(0);
  for (const v of data) {
    const b = Math.floor(((v + lim) / (2 * lim)) * bins);
    if (b >= 0 && b < bins) counts[b]++;
  }
  const mx = Math.max(...counts, 1);
  const x = scale([-lim, lim], [pad.l, W - pad.r]);
  const y = scale([0, mx / data.length], [H - pad.b, pad.t]);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label={label}>
      <Axes x={x} y={y} width={W} height={H} pad={pad} xlabel={label} ylabel="" />
      {counts.map((c, i) => (
        <rect key={i} x={x(-lim + (i * 2 * lim) / bins)} width={(W - pad.l - pad.r) / bins - 1} y={y(c / data.length)} height={y(0) - y(c / data.length)} className={cls} />
      ))}
    </svg>
  );
}

export default function ActivationStats({ props }: WidgetProps) {
  const [depth, setDepth] = useState(num(props, 'depth', 20));
  const [init, setInit] = useState<Init>((props.init as Init) ?? 'small');
  const [act, setAct] = useState<Act>((props.act as Act) ?? 'tanh');
  const [norm, setNorm] = useState(props.norm === 'true');
  const [residual, setResidual] = useState(props.residual === 'true');
  const [layer, setLayer] = useState(Math.min(depth, 10));
  const width = 128;
  const res = useMemo(() => simulate(depth, width, init, act, norm, residual), [depth, init, act, norm, residual]);
  const L = Math.min(layer, depth);
  const pts = (a: number[]): [number, number][] => a.map((v, i) => [i, Math.max(v, 1e-12)]);
  const all = [...res.actStd, ...res.gradStd].filter((v) => v > 0 && Number.isFinite(v));
  return (
    <Frame
      title="Activation and gradient statistics through depth"
      caption={
        <>
          Root mean square of activations at the top layer: {fmt(res.actStd[depth])}; of the gradient reaching the input: {fmt(res.gradStd[0])}.
          Healthy networks keep both within an order of magnitude or two of 1 across all layers.
        </>
      }
    >
      <LinePlot
        label="Root mean square of activations and gradients by layer"
        series={[
          { points: pts(res.actStd), cls: 'series-a', label: 'activation RMS' },
          { points: pts(res.gradStd), cls: 'series-c', label: 'gradient RMS' },
        ]}
        xDomain={[0, depth]}
        yDomain={[Math.max(1e-12, Math.min(1e-2, ...all) / 2), Math.max(10, ...all) * 2]}
        ylog
        xlabel="layer"
        ylabel="root mean square"
        height={230}
      />
      <div className="widget-grid">
        <Histogram data={res.acts[L]} label={`activations, layer ${L}`} cls="hist" />
        <Histogram data={res.grads[L]} label={`gradients, layer ${L}`} cls="hist-b" />
      </div>
      <div className="widget-controls">
        <Select
          label="Initialization"
          value={init}
          options={[
            { value: 'small', label: 'N(0, 0.01^2)' },
            { value: 'unit', label: 'N(0, 1)' },
            { value: 'xavier', label: 'Xavier: N(0, 1/width)' },
            { value: 'he', label: 'He: N(0, 2/width)' },
          ]}
          onChange={setInit}
        />
        <Select
          label="Activation"
          value={act}
          options={[
            { value: 'tanh', label: 'tanh' },
            { value: 'relu', label: 'ReLU' },
          ]}
          onChange={setAct}
        />
        <Toggle label="Layer norm" checked={norm} onChange={setNorm} />
        <Toggle label="Residual connections (pre-norm)" checked={residual} onChange={setResidual} />
      </div>
      <div className="widget-controls grid2">
        <Slider label="Depth" value={depth} min={2} max={40} step={1} onChange={setDepth} format={(v) => String(v)} />
        <Slider label="Histogram layer" value={L} min={0} max={depth} step={1} onChange={setLayer} format={(v) => String(v)} />
      </div>
    </Frame>
  );
}
