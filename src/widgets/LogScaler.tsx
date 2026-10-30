import { useState } from 'react';
import { Frame, Select, Toggle, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// The same data on linear, semi-log and log-log axes (M06). A straight line on semi-log
// axes means exponential growth, on log-log axes a power law; the slope of that line is
// the growth rate or the exponent.

export const DATASETS: Record<string, { label: string; f: (x: number) => number }> = {
  exponential: { label: 'y = 2 x 1.5^x', f: (x) => 2 * 1.5 ** x },
  power: { label: 'y = 3 x^2.5', f: (x) => 3 * x ** 2.5 },
  linear: { label: 'y = 4x + 3', f: (x) => 4 * x + 3 },
  loss: { label: 'loss = 1.7 + 8 n^-0.3 (a loss curve)', f: (x) => 1.7 + 8 * x ** -0.3 },
};

export function fitLine(xs: number[], ys: number[]) {
  const n = xs.length;
  const mx = xs.reduce((a, b) => a + b, 0) / n;
  const my = ys.reduce((a, b) => a + b, 0) / n;
  let sxy = 0;
  let sxx = 0;
  let syy = 0;
  for (let i = 0; i < n; i++) {
    sxy += (xs[i] - mx) * (ys[i] - my);
    sxx += (xs[i] - mx) ** 2;
    syy += (ys[i] - my) ** 2;
  }
  const slope = sxy / sxx;
  return { slope, intercept: my - slope * mx, r2: syy > 0 ? (sxy * sxy) / (sxx * syy) : 1 };
}

export default function LogScaler({ props }: WidgetProps) {
  const [key, setKey] = useState(props.data && DATASETS[props.data] ? props.data : 'exponential');
  const [xlog, setXlog] = useState(props.xlog === 'true');
  const [ylog, setYlog] = useState(props.ylog === 'true');
  const f = DATASETS[key].f;
  const xs = Array.from({ length: 24 }, (_, i) => 1 + (i * 19) / 23);
  const ys = xs.map(f);
  const tx = (x: number) => (xlog ? Math.log10(x) : x);
  const ty = (y: number) => (ylog ? Math.log10(y) : y);
  const fit = fitLine(xs.map(tx), ys.map(ty));
  const straight = fit.r2 > 0.9999;
  const yMin = Math.min(...ys);
  const yMax = Math.max(...ys);
  return (
    <Frame
      title="Which axes make the data straight?"
      caption={
        <>
          Best straight line in these axes: slope {fmt(fit.slope)}, R squared {fit.r2.toFixed(5)}.{' '}
          {straight
            ? xlog && ylog
              ? `Straight on log-log axes: a power law with exponent ${fmt(fit.slope)}.`
              : ylog
                ? `Straight on semi-log axes: exponential growth by a factor of ${fmt(10 ** fit.slope)} per unit of x.`
                : xlog
                  ? 'Straight against log x: y grows like a logarithm.'
                  : 'Straight on linear axes.'
            : 'Still curved in these axes.'}
        </>
      }
    >
      <LinePlot
        label="The dataset on the chosen axes"
        xDomain={[1, 20]}
        yDomain={ylog ? [Math.max(yMin * 0.8, 1e-3), yMax * 1.25] : [Math.min(0, yMin), yMax * 1.05]}
        xlog={xlog}
        ylog={ylog}
        xlabel="x"
        ylabel="y"
        series={[{ label: DATASETS[key].label, cls: 'series-c', points: xs.map((x, i) => [x, ys[i]]) }]}
      >
        {(sx, sy) => xs.map((x, i) => <circle key={i} cx={sx(x)} cy={sy(ys[i])} r={3} className="dot-a" />)}
      </LinePlot>
      <div className="widget-controls">
        <Select label="Data" value={key} options={Object.entries(DATASETS).map(([k, d]) => ({ value: k, label: d.label }))} onChange={setKey} />
        <Toggle label="Logarithmic x axis" checked={xlog} onChange={setXlog} />
        <Toggle label="Logarithmic y axis" checked={ylog} onChange={setYlog} />
      </div>
    </Frame>
  );
}
