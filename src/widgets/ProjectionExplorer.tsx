import { useMemo, useState } from 'react';
import { Frame, Slider, Toggle, gauss, num, rng, type WidgetProps, fmt } from './common';
import { LinePlot } from './plot';

// Least squares as projection (M12). The fitted values A w are the point of the
// column space of A = [1, x] nearest to y, so the residual r = y - A w is perpendicular
// to both columns: sum r_i = 0 and sum x_i r_i = 0. Move the line by hand and watch
// both dot products, and the sum of squares, reach their optimum together.

export function makePoints(n: number, seed: number, outlier: boolean) {
  const r = rng(seed);
  const xs = Array.from({ length: n }, (_, i) => -2 + (4 * (i + 0.5)) / n);
  const ys = xs.map((x) => 0.5 + 0.8 * x + 0.45 * gauss(r));
  if (outlier) ys[n - 2] += 4;
  return { xs, ys };
}

export function lstsqLine(xs: number[], ys: number[]) {
  const n = xs.length;
  const sx = xs.reduce((a, b) => a + b, 0);
  const sy = ys.reduce((a, b) => a + b, 0);
  const sxx = xs.reduce((a, x) => a + x * x, 0);
  const sxy = xs.reduce((a, x, i) => a + x * ys[i], 0);
  const det = n * sxx - sx * sx;
  return { intercept: (sxx * sy - sx * sxy) / det, slope: (n * sxy - sx * sy) / det };
}

export function residualStats(xs: number[], ys: number[], intercept: number, slope: number) {
  const r = ys.map((y, i) => y - intercept - slope * xs[i]);
  return {
    r,
    sse: r.reduce((a, v) => a + v * v, 0),
    dotOnes: r.reduce((a, v) => a + v, 0),
    dotX: r.reduce((a, v, i) => a + v * xs[i], 0),
  };
}

export default function ProjectionExplorer({ props }: WidgetProps) {
  const [outlier, setOutlier] = useState(props.outlier === 'true');
  const { xs, ys } = useMemo(() => makePoints(14, 7, outlier), [outlier]);
  const best = lstsqLine(xs, ys);
  const [b0, setB0] = useState(num(props, 'intercept', 0));
  const [b1, setB1] = useState(num(props, 'slope', 0.2));
  const [snap, setSnap] = useState(props.snap === 'true');
  const w0 = snap ? best.intercept : b0;
  const w1 = snap ? best.slope : b1;
  const st = residualStats(xs, ys, w0, w1);
  const opt = residualStats(xs, ys, best.intercept, best.slope);
  return (
    <Frame
      title="Least squares is a projection"
      caption={
        <>
          Sum of squared residuals {fmt(st.sse)} (the least possible is {fmt(opt.sse)}). Residual dot column of ones: {fmt(st.dotOnes)}. Residual dot
          column of x: {fmt(st.dotX)}. Both are zero only at the best line, intercept {fmt(best.intercept)} and slope {fmt(best.slope)}: the residual
          is then perpendicular to every column.
        </>
      }
    >
      <LinePlot
        label="Data points, a line and the residuals"
        xDomain={[-2.2, 2.2]}
        yDomain={[-2.5, 5.5]}
        xlabel="x"
        ylabel="y"
        series={[
          { points: [[-2.2, w0 - 2.2 * w1], [2.2, w0 + 2.2 * w1]], cls: 'series-c', label: 'your line' },
          { points: [[-2.2, best.intercept - 2.2 * best.slope], [2.2, best.intercept + 2.2 * best.slope]], cls: 'series-a', label: 'least squares', dashed: true },
        ]}
      >
        {(sx, sy) =>
          xs.map((x, i) => (
            <g key={i}>
              <line x1={sx(x)} x2={sx(x)} y1={sy(ys[i])} y2={sy(w0 + w1 * x)} className="cursor-line" />
              <circle cx={sx(x)} cy={sy(ys[i])} r={3.5} className="dot-b" />
            </g>
          ))
        }
      </LinePlot>
      <div className="widget-controls grid2">
        <Slider label="Intercept" value={snap ? best.intercept : b0} min={-1.5} max={2.5} step={0.02} onChange={(v) => { setSnap(false); setB0(v); }} />
        <Slider label="Slope" value={snap ? best.slope : b1} min={-1} max={2} step={0.02} onChange={(v) => { setSnap(false); setB1(v); }} />
      </div>
      <div className="widget-controls">
        <Toggle label="Snap to the least-squares line" checked={snap} onChange={setSnap} />
        <Toggle label="Add an outlier" checked={outlier} onChange={setOutlier} />
      </div>
    </Frame>
  );
}
