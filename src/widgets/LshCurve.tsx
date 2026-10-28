import { useState } from 'react';
import { Frame, Select, Slider, fmt, type WidgetProps } from './common';
import { LinePlot, type Series } from './plot';

// Banded locality-sensitive hashing over MinHash signatures: two documents with Jaccard
// similarity s collide in one band of r rows with probability s^r, and in at least one of b bands
// with probability 1 - (1 - s^r)^b.
export const candidateProbability = (s: number, bands: number, rows: number) => 1 - (1 - s ** rows) ** bands;
export const lshThreshold = (bands: number, rows: number) => (1 / bands) ** (1 / rows);

export function factorizations(n: number): [number, number][] {
  const out: [number, number][] = [];
  for (let r = 1; r <= n; r++) if (n % r === 0) out.push([n / r, r]);
  return out;
}

const SIMS = [0.3, 0.5, 0.7, 0.8, 0.9, 0.95];

export default function LshCurve({ props }: WidgetProps) {
  const [perm, setPerm] = useState(String(Number(props.perm) || 128));
  const options = factorizations(Number(perm)).filter(([b, r]) => b > 1 && r > 1);
  const [idx, setIdx] = useState(Math.max(0, options.findIndex(([, r]) => r === 8)));
  const [bands, rows] = options[Math.min(idx, options.length - 1)];
  const [cut, setCut] = useState(0.8);
  const t = lshThreshold(bands, rows);
  const curve: Series[] = [
    {
      points: Array.from({ length: 201 }, (_, i) => [i / 200, candidateProbability(i / 200, bands, rows)] as [number, number]),
      cls: 'series-a',
      label: `${bands} bands of ${rows} rows`,
    },
    { points: [[0, 0], [cut, 0], [cut, 1], [1, 1]], cls: 'series-c', label: 'ideal: flag every pair above the cutoff', dashed: true },
  ];
  return (
    <Frame
      title="LSH: the probability that two documents become candidates"
      caption={
        <>
          Each signature of {perm} MinHash values is cut into {bands} bands of {rows} rows; two documents become candidates if any band matches exactly.
          The curve rises steeply near {fmt(t, 2)}: pairs well below are almost never compared, pairs well above almost always are.
        </>
      }
    >
      <LinePlot
        series={curve}
        xDomain={[0, 1]}
        yDomain={[0, 1]}
        xlabel="Jaccard similarity of the pair"
        ylabel="probability of becoming a candidate"
        label="Candidate probability against Jaccard similarity"
      >
        {(x, y) => <line x1={x(t)} x2={x(t)} y1={y(0)} y2={y(1)} className="grid-line" strokeDasharray="3 3" />}
      </LinePlot>
      <table className="widget-table">
        <thead>
          <tr>
            <th>similarity</th>
            {SIMS.map((s) => (
              <th key={s}>{s}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>candidate</td>
            {SIMS.map((s) => (
              <td key={s}>{fmt(candidateProbability(s, bands, rows), 3)}</td>
            ))}
          </tr>
        </tbody>
      </table>
      <div className="widget-stats" aria-live="polite">
        <span>
          threshold (1/b)^(1/r) = {fmt(t, 3)}; a pair at the cutoff {cut} is missed with probability {fmt(1 - candidateProbability(cut, bands, rows), 3)}
        </span>
      </div>
      <div className="widget-controls grid2">
        <Select
          label="Signature length"
          value={perm}
          options={['64', '128', '256'].map((v) => ({ value: v, label: `${v} hashes` }))}
          onChange={(v) => {
            setPerm(v);
            setIdx(0);
          }}
        />
        <Slider
          label="Bands x rows"
          value={Math.min(idx, options.length - 1)}
          min={0}
          max={options.length - 1}
          step={1}
          onChange={setIdx}
          format={(v) => `${options[v][0]} x ${options[v][1]}`}
        />
        <Slider label="Similarity cutoff" value={cut} min={0.5} max={0.95} step={0.05} onChange={setCut} format={(v) => v.toFixed(2)} />
      </div>
    </Frame>
  );
}
