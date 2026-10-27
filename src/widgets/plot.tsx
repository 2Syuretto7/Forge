// Minimal SVG plotting shared by widgets: axes, ticks, line series, bars.
import type { ReactNode } from 'react';

export interface Series {
  points: [number, number][];
  cls: 'series-a' | 'series-b' | 'series-c' | 'series-d';
  label: string;
  dashed?: boolean;
}

export interface Scale {
  (v: number): number;
  domain: [number, number];
  log: boolean;
}

export function scale(domain: [number, number], range: [number, number], log = false): Scale {
  const [d0, d1] = log ? [Math.log10(domain[0]), Math.log10(domain[1])] : domain;
  const f = ((v: number) => {
    const t = log ? Math.log10(Math.max(v, 1e-300)) : v;
    return range[0] + ((t - d0) / (d1 - d0 || 1)) * (range[1] - range[0]);
  }) as Scale;
  f.domain = domain;
  f.log = log;
  return f;
}

export function ticks(domain: [number, number], log: boolean, count = 5): number[] {
  const [a, b] = domain;
  if (log) {
    const out: number[] = [];
    const e0 = Math.ceil(Math.log10(a));
    const e1 = Math.floor(Math.log10(b));
    if (!Number.isFinite(e0) || !Number.isFinite(e1)) return out;
    const stride = Math.max(1, Math.ceil((e1 - e0 + 1) / count));
    for (let e = e0; e <= e1; e += stride) out.push(10 ** e);
    return out;
  }
  const span = b - a || 1;
  if (!Number.isFinite(span)) return [];
  const step0 = span / count;
  const mag = 10 ** Math.floor(Math.log10(step0));
  const step = [1, 2, 5, 10].map((m) => m * mag).find((s) => span / s <= count) ?? mag * 10;
  const out: number[] = [];
  for (let v = Math.ceil(a / step) * step; v <= b + 1e-9 * span; v += step) out.push(Math.round(v / step) * step);
  return out;
}

const tickLabel = (v: number, log: boolean) => {
  if (log) return v >= 1000 || v < 0.01 ? `1e${Math.round(Math.log10(v))}` : String(v);
  if (Math.abs(v) >= 1e4 || (Math.abs(v) < 1e-3 && v !== 0)) return v.toExponential(0);
  return String(Math.round(v * 1000) / 1000);
};

export function Axes({
  x,
  y,
  width,
  height,
  pad,
  xlabel,
  ylabel,
}: {
  x: Scale;
  y: Scale;
  width: number;
  height: number;
  pad: { l: number; r: number; t: number; b: number };
  xlabel: string;
  ylabel: string;
}) {
  return (
    <g>
      <line x1={pad.l} y1={height - pad.b} x2={width - pad.r} y2={height - pad.b} className="axis" />
      <line x1={pad.l} y1={pad.t} x2={pad.l} y2={height - pad.b} className="axis" />
      {ticks(x.domain, x.log).map((t) => (
        <g key={'x' + t}>
          <line x1={x(t)} x2={x(t)} y1={height - pad.b} y2={height - pad.b + 4} className="axis" />
          <text x={x(t)} y={height - pad.b + 15} textAnchor="middle">
            {tickLabel(t, x.log)}
          </text>
        </g>
      ))}
      {ticks(y.domain, y.log).map((t) => (
        <g key={'y' + t}>
          <line x1={pad.l - 4} x2={pad.l} y1={y(t)} y2={y(t)} className="axis" />
          <text x={pad.l - 6} y={y(t) + 3} textAnchor="end">
            {tickLabel(t, y.log)}
          </text>
        </g>
      ))}
      <text x={(pad.l + width - pad.r) / 2} y={height - 4} textAnchor="middle">
        {xlabel}
      </text>
      <text x={12} y={(pad.t + height - pad.b) / 2} textAnchor="middle" transform={`rotate(-90 12 ${(pad.t + height - pad.b) / 2})`}>
        {ylabel}
      </text>
    </g>
  );
}

export function path(points: [number, number][], x: Scale, y: Scale) {
  return points
    .filter(([a, b]) => Number.isFinite(a) && Number.isFinite(b))
    .map(([a, b], i) => `${i ? 'L' : 'M'}${x(a).toFixed(1)},${y(b).toFixed(1)}`)
    .join(' ');
}

export function LinePlot({
  series,
  xDomain,
  yDomain,
  xlabel,
  ylabel,
  xlog = false,
  ylog = false,
  width = 420,
  height = 240,
  children,
  label,
}: {
  series: Series[];
  xDomain: [number, number];
  yDomain: [number, number];
  xlabel: string;
  ylabel: string;
  xlog?: boolean;
  ylog?: boolean;
  width?: number;
  height?: number;
  children?: (x: Scale, y: Scale) => ReactNode;
  label: string;
}) {
  const pad = { l: 48, r: 12, t: 10, b: 34 };
  const x = scale(xDomain, [pad.l, width - pad.r], xlog);
  const y = scale(yDomain, [height - pad.b, pad.t], ylog);
  return (
    <div>
      <svg viewBox={`0 0 ${width} ${height}`} className="widget-svg" role="img" aria-label={label}>
        <defs>
          <clipPath id={`clip-${label.length}-${width}`}>
            <rect x={pad.l} y={pad.t} width={width - pad.l - pad.r} height={height - pad.t - pad.b} />
          </clipPath>
        </defs>
        <Axes x={x} y={y} width={width} height={height} pad={pad} xlabel={xlabel} ylabel={ylabel} />
        <g clipPath={`url(#clip-${label.length}-${width})`}>
          {series.map((s) => (
            <path key={s.label} d={path(s.points, x, y)} className={s.cls} strokeDasharray={s.dashed ? '5 4' : undefined} />
          ))}
          {children?.(x, y)}
        </g>
      </svg>
      <Legend items={series.map((s) => ({ cls: s.cls, label: s.label, dashed: s.dashed }))} />
    </div>
  );
}

export function Legend({ items }: { items: { cls: string; label: string; dashed?: boolean }[] }) {
  return (
    <ul className="legend-row">
      {items.map((it) => (
        <li key={it.label}>
          <svg width="22" height="10" aria-hidden="true" className="widget-svg legend-swatch">
            <line x1="1" y1="5" x2="21" y2="5" className={it.cls} strokeDasharray={it.dashed ? '4 3' : undefined} />
          </svg>
          {it.label}
        </li>
      ))}
    </ul>
  );
}
