import { useState } from 'react';
import { Frame, Select, Slider, Toggle, fmt, type WidgetProps } from './common';
import { LinePlot, type Series } from './plot';
import logged from './data/spike_runs.json';

// Logs written by scripts/gen_spike_runs.py: real training runs of a small character-level GPT,
// one value per optimizer step.
export interface RunLog {
  label: string;
  note: string;
  loss: number[];
  gradNorm: number[];
  lr: number[];
  maxLogit: number[];
  val: [number, number][];
}
export interface SpikeLogs {
  checkpointEvery: number;
  model: string;
  runs: Record<string, RunLog>;
}
export const LOGS = logged as unknown as SpikeLogs;

// Steps (1-based) whose loss exceeds the mean of the previous `window` losses by more than k of
// their standard deviations.
export function detectSpikes(loss: number[], window: number, k: number): number[] {
  const out: number[] = [];
  let sum = 0;
  let sq = 0;
  for (let i = 0; i < loss.length; i++) {
    if (i >= window) {
      const mean = sum / window;
      const sd = Math.sqrt(Math.max(0, sq / window - mean * mean));
      if (!Number.isFinite(loss[i]) || loss[i] > mean + k * sd) out.push(i + 1);
    }
    sum += loss[i];
    sq += loss[i] * loss[i];
    if (i >= window) {
      sum -= loss[i - window];
      sq -= loss[i - window] ** 2;
    }
  }
  return out;
}

// The loss logged at step s is measured before update s, so a flagged step s means update s - 1 may
// already be damaged: roll back to the last checkpoint saved before it.
export const rollbackPoint = (flagged: number, every: number) => Math.floor((flagged - 2) / every) * every;

export function ema(xs: number[], beta: number) {
  let m = xs[0];
  return xs.map((x, i) => (i === 0 ? x : (m = beta * m + (1 - beta) * x)));
}

const METRICS = {
  gradNorm: { label: 'gradient norm before clipping', log: true },
  maxLogit: { label: 'largest attention logit', log: true },
  lr: { label: 'learning rate', log: false },
} as const;
type MetricId = keyof typeof METRICS;

const pts = (ys: number[], cap = Infinity): [number, number][] => ys.map((y, i) => [i + 1, Math.min(y, cap)]);
const finiteMax = (ys: number[]) => ys.reduce((m, y) => (Number.isFinite(y) && y > m ? y : m), 0);
const finiteMin = (ys: number[]) => ys.reduce((m, y) => (Number.isFinite(y) && y > 0 && y < m ? y : m), Infinity);

export default function LossSpikeExplorer({ props }: WidgetProps) {
  const ids = Object.keys(LOGS.runs);
  const [a, setA] = useState<string>(props.run in LOGS.runs ? props.run : 'bad_data');
  const [b, setB] = useState<string>(props.compare in LOGS.runs ? props.compare : 'healthy');
  const [metric, setMetric] = useState<MetricId>('gradNorm');
  const [window, setWindow] = useState(50);
  const [k, setK] = useState(5);
  const [smooth, setSmooth] = useState(false);
  const runA = LOGS.runs[a];
  const runB = b === 'none' ? null : LOGS.runs[b];
  const steps = Math.max(runA.loss.length, runB?.loss.length ?? 0);
  const [cursor, setCursor] = useState(Math.min(Number(props.step) || Math.round(steps / 2), steps));
  const cur = Math.min(cursor, steps);
  const show = (ys: number[]) => (smooth ? ema(ys, 0.9) : ys);
  const lossTop = Math.min(6, Math.max(finiteMax(runA.loss), runB ? finiteMax(runB.loss) : 0) * 1.05);
  const lossSeries: Series[] = [{ points: pts(show(runA.loss), lossTop), cls: 'series-a', label: runA.label }];
  if (runB) lossSeries.push({ points: pts(show(runB.loss), lossTop), cls: 'series-b', label: runB.label });
  const m = METRICS[metric];
  const mA = runA[metric];
  const mB = runB?.[metric];
  const lo = Math.min(finiteMin(mA), mB ? finiteMin(mB) : Infinity);
  const hi = Math.max(finiteMax(mA), mB ? finiteMax(mB) : 0);
  const mDomain: [number, number] = m.log ? [10 ** Math.floor(Math.log10(lo)), 10 ** Math.ceil(Math.log10(hi))] : [0, hi * 1.1];
  const metricSeries: Series[] = [{ points: pts(mA), cls: 'series-a', label: runA.label }];
  if (runB && mB) metricSeries.push({ points: pts(mB), cls: 'series-b', label: runB.label });
  const spikes = detectSpikes(runA.loss, window, k);
  const first = spikes[0];
  const ckpt = first ? rollbackPoint(first, LOGS.checkpointEvery) : 0;
  const at = (r: RunLog, key: 'loss' | MetricId) => (cur <= r[key].length ? fmt(r[key][cur - 1], 4) : 'stopped');
  const cursorMark = (x: (v: number) => number, top: number, bottom: number) => <line x1={x(cur)} x2={x(cur)} y1={top} y2={bottom} className="cursor-line" />;
  return (
    <Frame
      title="Loss spikes: replay logged training runs"
      caption={
        <>
          {LOGS.model} Every value is from a real run, logged once per step. Red bands: steps the detector flags in the first run; checkpoints every{' '}
          {LOGS.checkpointEvery} steps.
        </>
      }
    >
      <LinePlot series={lossSeries} xDomain={[1, steps]} yDomain={[0, lossTop]} xlabel="step" ylabel="training loss" label="Training loss per step">
        {(x, y) => (
          <g>
            {spikes.map((s) => (
              <rect key={s} x={x(s - 0.5)} y={y(lossTop)} width={Math.max(1.5, x(s + 0.5) - x(s - 0.5))} height={y(0) - y(lossTop)} className="spike-band" />
            ))}
            {runA.val.map(([s, v]) => (
              <circle key={s} cx={x(s)} cy={y(v)} r={2.5} className="dot-a" />
            ))}
            {runB?.val.map(([s, v]) => (
              <circle key={s} cx={x(s)} cy={y(v)} r={2.5} className="dot-b" />
            ))}
            {cursorMark(x, y(lossTop), y(0))}
          </g>
        )}
      </LinePlot>
      <LinePlot
        series={metricSeries}
        xDomain={[1, steps]}
        yDomain={mDomain}
        ylog={m.log}
        xlabel="step"
        ylabel={m.label}
        height={180}
        label={`${m.label} per step`}
      >
        {(x, y) => cursorMark(x, y(mDomain[1]), y(mDomain[0]))}
      </LinePlot>
      <div className="widget-stats" aria-live="polite">
        <span>
          step {cur}: {runA.label} loss {at(runA, 'loss')}, {m.label} {at(runA, metric)}
        </span>
        {runB && (
          <span>
            {runB.label} loss {at(runB, 'loss')}, {m.label} {at(runB, metric)}
          </span>
        )}
        <span>
          {first
            ? `${spikes.length} flagged steps; first at ${first}. Rolling back to the checkpoint at step ${ckpt} replays ${first - 1 - ckpt} steps.`
            : 'no steps flagged'}
        </span>
        <span>{runA.note}</span>
      </div>
      <div className="widget-controls grid2">
        <Select label="Run" value={a} options={ids.map((id) => ({ value: id, label: LOGS.runs[id].label }))} onChange={setA} />
        <Select
          label="Compare with"
          value={b}
          options={[{ value: 'none', label: 'nothing' }, ...ids.filter((id) => id !== a).map((id) => ({ value: id, label: LOGS.runs[id].label }))]}
          onChange={setB}
        />
        <Select
          label="Lower panel"
          value={metric}
          options={(Object.keys(METRICS) as MetricId[]).map((id) => ({ value: id, label: METRICS[id].label }))}
          onChange={setMetric}
        />
        <Slider label="Step" value={cur} min={1} max={steps} step={1} onChange={setCursor} format={(v) => String(v)} />
        <Slider label="Detector window" value={window} min={10} max={200} step={10} onChange={setWindow} format={(v) => `${v} steps`} />
        <Slider label="Detector threshold" value={k} min={2} max={10} step={0.5} onChange={setK} format={(v) => `${v} standard deviations`} />
      </div>
      <div className="widget-controls">
        <Toggle label="Smooth the loss (moving average)" checked={smooth} onChange={setSmooth} />
      </div>
    </Frame>
  );
}
