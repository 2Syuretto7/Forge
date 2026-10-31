import { useState } from 'react';
import { Frame, Slider, num, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// How likely is the average of n coin flips to miss its mean by at least eps (M31)? The
// exact binomial tail against three answers: Chebyshev's bound p(1-p)/(n eps^2),
// Hoeffding's bound 2 exp(-2 n eps^2), and the normal approximation of the central limit
// theorem. The bounds always hold; the approximation is closer but guarantees nothing.

// P(|K/n - p| >= eps) for K ~ Binomial(n, p), summed exactly in log space.
export function binomTail(n: number, p: number, eps: number) {
  let total = 0;
  let lc = 0; // log C(n, k), updated incrementally
  for (let k = 0; k <= n; k++) {
    if (k > 0) lc += Math.log((n - k + 1) / k);
    if (Math.abs(k / n - p) >= eps - 1e-12) total += Math.exp(lc + k * Math.log(p) + (n - k) * Math.log(1 - p));
  }
  return Math.min(1, total);
}

export const chebyshev = (n: number, p: number, eps: number) => Math.min(1, (p * (1 - p)) / (n * eps * eps));
export const hoeffding = (n: number, eps: number) => Math.min(1, 2 * Math.exp(-2 * n * eps * eps));

function erfc(x: number) {
  // Abramowitz and Stegun 7.1.26, accurate to about 1e-7.
  const t = 1 / (1 + 0.3275911 * Math.abs(x));
  const y = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429)))) * Math.exp(-x * x);
  return x >= 0 ? y : 2 - y;
}

export const normalApprox = (n: number, p: number, eps: number) => erfc((eps * Math.sqrt(n)) / Math.sqrt(2 * p * (1 - p)));

// Hoeffding's half-width at confidence 1 - delta.
export const hoeffdingEps = (n: number, delta: number) => Math.sqrt(Math.log(2 / delta) / (2 * n));

export default function ConcentrationMeter({ props }: WidgetProps) {
  const [p, setP] = useState(num(props, 'p', 0.9));
  const [eps, setEps] = useState(num(props, 'eps', 0.03));
  const [maxN, setMaxN] = useState(num(props, 'maxn', 2000));
  const ns = Array.from({ length: 40 }, (_, i) => Math.max(1, Math.round(Math.exp(Math.log(10) + (i / 39) * (Math.log(maxN) - Math.log(10))))));
  const floor = 1e-9;
  const pts = (f: (n: number) => number) => ns.map((n) => [n, Math.max(f(n), floor)] as [number, number]);
  const n1000 = Math.min(1000, maxN);
  return (
    <Frame
      title="Concentration of an average"
      caption={
        <>
          Chance that the average of n flips of a coin with p = {fmt(p, 2)} misses p by at least {fmt(eps, 3)}. At n = {n1000}: exact {binomTail(n1000, p, eps).toExponential(2)},
          normal approximation {normalApprox(n1000, p, eps).toExponential(2)}, Hoeffding bound {hoeffding(n1000, eps).toExponential(2)}, Chebyshev bound{' '}
          {chebyshev(n1000, p, eps).toExponential(2)}. With n = {n1000}, Hoeffding guarantees a miss of at most {fmt(hoeffdingEps(n1000, 0.05), 3)} with probability 0.95.
        </>
      }
    >
      <LinePlot
        label="Tail probability against sample size on log scales: exact, normal approximation, Hoeffding and Chebyshev"
        series={[
          { points: pts((n) => binomTail(n, p, eps)), cls: 'series-a', label: 'exact' },
          { points: pts((n) => normalApprox(n, p, eps)), cls: 'series-b', label: 'normal approximation', dashed: true },
          { points: pts((n) => hoeffding(n, eps)), cls: 'series-c', label: 'Hoeffding bound' },
          { points: pts((n) => chebyshev(n, p, eps)), cls: 'series-d', label: 'Chebyshev bound' },
        ]}
        xDomain={[10, maxN]}
        yDomain={[floor, 1.2]}
        xlog
        ylog
        xlabel="sample size n"
        ylabel="P(miss by at least eps)"
      />
      <div className="widget-controls grid2">
        <Slider label="Coin probability p" value={p} min={0.05} max={0.95} step={0.01} onChange={setP} />
        <Slider label="Tolerance eps" value={eps} min={0.005} max={0.2} step={0.005} onChange={setEps} format={(v) => v.toFixed(3)} />
        <Slider label="Largest n" value={maxN} min={100} max={5000} step={100} onChange={setMaxN} format={(v) => String(v)} />
      </div>
    </Frame>
  );
}
