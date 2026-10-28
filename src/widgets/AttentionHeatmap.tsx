import { useMemo, useState } from 'react';
import { Frame, Select, Slider, Toggle, gauss, rng, type WidgetProps, fmt } from './common';

export type Matrix = number[][];

const dot = (a: number[], b: number[]) => a.reduce((s, v, i) => s + v * b[i], 0);

// Row-wise softmax of the scores; with causal=true, entries above the
// diagonal are masked to -infinity (weight exactly zero).
export function softmaxRows(S: Matrix, causal: boolean): Matrix {
  return S.map((row, i) => {
    const vals = row.map((v, j) => (causal && j > i ? -Infinity : v));
    const m = Math.max(...vals);
    const e = vals.map((v) => (v === -Infinity ? 0 : Math.exp(v - m)));
    const z = e.reduce((a, b) => a + b, 0);
    return e.map((v) => v / z);
  });
}

export function attention(Q: Matrix, K: Matrix, V: Matrix, opts: { causal: boolean; scaled: boolean }) {
  const d = Q[0].length;
  const c = opts.scaled ? 1 / Math.sqrt(d) : 1;
  const logits = Q.map((q) => K.map((k) => c * dot(q, k)));
  const weights = softmaxRows(logits, opts.causal);
  const out = weights.map((w) => V[0].map((_, j) => w.reduce((s, wi, i) => s + wi * V[i][j], 0)));
  return { logits, weights, out };
}

export const rowEntropyBits = (w: number[]) => -w.reduce((s, p) => s + (p > 0 ? p * Math.log2(p) : 0), 0);

export const TOKENS = ['the', 'cat', 'sat', 'on', 'the', 'mat', 'because', 'the', 'cat', 'was', 'tired'];

type Pattern = 'random' | 'previous' | 'same';

// Queries and keys for three kinds of head. "random": unit-variance random
// projections, so each logit q.k has variance d. "previous": every query
// matches the key of the token before it. "same": each token matches earlier
// occurrences of the same word.
export function makeQK(pattern: Pattern, d: number, strength: number, seed = 3): { Q: Matrix; K: Matrix } {
  const r = rng(seed);
  const L = TOKENS.length;
  const randVec = () => Array.from({ length: d }, () => gauss(r));
  if (pattern === 'random') return { Q: TOKENS.map(randVec), K: TOKENS.map(randVec) };
  const codes = Array.from({ length: L + 1 }, () => randVec().map((v) => v / Math.sqrt(d)));
  const vocab = [...new Set(TOKENS)];
  const s = Math.sqrt(strength * Math.sqrt(d));
  if (pattern === 'previous') {
    return { Q: TOKENS.map((_, i) => codes[i].map((v) => v * s)), K: TOKENS.map((_, j) => codes[j + 1].map((v) => v * s)) };
  }
  const word = vocab.map(() => randVec().map((v) => v / Math.sqrt(d)));
  const id = (t: string) => vocab.indexOf(t);
  return { Q: TOKENS.map((t) => word[id(t)].map((v) => v * s)), K: TOKENS.map((t) => word[id(t)].map((v) => v * s)) };
}

export default function AttentionHeatmap({ props }: WidgetProps) {
  const [pattern, setPattern] = useState<Pattern>((['random', 'previous', 'same'] as Pattern[]).includes(props.pattern as Pattern) ? (props.pattern as Pattern) : 'random');
  const [logD, setLogD] = useState(Math.log2(Number(props.d) || 16));
  const [scaled, setScaled] = useState(props.scaled !== 'false');
  const [causal, setCausal] = useState(props.causal !== 'false');
  const [strength, setStrength] = useState(4);
  const [query, setQuery] = useState(TOKENS.length - 2);
  const d = 2 ** logD;
  const { weights, logits } = useMemo(() => {
    const { Q, K } = makeQK(pattern, d, strength);
    const V = K.map((_, i) => [i]);
    return attention(Q, K, V, { causal, scaled });
  }, [pattern, d, strength, causal, scaled]);
  const L = TOKENS.length;
  const cell = 30;
  const left = 64;
  const top = 64;
  const W = left + L * cell + 8;
  const H = top + L * cell + 8;
  const flatLogits = logits.flatMap((row, i) => row.filter((_, j) => !causal || j <= i));
  const mean = flatLogits.reduce((a, b) => a + b, 0) / flatLogits.length;
  const std = Math.sqrt(flatLogits.reduce((a, b) => a + (b - mean) ** 2, 0) / flatLogits.length);
  const ent = weights.map(rowEntropyBits);
  const meanMax = weights.reduce((a, w) => a + Math.max(...w), 0) / L;
  return (
    <Frame
      title="Attention weights for a toy sentence"
      caption={
        <>
          Row = query, column = key; darker means more weight, and each row sums to 1. Logit standard deviation {fmt(std, 2)}; mean largest weight per row{' '}
          {fmt(meanMax, 2)}; query &quot;{TOKENS[query]}&quot; (position {query}) spreads its attention over {fmt(2 ** ent[query], 1)} keys (2 to the power of its row
          entropy).
        </>
      }
    >
      <svg viewBox={`0 0 ${W} ${H}`} className="widget-svg" role="img" aria-label="Heatmap of attention weights, queries as rows and keys as columns">
        {TOKENS.map((t, j) => (
          <text key={'c' + j} x={left + j * cell + cell / 2} y={top - 6} transform={`rotate(-50 ${left + j * cell + cell / 2} ${top - 6})`}>
            {t}
          </text>
        ))}
        {TOKENS.map((t, i) => (
          <text key={'r' + i} x={left - 6} y={top + i * cell + cell / 2 + 4} textAnchor="end" className={i === query ? 'val' : undefined}>
            {t}
          </text>
        ))}
        {weights.map((row, i) =>
          row.map((w, j) => (
            <rect
              key={`${i}-${j}`}
              x={left + j * cell}
              y={top + i * cell}
              width={cell - 1}
              height={cell - 1}
              className="heat-cell"
              style={{ fillOpacity: causal && j > i ? 0.04 : 0.08 + 0.92 * w }}
              onClick={() => setQuery(i)}
            >
              <title>{`${TOKENS[i]} -> ${TOKENS[j]}: ${w.toFixed(3)}`}</title>
            </rect>
          )),
        )}
        <rect x={left - 1} y={top + query * cell - 1} width={L * cell + 1} height={cell + 1} className="heat-row" />
      </svg>
      <div className="widget-controls grid2">
        <Select
          label="Head"
          value={pattern}
          options={[
            { value: 'random', label: 'random projections' },
            { value: 'previous', label: 'previous-token head' },
            { value: 'same', label: 'same-word head' },
          ]}
          onChange={setPattern}
        />
        <Slider label="Head dimension d" value={logD} min={2} max={9} step={1} onChange={setLogD} format={(v) => String(2 ** v)} />
        {pattern !== 'random' && <Slider label="Match strength" value={strength} min={0.5} max={8} step={0.5} onChange={setStrength} />}
        <Slider label="Query row" value={query} min={0} max={L - 1} step={1} onChange={setQuery} format={(v) => `${v}: ${TOKENS[v]}`} />
      </div>
      <div className="widget-controls">
        <Toggle label="Divide logits by sqrt(d)" checked={scaled} onChange={setScaled} />
        <Toggle label="Causal mask" checked={causal} onChange={setCausal} />
      </div>
    </Frame>
  );
}
