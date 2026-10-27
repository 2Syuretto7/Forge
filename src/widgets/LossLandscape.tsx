import { useMemo, useState } from 'react';
import { Frame, Select, Slider, Toggle, gauss, num, rng, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

type Surface = 'quadratic' | 'rosenbrock' | 'saddle';
type V2 = [number, number];

export function surfaceFns(s: Surface, kappa: number) {
  const c = Math.cos(Math.PI / 6);
  const sn = Math.sin(Math.PI / 6);
  if (s === 'quadratic') {
    // 0.5 * (u^2 + kappa v^2) in coordinates rotated by 30 degrees
    const f = ([x, y]: V2) => {
      const u = c * x + sn * y;
      const v = -sn * x + c * y;
      return 0.5 * (u * u + kappa * v * v);
    };
    const g = ([x, y]: V2): V2 => {
      const u = c * x + sn * y;
      const v = -sn * x + c * y;
      return [c * u - sn * kappa * v, sn * u + c * kappa * v];
    };
    return { f, g, box: 2.2, start: [-1.8, 1.4] as V2 };
  }
  if (s === 'rosenbrock') {
    const f = ([x, y]: V2) => (1 - x) ** 2 + 10 * (y - x * x) ** 2;
    const g = ([x, y]: V2): V2 => [-2 * (1 - x) - 40 * x * (y - x * x), 20 * (y - x * x)];
    return { f, g, box: 2, start: [-1.5, 1.8] as V2 };
  }
  const f = ([x, y]: V2) => 0.5 * x * x - 0.25 * y * y + 0.05 * y ** 4;
  const g = ([x, y]: V2): V2 => [x, -0.5 * y + 0.2 * y ** 3];
  return { f, g, box: 2.5, start: [-2, 0.02] as V2 };
}

type Opt = 'sgd' | 'momentum' | 'adam';

export function run(opt: Opt, g: (p: V2) => V2, f: (p: V2) => number, start: V2, lr: number, beta: number, noise: number, steps: number, biasCorr: boolean) {
  const r = rng(11);
  let p: V2 = [...start];
  let m: V2 = [0, 0];
  let v: V2 = [0, 0];
  const path: V2[] = [p];
  const losses: [number, number][] = [[0, f(p)]];
  for (let t = 1; t <= steps; t++) {
    const gr = g(p);
    const gn: V2 = [gr[0] + noise * gauss(r), gr[1] + noise * gauss(r)];
    if (opt === 'sgd') p = [p[0] - lr * gn[0], p[1] - lr * gn[1]];
    else if (opt === 'momentum') {
      m = [beta * m[0] + gn[0], beta * m[1] + gn[1]];
      p = [p[0] - lr * m[0], p[1] - lr * m[1]];
    } else {
      const b1 = 0.9;
      const b2 = 0.999;
      m = [b1 * m[0] + (1 - b1) * gn[0], b1 * m[1] + (1 - b1) * gn[1]];
      v = [b2 * v[0] + (1 - b2) * gn[0] ** 2, b2 * v[1] + (1 - b2) * gn[1] ** 2];
      const c1 = biasCorr ? 1 - b1 ** t : 1;
      const c2 = biasCorr ? 1 - b2 ** t : 1;
      p = [p[0] - (lr * m[0]) / c1 / (Math.sqrt(v[0] / c2) + 1e-8), p[1] - (lr * m[1]) / c1 / (Math.sqrt(v[1] / c2) + 1e-8)];
    }
    if (!Number.isFinite(p[0]) || !Number.isFinite(p[1]) || Math.abs(p[0]) > 1e3 || Math.abs(p[1]) > 1e3) break;
    path.push(p);
    losses.push([t, f(p)]);
  }
  return { path, losses };
}

export default function LossLandscape({ props }: WidgetProps) {
  const [surface, setSurface] = useState<Surface>((props.surface as Surface) ?? 'quadratic');
  const [kappa, setKappa] = useState(num(props, 'kappa', 10));
  const [logLr, setLogLr] = useState(num(props, 'loglr', -1));
  const [beta, setBeta] = useState(num(props, 'beta', 0.9));
  const [noise, setNoise] = useState(num(props, 'noise', 0));
  const [biasCorr, setBiasCorr] = useState(true);
  const [show, setShow] = useState<Record<Opt, boolean>>({ sgd: true, momentum: true, adam: true });
  const lr = 10 ** logLr;
  const { f, g, box, start } = surfaceFns(surface, kappa);
  const steps = 150;
  const runs = useMemo(
    () => ({
      sgd: run('sgd', g, f, start, lr, beta, noise, steps, biasCorr),
      momentum: run('momentum', g, f, start, lr * (1 - beta), beta, noise, steps, biasCorr),
      adam: run('adam', g, f, start, lr, beta, noise, steps, biasCorr),
    }),
    // surface functions are recreated each render; depend on their inputs instead
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [surface, kappa, lr, beta, noise, biasCorr],
  );
  const S = 300;
  const toPx = (v: number) => ((v + box) / (2 * box)) * S;
  const cells = 40;
  const vals: number[] = [];
  for (let j = 0; j < cells; j++)
    for (let i = 0; i < cells; i++) vals.push(f([-box + ((i + 0.5) * 2 * box) / cells, box - ((j + 0.5) * 2 * box) / cells]));
  const lo = Math.min(...vals);
  const hi = Math.max(...vals);
  const cls: Record<Opt, 'series-a' | 'series-b' | 'series-c'> = { sgd: 'series-a', momentum: 'series-b', adam: 'series-c' };
  const label: Record<Opt, string> = { sgd: 'SGD', momentum: 'momentum (lr scaled by 1 - beta)', adam: 'Adam' };
  const finalLoss = (o: Opt) => runs[o].losses[runs[o].losses.length - 1][1];
  const allLoss = (Object.keys(runs) as Opt[]).filter((o) => show[o]).flatMap((o) => runs[o].losses.map((l) => l[1]));
  return (
    <Frame
      title="Optimizers on a 2D loss surface"
      caption={
        <>
          Final loss after {steps} steps: SGD {fmt(finalLoss('sgd'))}, momentum {fmt(finalLoss('momentum'))}, Adam {fmt(finalLoss('adam'))}. A
          trajectory that leaves the frame has diverged.{' '}
          {surface === 'quadratic' && `With condition number ${kappa}, plain gradient descent needs a step below 2 / ${kappa} to stay stable.`}
        </>
      }
    >
      <div className="widget-grid">
        <svg viewBox={`0 0 ${S} ${S}`} className="widget-svg" role="img" aria-label="Loss surface heat map with optimizer trajectories">
          {vals.map((v, k) => {
            const i = k % cells;
            const j = Math.floor(k / cells);
            const t = Math.log1p(v - lo) / Math.log1p(hi - lo);
            return <rect key={k} x={(i * S) / cells} y={(j * S) / cells} width={S / cells + 0.5} height={S / cells + 0.5} fill="var(--theory)" opacity={0.75 - 0.7 * t} shapeRendering="crispEdges" />;
          })}
          {(Object.keys(runs) as Opt[])
            .filter((o) => show[o])
            .map((o) => (
              <polyline key={o} points={runs[o].path.map(([x, y]) => `${toPx(x)},${S - toPx(y)}`).join(' ')} className={cls[o]} fill="none" />
            ))}
          <circle cx={toPx(start[0])} cy={S - toPx(start[1])} r={4} className="marker" />
        </svg>
        <LinePlot
          label="Loss against iteration for each optimizer"
          series={(Object.keys(runs) as Opt[]).filter((o) => show[o]).map((o) => ({ points: runs[o].losses.map(([t, l]) => [t, Math.max(l - lo, 1e-8)] as [number, number]), cls: cls[o], label: label[o] }))}
          xDomain={[0, steps]}
          yDomain={[1e-8, Math.max(10, ...allLoss.map((l) => l - lo + 1))]}
          ylog
          xlabel="iteration"
          ylabel="loss minus minimum"
          height={260}
        />
      </div>
      <div className="widget-controls">
        <Select
          label="Surface"
          value={surface}
          options={[
            { value: 'quadratic', label: 'Ill-conditioned quadratic' },
            { value: 'rosenbrock', label: 'Rosenbrock valley' },
            { value: 'saddle', label: 'Saddle point' },
          ]}
          onChange={setSurface}
        />
        {(Object.keys(show) as Opt[]).map((o) => (
          <Toggle key={o} label={label[o]} checked={show[o]} onChange={(v) => setShow((s) => ({ ...s, [o]: v }))} />
        ))}
        <Toggle label="Adam bias correction" checked={biasCorr} onChange={setBiasCorr} />
      </div>
      <div className="widget-controls grid2">
        <Slider label="Learning rate (log10)" value={logLr} min={-3} max={0.5} step={0.05} onChange={setLogLr} format={(v) => (10 ** v).toPrecision(2)} />
        <Slider label="Momentum beta" value={beta} min={0} max={0.99} step={0.01} onChange={setBeta} />
        {surface === 'quadratic' && <Slider label="Condition number" value={kappa} min={1} max={100} step={1} onChange={setKappa} format={(v) => String(v)} />}
        <Slider label="Gradient noise" value={noise} min={0} max={2} step={0.05} onChange={setNoise} />
      </div>
    </Frame>
  );
}
