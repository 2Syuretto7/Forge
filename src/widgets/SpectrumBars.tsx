import { useMemo, useState } from 'react';
import { Frame, Select, Slider, gauss, num, rng, type WidgetProps, fmt } from './common';

// Singular values of a 60 x 40 data matrix (M14, M33): a planted low-rank signal plus
// noise, or a power-law spectrum. Keeping the top k singular triplets leaves the error
// sqrt(sum of the discarded sigma_i^2) in Frobenius norm (Eckart-Young).

// Cyclic Jacobi rotations: eigenvalues of a symmetric matrix, in decreasing order.
export function symEigvals(S: number[][]): number[] {
  const n = S.length;
  const A = S.map((r) => [...r]);
  for (let sweep = 0; sweep < 60; sweep++) {
    let off = 0;
    for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += A[p][q] * A[p][q];
    if (off < 1e-22 * Math.max(1e-300, A.reduce((s, r, i) => s + r[i] * r[i], 0))) break;
    for (let p = 0; p < n; p++)
      for (let q = p + 1; q < n; q++) {
        if (Math.abs(A[p][q]) < 1e-300) continue;
        const theta = (A[q][q] - A[p][p]) / (2 * A[p][q]);
        const t = Math.sign(theta || 1) / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
        const c = 1 / Math.sqrt(t * t + 1);
        const s = t * c;
        for (let k = 0; k < n; k++) {
          const akp = A[k][p];
          const akq = A[k][q];
          A[k][p] = c * akp - s * akq;
          A[k][q] = s * akp + c * akq;
        }
        for (let k = 0; k < n; k++) {
          const apk = A[p][k];
          const aqk = A[q][k];
          A[p][k] = c * apk - s * aqk;
          A[q][k] = s * apk + c * aqk;
        }
      }
  }
  return A.map((r, i) => r[i]).sort((a, b) => b - a);
}

export function singularValues(A: number[][]): number[] {
  const n = A[0].length;
  const G = Array.from({ length: n }, (_, i) => Array.from({ length: n }, (_, j) => A.reduce((s, row) => s + row[i] * row[j], 0)));
  return symEigvals(G).map((l) => Math.sqrt(Math.max(0, l)));
}

export function tailError(s: number[], k: number) {
  const total = s.reduce((a, v) => a + v * v, 0);
  const tail = s.slice(k).reduce((a, v) => a + v * v, 0);
  return { abs: Math.sqrt(tail), rel: Math.sqrt(tail / total), explained: 1 - tail / total };
}

export type Shape = 'planted' | 'power';

export function makeMatrix(shape: Shape, rank: number, noise: number, seed = 3, m = 60, n = 40): number[][] {
  const r = rng(seed);
  const A = Array.from({ length: m }, () => Array(n).fill(0));
  const terms = shape === 'planted' ? rank : n;
  for (let t = 0; t < terms; t++) {
    const w = shape === 'planted' ? 10 * 0.8 ** t : 10 / (t + 1);
    const u = Array.from({ length: m }, () => gauss(r) / Math.sqrt(m));
    const v = Array.from({ length: n }, () => gauss(r) / Math.sqrt(n));
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) A[i][j] += w * u[i] * v[j];
  }
  for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) A[i][j] += (noise * gauss(r)) / Math.sqrt(m);
  return A;
}

export default function SpectrumBars({ props }: WidgetProps) {
  const [shape, setShape] = useState<Shape>(props.shape === 'power' ? 'power' : 'planted');
  const [rank, setRank] = useState(num(props, 'rank', 3));
  const [noise, setNoise] = useState(num(props, 'noise', 0.3));
  const [k, setK] = useState(num(props, 'k', 3));
  const s = useMemo(() => singularValues(makeMatrix(shape, rank, noise)), [shape, rank, noise]);
  const err = tailError(s, k);
  const W = 420;
  const H = 220;
  const pad = { l: 40, r: 10, t: 10, b: 30 };
  const bw = (W - pad.l - pad.r) / s.length;
  const smax = s[0] || 1;
  const y = (v: number) => H - pad.b - ((H - pad.t - pad.b) * v) / smax;
  let cum = 0;
  const total = s.reduce((a, v) => a + v * v, 0) || 1;
  const cumPts = s.map((v, i) => {
    cum += v * v;
    return `${pad.l + bw * (i + 0.5)},${H - pad.b - ((H - pad.t - pad.b) * cum) / total}`;
  });
  return (
    <Frame
      title="Singular values and low-rank approximation"
      caption={
        <>
          Keeping the top {k} of {s.length} singular values explains {fmt(100 * err.explained, 1)} percent of the squared Frobenius norm. The rank-{k}{' '}
          error is sqrt(sum of the discarded sigma squared) = {fmt(err.abs)}, {fmt(100 * err.rel, 1)} percent of the norm of A, and no rank-{k} matrix
          does better. The line is the cumulative fraction of sigma squared.
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Bar chart of singular values in decreasing order with the cumulative energy">
        <line x1={pad.l} y1={H - pad.b} x2={W - pad.r} y2={H - pad.b} className="axis" />
        <line x1={pad.l} y1={pad.t} x2={pad.l} y2={H - pad.b} className="axis" />
        {s.map((v, i) => (
          <rect key={i} x={pad.l + bw * i + 1} y={y(v)} width={Math.max(1, bw - 2)} height={H - pad.b - y(v)} className={i < k ? 'bar-a' : 'bar-d'} opacity={i < k ? 0.9 : 0.45} />
        ))}
        <polyline points={cumPts.join(' ')} className="series-c" />
        <text x={pad.l} y={H - 8}>
          1
        </text>
        <text x={W - pad.r} y={H - 8} textAnchor="end">
          index i = {s.length}
        </text>
        <text x={pad.l - 4} y={pad.t + 10} textAnchor="end">
          {fmt(smax, 1)}
        </text>
      </svg>
      <div className="widget-controls grid2">
        <Slider label="Keep the top k" value={k} min={0} max={s.length} step={1} onChange={setK} format={(v) => String(v)} />
        <Slider label="Noise level" value={noise} min={0} max={1.5} step={0.05} onChange={setNoise} />
        {shape === 'planted' && <Slider label="Planted rank" value={rank} min={1} max={10} step={1} onChange={setRank} format={(v) => String(v)} />}
      </div>
      <div className="widget-controls">
        <Select<Shape>
          label="Signal"
          value={shape}
          onChange={setShape}
          options={[
            { value: 'planted', label: 'Low rank plus noise' },
            { value: 'power', label: 'Power-law spectrum, sigma_i about 1/i' },
          ]}
        />
      </div>
    </Frame>
  );
}
