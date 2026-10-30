import { useMemo, useState } from 'react';
import { Frame, Select, Slider, Toggle, type WidgetProps, fmt } from './common';

// Gaussian elimination on an augmented matrix, one row operation at a time (M11).
// With partial pivoting the largest entry in the column becomes the pivot; without it
// any nonzero entry is used, and a tiny pivot multiplies rounding errors by 1/pivot.

export interface Step {
  note: string;
  M: number[][];
  pivot?: [number, number];
}

export interface Elimination {
  steps: Step[];
  rank: number;
  status: 'unique' | 'infinite' | 'none';
  x: number[] | null;
  residual: number;
}

export function eliminate(A: number[][], b: number[], pivoting: boolean, tol = 1e-10): Elimination {
  const m = A.length;
  const n = A[0].length;
  const M = A.map((r, i) => [...r, b[i]]);
  const scale = Math.max(1e-300, ...A.flat().map(Math.abs));
  const snap = (note: string, pivot?: [number, number]): Step => ({ note, M: M.map((r) => [...r]), pivot });
  const steps: Step[] = [snap('The augmented matrix [A | b].')];
  const pivCols: number[] = [];
  let r = 0;
  for (let j = 0; j < n && r < m; j++) {
    let p = -1;
    if (pivoting) {
      p = r;
      for (let i = r + 1; i < m; i++) if (Math.abs(M[i][j]) > Math.abs(M[p][j])) p = i;
      if (Math.abs(M[p][j]) <= tol * scale) p = -1;
    } else {
      for (let i = r; i < m; i++)
        if (M[i][j] !== 0) {
          p = i;
          break;
        }
    }
    if (p < 0) {
      steps.push(snap(`Column ${j + 1} has no usable pivot below row ${r}: it is a free column.`));
      continue;
    }
    if (p !== r) {
      [M[r], M[p]] = [M[p], M[r]];
      steps.push(snap(`Swap rows ${r + 1} and ${p + 1} so the pivot is ${fmt(M[r][j])}.`, [r, j]));
    }
    for (let i = r + 1; i < m; i++) {
      const f = M[i][j] / M[r][j];
      if (f === 0) continue;
      for (let k = j; k <= n; k++) M[i][k] -= f * M[r][k];
      M[i][j] = 0;
      steps.push(snap(`Row ${i + 1} minus ${fmt(f)} times row ${r + 1}.`, [r, j]));
    }
    pivCols.push(j);
    r++;
  }
  const rank = pivCols.length;
  const rhsScale = Math.max(1, ...b.map(Math.abs));
  const inconsistent = M.slice(rank).some((row) => Math.abs(row[n]) > tol * rhsScale * Math.max(1, scale));
  let x: number[] | null = null;
  let status: Elimination['status'];
  if (inconsistent) status = 'none';
  else {
    status = rank === n ? 'unique' : 'infinite';
    x = Array(n).fill(0);
    for (let k = rank - 1; k >= 0; k--) {
      const j = pivCols[k];
      let s = M[k][n];
      for (let c = j + 1; c < n; c++) s -= M[k][c] * x[c];
      x[j] = s / M[k][j];
    }
  }
  const residual = x ? Math.hypot(...A.map((row, i) => row.reduce((s, a, k) => s + a * x![k], 0) - b[i])) : NaN;
  steps.push(
    snap(
      status === 'none'
        ? `Rank ${rank}, and a zero row of A has a nonzero right side: no solution.`
        : status === 'unique'
          ? `Rank ${rank} = number of unknowns: back substitution gives the one solution.`
          : `Rank ${rank} < ${n} unknowns: ${n - rank} free variable(s), infinitely many solutions (free variables set to 0 below).`,
    ),
  );
  return { steps, rank, status, x, residual };
}

export const PRESETS: Record<string, { label: string; A: number[][]; b: number[] }> = {
  unique: { label: 'Three independent sensors', A: [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], b: [8, -11, -3] },
  same: { label: 'Two sensors measure the same thing', A: [[1, 2, 1], [2, 4, 2], [1, 0, 1]], b: [4, 8, 2] },
  clash: { label: 'Same sensors, readings disagree', A: [[1, 2, 1], [2, 4, 2], [1, 0, 1]], b: [4, 8.1, 2] },
  tiny: { label: 'A tiny leading entry', A: [[1e-20, 1], [1, 1]], b: [1, 2] },
};

export default function EliminationStepper({ props }: WidgetProps) {
  const [preset, setPreset] = useState(props.preset && PRESETS[props.preset] ? props.preset : 'unique');
  const [pivoting, setPivoting] = useState(props.pivoting !== 'false');
  const { A, b } = PRESETS[preset];
  const res = useMemo(() => eliminate(A, b, pivoting), [A, b, pivoting]);
  const [k, setK] = useState(0);
  const step = Math.min(k, res.steps.length - 1);
  const s = res.steps[step];
  const n = A[0].length;
  return (
    <Frame
      title="Gaussian elimination, step by step"
      caption={
        <>
          {s.note}{' '}
          {step === res.steps.length - 1 && res.x && (
            <>
              x = ({res.x.map((v) => fmt(v)).join(', ')}); residual |Ax - b| = {fmt(res.residual)}.
            </>
          )}
        </>
      }
    >
      <div style={{ overflowX: 'auto' }} role="group" aria-label="Augmented matrix [A | b]">
        <table className="widget-table truth" aria-label={`Augmented matrix after step ${step}`}>
          <tbody>
            {s.M.map((row, i) => (
              <tr key={i}>
                {row.map((v, j) => (
                  <td key={j} style={{ borderLeft: j === n ? '2px solid var(--border)' : undefined, fontWeight: s.pivot && s.pivot[0] === i && s.pivot[1] === j ? 700 : undefined, color: s.pivot && s.pivot[0] === i && s.pivot[1] === j ? 'var(--accent)' : undefined }}>
                    {fmt(v, 3)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="widget-controls">
        <Slider label={`Step (of ${res.steps.length - 1})`} value={step} min={0} max={res.steps.length - 1} step={1} onChange={setK} format={(v) => String(v)} />
      </div>
      <div className="widget-controls">
        <Select
          label="System"
          value={preset}
          onChange={(v) => {
            setPreset(v);
            setK(0);
          }}
          options={Object.entries(PRESETS).map(([value, p]) => ({ value, label: p.label }))}
        />
        <Toggle
          label="Partial pivoting"
          checked={pivoting}
          onChange={(v) => {
            setPivoting(v);
            setK(0);
          }}
        />
      </div>
    </Frame>
  );
}
