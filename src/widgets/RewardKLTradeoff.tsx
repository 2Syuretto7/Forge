import { useState } from 'react';
import { Frame, Select, Slider, fmt, type WidgetProps } from './common';
import { LinePlot, type Series } from './plot';

// A toy prompt with eight candidate responses: the reference policy's probabilities, the reward a
// learned reward model gives (proxy) and the reward a careful judge would give (true).
export interface Response {
  label: string;
  ref: number;
  proxy: number;
  truth: number;
}

export const RESPONSES: Response[] = [
  { label: 'correct and concise', ref: 0.12, proxy: 0.8, truth: 1.0 },
  { label: 'correct, verbose', ref: 0.18, proxy: 0.9, truth: 0.8 },
  { label: 'partly correct', ref: 0.2, proxy: 0.4, truth: 0.4 },
  { label: 'wrong but confident', ref: 0.15, proxy: 0.3, truth: -0.5 },
  { label: 'off topic', ref: 0.15, proxy: -0.5, truth: -0.6 },
  { label: 'refuses', ref: 0.1, proxy: -0.2, truth: -0.3 },
  { label: 'flatters the user, wrong', ref: 0.06, proxy: 1.6, truth: -0.8 },
  { label: 'repeats the question', ref: 0.04, proxy: -1.0, truth: -1.0 },
];

// The KL-regularized objective E[r] - beta KL(pi || pi_ref) is maximized by
// pi*(y) = pi_ref(y) exp(r(y) / beta) / Z.
export function optimalPolicy(ref: number[], reward: number[], beta: number) {
  const logits = ref.map((p, i) => Math.log(p) + reward[i] / beta);
  const m = Math.max(...logits);
  const w = logits.map((l) => Math.exp(l - m));
  const z = w.reduce((s, v) => s + v, 0);
  return w.map((v) => v / z);
}

export const kl = (p: number[], q: number[]) => p.reduce((s, pi, i) => (pi > 0 ? s + pi * Math.log(pi / q[i]) : s), 0);
export const expect = (p: number[], r: number[]) => p.reduce((s, pi, i) => s + pi * r[i], 0);

// DPO's implicit reward: beta log(pi / pi_ref) equals the reward up to a constant (beta log Z).
export const implicitReward = (pi: number[], ref: number[], beta: number) => pi.map((p, i) => beta * Math.log(p / ref[i]));

const BETAS = Array.from({ length: 81 }, (_, i) => 10 ** (1 - (3 * i) / 80));

export default function RewardKLTradeoff({ props }: WidgetProps) {
  const [logBeta, setLogBeta] = useState(Number(props.logBeta) || 0);
  const [optimize, setOptimize] = useState<'proxy' | 'truth'>(props.reward === 'truth' ? 'truth' : 'proxy');
  const beta = 10 ** logBeta;
  const ref = RESPONSES.map((r) => r.ref);
  const target = RESPONSES.map((r) => (optimize === 'proxy' ? r.proxy : r.truth));
  const proxy = RESPONSES.map((r) => r.proxy);
  const truth = RESPONSES.map((r) => r.truth);
  const pts = BETAS.map((b) => {
    const p = optimalPolicy(ref, target, b);
    return { kl: kl(p, ref), proxy: expect(p, proxy), truth: expect(p, truth) };
  });
  const pi = optimalPolicy(ref, target, beta);
  const cur = { kl: kl(pi, ref), proxy: expect(pi, proxy), truth: expect(pi, truth) };
  const maxKl = Math.max(...pts.map((p) => p.kl)) * 1.05 || 1;
  const series: Series[] = [
    { points: pts.map((p) => [p.kl, p.proxy]), cls: 'series-a', label: 'reward-model score' },
    { points: pts.map((p) => [p.kl, p.truth]), cls: 'series-b', label: 'true quality' },
  ];
  return (
    <Frame
      title="Reward against KL: what the policy gains as it leaves the reference"
      caption={
        <>
          The exact optimum of reward minus beta times KL to the reference, for one toy prompt with eight possible responses. Lowering beta lets
          the policy move further from the reference. Optimizing the reward model's score past a point trades true quality for a higher score.
        </>
      }
    >
      <LinePlot
        series={series}
        xDomain={[0, maxKl]}
        yDomain={[-1, 1.7]}
        xlabel="KL(policy || reference) in nats"
        ylabel="expected reward"
        label="Expected proxy and true reward against KL from the reference policy"
      >
        {(x, y) => (
          <g>
            <circle cx={x(cur.kl)} cy={y(cur.proxy)} r={4.5} className="dot-a" />
            <circle cx={x(cur.kl)} cy={y(cur.truth)} r={4.5} className="dot-b" />
          </g>
        )}
      </LinePlot>
      <table className="widget-table">
        <thead>
          <tr>
            <th>response</th>
            <th>reference</th>
            <th>policy</th>
            <th>score</th>
            <th>true</th>
          </tr>
        </thead>
        <tbody>
          {RESPONSES.map((r, i) => (
            <tr key={r.label}>
              <td>{r.label}</td>
              <td>{fmt(r.ref, 2)}</td>
              <td>{fmt(pi[i], 2)}</td>
              <td>{fmt(r.proxy, 1)}</td>
              <td>{fmt(r.truth, 1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="widget-stats" aria-live="polite">
        <span>
          beta {fmt(beta, 3)}: KL {fmt(cur.kl, 3)} nats, score {fmt(cur.proxy, 3)}, true quality {fmt(cur.truth, 3)}
        </span>
      </div>
      <div className="widget-controls grid2">
        <Slider label="KL weight beta (log10)" value={logBeta} min={-2} max={1} step={0.05} onChange={setLogBeta} format={(v) => fmt(10 ** v, 3)} />
        <Select
          label="Optimize"
          value={optimize}
          options={[
            { value: 'proxy', label: 'the reward model' },
            { value: 'truth', label: 'the true reward' },
          ]}
          onChange={setOptimize}
        />
      </div>
    </Frame>
  );
}
