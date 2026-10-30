import { useMemo, useState } from 'react';
import { Frame, Select, Slider, Toggle, type WidgetProps, fmt } from './common';
import { LinePlot, type Series } from './plot';

// Partial sums of a series against the number of terms (M05). Some settle on a limit;
// the harmonic series keeps climbing like ln n, too slowly to see without a log axis.

export const SERIES: Record<string, { label: string; term: (k: number, r: number) => number; limit: (r: number) => number | null }> = {
  geometric: { label: 'geometric: 1 + r + r^2 + ...', term: (k, r) => r ** (k - 1), limit: (r) => (Math.abs(r) < 1 ? 1 / (1 - r) : null) },
  harmonic: { label: 'harmonic: 1 + 1/2 + 1/3 + ...', term: (k) => 1 / k, limit: () => null },
  squares: { label: 'inverse squares: 1 + 1/4 + 1/9 + ...', term: (k) => 1 / (k * k), limit: () => (Math.PI * Math.PI) / 6 },
  alternating: { label: 'alternating: 1 - 1/2 + 1/3 - ...', term: (k) => (k % 2 ? 1 : -1) / k, limit: () => Math.LN2 },
};

export function partialSums(kind: string, n: number, r = 0.5) {
  const s = SERIES[kind];
  const out: number[] = [];
  let acc = 0;
  for (let k = 1; k <= n; k++) {
    acc += s.term(k, r);
    out.push(acc);
  }
  return out;
}

const EULER_GAMMA = 0.5772156649015329;

export default function SeriesStacker({ props }: WidgetProps) {
  const [kind, setKind] = useState(props.series && SERIES[props.series] ? props.series : 'geometric');
  const [r, setR] = useState(Number(props.r) || 0.5);
  const [logN, setLogN] = useState(Number(props.logn) || 2);
  const [logx, setLogx] = useState(props.logx === 'true');
  const n = Math.round(10 ** logN);
  const sums = useMemo(() => partialSums(kind, n, r), [kind, n, r]);
  const lim = SERIES[kind].limit(r);
  const pick = (k: number) => [k, sums[k - 1]] as [number, number];
  // Plot at most 400 points, spaced evenly in k or in log k.
  const ks = Array.from(new Set(Array.from({ length: 400 }, (_, i) => Math.max(1, Math.round(logx ? n ** (i / 399) : 1 + ((n - 1) * i) / 399)))));
  const ys = sums.filter(Number.isFinite);
  const yMax = Math.min(1e6, Math.max(...ys.map(Math.abs), lim ?? 0, 1));
  const yMin = Math.min(0, ...ys);
  const series: Series[] = [{ label: 'partial sum', cls: 'series-c', points: ks.map(pick) }];
  if (lim !== null) series.push({ label: `limit ${fmt(lim)}`, cls: 'series-a', points: [[1, lim], [n, lim]] as [number, number][] });
  if (kind === 'harmonic')
    series.push({ label: 'ln n + 0.5772', cls: 'series-b', points: ks.map((k) => [k, Math.log(k) + EULER_GAMMA] as [number, number]) });
  return (
    <Frame
      title="Partial sums: does adding forever stay finite?"
      caption={
        <>
          After {n.toLocaleString('en-US')} terms the sum is {fmt(sums[n - 1], 6)}.{' '}
          {lim !== null
            ? `The limit is ${fmt(lim, 6)}; the gap is ${fmt(Math.abs(lim - sums[n - 1]))}.`
            : kind === 'harmonic'
              ? 'No limit: the sum grows like ln n, so every factor of 10 more terms adds about 2.3.'
              : 'With |r| of 1 or more the terms do not shrink, so the sum cannot settle.'}
        </>
      }
    >
      <LinePlot
        label="Partial sums against the number of terms"
        xDomain={[1, Math.max(2, n)]}
        yDomain={[yMin, yMax * 1.08]}
        xlog={logx}
        xlabel="number of terms n"
        ylabel="sum of the first n terms"
        series={series}
      />
      <div className="widget-controls grid2">
        <Select label="Series" value={kind} options={Object.entries(SERIES).map(([k, s]) => ({ value: k, label: s.label }))} onChange={setKind} />
        <Slider label="Terms (log10 of n)" value={logN} min={0.5} max={6} step={0.1} onChange={setLogN} format={(v) => Math.round(10 ** v).toLocaleString('en-US')} />
        {kind === 'geometric' && <Slider label="Ratio r" value={r} min={-1.2} max={1.2} step={0.05} onChange={setR} />}
      </div>
      <div className="widget-controls">
        <Toggle label="Logarithmic n axis" checked={logx} onChange={setLogx} />
      </div>
    </Frame>
  );
}
