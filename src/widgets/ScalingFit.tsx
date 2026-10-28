import { useState } from 'react';
import { Frame, Select, Slider, gauss, rng, fmt, type WidgetProps } from './common';
import { LinePlot, path, type Series } from './plot';

// Parametric loss L(N, D) = E + A / N^alpha + B / D^beta, with the constants
// fitted by Hoffmann et al. (2022, "approach 3"). Compute is C = 6 N D.
export interface LossLaw {
  E: number;
  A: number;
  B: number;
  alpha: number;
  beta: number;
}
export const CHINCHILLA: LossLaw = { E: 1.69, A: 406.4, B: 410.7, alpha: 0.34, beta: 0.28 };

export const lossAt = (p: LossLaw, N: number, D: number) => p.E + p.A / N ** p.alpha + p.B / D ** p.beta;

// Minimizing L(N, C / 6N) over N: N* = G (C/6)^(beta/(alpha+beta)), D* = (C/6) / N*.
export function optimal(p: LossLaw, C: number) {
  const G = ((p.alpha * p.A) / (p.beta * p.B)) ** (1 / (p.alpha + p.beta));
  const N = G * (C / 6) ** (p.beta / (p.alpha + p.beta));
  const D = C / (6 * N);
  return { N, D, loss: lossAt(p, N, D) };
}

// On the frontier both reducible terms scale as (C/6)^-gamma, gamma = alpha beta / (alpha + beta),
// so L*(C) = E + K (C/6)^-gamma exactly.
export function frontier(p: LossLaw) {
  const G = ((p.alpha * p.A) / (p.beta * p.B)) ** (1 / (p.alpha + p.beta));
  return { E: p.E, K: p.A * G ** -p.alpha + p.B * G ** p.beta, gamma: (p.alpha * p.beta) / (p.alpha + p.beta) };
}

export function linfit(xs: number[], ys: number[]) {
  const n = xs.length;
  const mx = xs.reduce((a, b) => a + b, 0) / n;
  const my = ys.reduce((a, b) => a + b, 0) / n;
  let sxy = 0;
  let sxx = 0;
  for (let i = 0; i < n; i++) {
    sxy += (xs[i] - mx) * (ys[i] - my);
    sxx += (xs[i] - mx) ** 2;
  }
  const slope = sxy / sxx;
  const intercept = my - slope * mx;
  const sse = xs.reduce((s, x, i) => s + (ys[i] - intercept - slope * x) ** 2, 0);
  return { slope, intercept, sse };
}

export interface PowerFit {
  E: number;
  k: number;
  gamma: number;
}

// L = k C^-gamma: a straight line in log-log coordinates.
export function fitPower(pts: [number, number][]): PowerFit {
  const f = linfit(
    pts.map(([c]) => Math.log(c)),
    pts.map(([, l]) => Math.log(l)),
  );
  return { E: 0, k: Math.exp(f.intercept), gamma: -f.slope };
}

// L = E + k C^-gamma: for each floor E the rest is a log-log line; choose the E whose line fits best.
export function fitPowerFloor(pts: [number, number][]): PowerFit {
  const minL = Math.min(...pts.map(([, l]) => l));
  const sse = (E: number) =>
    linfit(
      pts.map(([c]) => Math.log(c)),
      pts.map(([, l]) => Math.log(l - E)),
    ).sse;
  const hi = minL * (1 - 1e-6);
  let best = 0;
  let bestS = Infinity;
  const grid = 200;
  for (let i = 0; i <= grid; i++) {
    const E = (hi * i) / grid;
    const s = sse(E);
    if (s < bestS) [best, bestS] = [E, s];
  }
  // Golden-section refinement around the best grid point.
  let a = Math.max(0, best - hi / grid);
  let b = Math.min(hi, best + hi / grid);
  const g = (Math.sqrt(5) - 1) / 2;
  for (let it = 0; it < 60; it++) {
    const c = b - g * (b - a);
    const d = a + g * (b - a);
    if (sse(c) < sse(d)) b = d;
    else a = c;
  }
  const E = (a + b) / 2;
  const f = linfit(
    pts.map(([c]) => Math.log(c)),
    pts.map(([, l]) => Math.log(l - E)),
  );
  return { E, k: Math.exp(f.intercept), gamma: -f.slope };
}

export const predict = (f: PowerFit, C: number) => f.E + f.k * C ** -f.gamma;

// Compute-optimal runs between 10^lo and 10^hi FLOPs, with relative noise on the loss.
export function sampleRuns(p: LossLaw, lo: number, hi: number, count: number, noise: number, seed = 7): [number, number][] {
  const r = rng(seed);
  return Array.from({ length: count }, (_, i) => {
    const C = 10 ** (lo + ((hi - lo) * i) / (count - 1));
    return [C, optimal(p, C).loss * (1 + noise * gauss(r))];
  });
}

const SIZES = [1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11];
const XS: [number, number] = [1e17, 1e25];
const grid = (n: number) => Array.from({ length: n }, (_, i) => 10 ** (17 + (8 * i) / (n - 1)));
const big = (v: number) => {
  for (const [s, u] of [
    [1e12, 'T'],
    [1e9, 'B'],
    [1e6, 'M'],
  ] as const)
    if (v >= s) return `${(v / s).toPrecision(3)}${u}`;
  return v.toPrecision(3);
};

export default function ScalingFit({ props }: WidgetProps) {
  const [alpha, setAlpha] = useState(CHINCHILLA.alpha);
  const [beta, setBeta] = useState(CHINCHILLA.beta);
  const [lo, setLo] = useState(Number(props.lo) || 18);
  const [hi, setHi] = useState(Number(props.hi) || 21);
  const [target, setTarget] = useState(Number(props.target) || 24);
  const [mode, setMode] = useState<'floor' | 'pure'>(props.fit === 'floor' ? 'floor' : 'pure');
  const [noise, setNoise] = useState(0.005);
  const law: LossLaw = { ...CHINCHILLA, alpha, beta };
  const top = Math.max(hi, lo + 0.5);
  const runs = sampleRuns(law, lo, top, 8, noise);
  const fit = mode === 'floor' ? fitPowerFloor(runs) : fitPower(runs);
  const C = 10 ** target;
  const opt = optimal(law, C);
  const pred = predict(fit, C);
  const err = (pred - opt.loss) / opt.loss;
  const series: Series[] = [
    { points: grid(161).map((c) => [c, optimal(law, c).loss]), cls: 'series-a', label: 'compute-optimal frontier' },
    { points: grid(161).map((c) => [c, predict(fit, c)]), cls: 'series-c', label: mode === 'floor' ? 'fit E + k C^-γ' : 'fit k C^-γ', dashed: true },
  ];
  const a = beta / (alpha + beta);
  return (
    <Frame
      title="Scaling laws: fit the frontier, then extrapolate"
      caption={
        <>
          Faint curves: one model size each, trained on more and more tokens (left to right, 10M to 100B parameters). Their lower envelope is the
          compute-optimal frontier. Dots: eight compute-optimal runs you can afford; the dashed fit through them is extrapolated to the target budget.
        </>
      }
    >
      <LinePlot
        series={series}
        xDomain={XS}
        yDomain={[1.5, 6]}
        xlog
        xlabel="training compute C = 6ND (FLOPs)"
        ylabel="loss (nats per token)"
        label="Loss against compute for fixed model sizes, the compute-optimal frontier and a power-law fit"
      >
        {(x, y) => (
          <g>
            {SIZES.map((N) => (
              <path
                key={N}
                d={path(
                  grid(121).map((c) => [c, lossAt(law, N, c / (6 * N))]),
                  x,
                  y,
                )}
                className="iso-curve"
              />
            ))}
            <rect x={x(10 ** lo)} y={y(6)} width={x(10 ** top) - x(10 ** lo)} height={y(1.5) - y(6)} className="fit-band" />
            {runs.map(([c, l], i) => (
              <circle key={i} cx={x(c)} cy={y(l)} r={3.5} className="dot-b" />
            ))}
            <line x1={x(C)} x2={x(C)} y1={y(1.5)} y2={y(6)} className="grid-line" strokeDasharray="3 3" />
            <circle cx={x(C)} cy={y(opt.loss)} r={4} className="dot-a" />
            <circle cx={x(C)} cy={y(pred)} r={4} className="dot-c" />
          </g>
        )}
      </LinePlot>
      <div className="widget-stats" aria-live="polite">
        <span>
          budget {C.toExponential(0)} FLOPs: N* = {big(opt.N)}, D* = {big(opt.D)} tokens ({fmt(opt.D / opt.N, 1)} tokens per parameter)
        </span>
        <span>
          true loss {fmt(opt.loss, 3)}, predicted {fmt(pred, 3)} ({err >= 0 ? '+' : ''}
          {fmt(100 * err, 1)}%)
        </span>
        <span>
          fit: {mode === 'floor' ? `E = ${fmt(fit.E, 2)}, ` : ''}γ = {fmt(fit.gamma, 3)} (true E = {CHINCHILLA.E}, γ = {fmt(frontier(law).gamma, 3)})
        </span>
        <span>
          N* ∝ C^{fmt(a, 2)}, D* ∝ C^{fmt(1 - a, 2)}
        </span>
      </div>
      <div className="widget-controls grid2">
        <Slider label="Smallest run (log10 FLOPs)" value={lo} min={17} max={23} step={0.5} onChange={setLo} format={(v) => `1e${v}`} />
        <Slider label="Largest run (log10 FLOPs)" value={hi} min={17.5} max={24} step={0.5} onChange={setHi} format={(v) => `1e${Math.max(v, lo + 0.5)}`} />
        <Slider label="Target budget (log10 FLOPs)" value={target} min={18} max={25} step={0.5} onChange={setTarget} format={(v) => `1e${v}`} />
        <Select
          label="Fitted form"
          value={mode}
          options={[
            { value: 'pure', label: 'k C^-γ' },
            { value: 'floor', label: 'E + k C^-γ' },
          ]}
          onChange={setMode}
        />
        <Slider label="Parameter exponent α" value={alpha} min={0.2} max={0.5} step={0.01} onChange={setAlpha} />
        <Slider label="Data exponent β" value={beta} min={0.2} max={0.5} step={0.01} onChange={setBeta} />
        <Slider label="Run-to-run noise" value={noise} min={0} max={0.03} step={0.0025} onChange={setNoise} format={(v) => `${(100 * v).toFixed(2)}%`} />
      </div>
    </Frame>
  );
}
