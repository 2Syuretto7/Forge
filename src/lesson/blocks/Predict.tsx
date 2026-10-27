import { useState } from 'react';
import type { Block } from '../../content/types';
import { savePrediction, useStore } from '../../store/store';
import { Html } from './Html';

type P = Extract<Block, { t: 'predict' }>;

export function judgePrediction(b: Pick<P, 'kind' | 'answer' | 'tol'>, value: string): boolean {
  if (b.kind === 'choice') return value === b.answer;
  if (b.kind === 'numeric') {
    const v = parseFloat(value);
    const a = parseFloat(b.answer);
    if (!Number.isFinite(v)) return false;
    const tol = b.tol > 0 ? b.tol : Math.max(1e-9, 0.05 * Math.abs(a));
    return Math.abs(v - a) <= tol;
  }
  const ys = value.split(',').map(Number);
  const as = b.answer.split(',').map(Number);
  if (ys.length !== as.length) return false;
  const mae = ys.reduce((s, y, i) => s + Math.abs(y - as[i]), 0) / ys.length;
  return mae <= (b.tol || 0.15);
}

function Sketch({
  n,
  values,
  onChange,
  answer,
  xlabel,
  ylabel,
  disabled,
}: {
  n: number;
  values: number[];
  onChange?: (v: number[]) => void;
  answer?: number[];
  xlabel: string;
  ylabel: string;
  disabled: boolean;
}) {
  const W = 320;
  const H = 180;
  const pad = 28;
  const x = (i: number) => pad + (i * (W - 2 * pad)) / (n - 1);
  const y = (v: number) => H - pad - v * (H - 2 * pad);
  const [drag, setDrag] = useState<number | null>(null);
  const setAt = (i: number, v: number) => {
    const next = [...values];
    next[i] = Math.max(0, Math.min(1, Math.round(v * 100) / 100));
    onChange?.(next);
  };
  const path = (vs: number[]) => vs.map((v, i) => `${i ? 'L' : 'M'}${x(i)},${y(v)}`).join(' ');
  return (
    <svg
      viewBox={`0 0 ${W} ${H}`}
      className="sketch"
      role="group"
      aria-label={`Sketch ${ylabel} against ${xlabel}. Focus a point and use arrow keys.`}
      onPointerMove={(e) => {
        if (drag == null || disabled) return;
        const r = (e.currentTarget as SVGSVGElement).getBoundingClientRect();
        const py = ((e.clientY - r.top) / r.height) * H;
        setAt(drag, (H - pad - py) / (H - 2 * pad));
      }}
      onPointerUp={() => setDrag(null)}
      onPointerLeave={() => setDrag(null)}
    >
      <line x1={pad} y1={H - pad} x2={W - pad} y2={H - pad} className="axis" />
      <line x1={pad} y1={pad} x2={pad} y2={H - pad} className="axis" />
      <text x={W / 2} y={H - 6} textAnchor="middle" className="axis-label">
        {xlabel}
      </text>
      <text x={10} y={H / 2} textAnchor="middle" className="axis-label" transform={`rotate(-90 10 ${H / 2})`}>
        {ylabel}
      </text>
      {answer && <path d={path(answer)} className="sketch-answer" />}
      <path d={path(values)} className="sketch-line" />
      {values.map((v, i) => (
        <circle
          key={i}
          cx={x(i)}
          cy={y(v)}
          r={8}
          tabIndex={disabled ? -1 : 0}
          role="slider"
          aria-label={`Point ${i + 1}`}
          aria-valuemin={0}
          aria-valuemax={1}
          aria-valuenow={v}
          className="sketch-handle"
          onPointerDown={(e) => {
            if (disabled) return;
            (e.target as Element).setPointerCapture?.(e.pointerId);
            setDrag(i);
          }}
          onKeyDown={(e) => {
            if (disabled) return;
            if (e.key === 'ArrowUp') setAt(i, v + 0.05);
            else if (e.key === 'ArrowDown') setAt(i, v - 0.05);
            else return;
            e.preventDefault();
          }}
        />
      ))}
    </svg>
  );
}

export function Predict({ b, lessonId }: { b: P; lessonId: string }) {
  const key = `${lessonId}/${b.id}`;
  const rec = useStore((s) => s.predictions[key]);
  const n = b.kind === 'sketch' ? b.answer.split(',').length : 0;
  const [value, setValue] = useState('');
  const [sketch, setSketch] = useState<number[]>(() => Array(n).fill(0.5));
  const committed = !!rec;
  const current = b.kind === 'sketch' ? sketch.join(',') : value;

  const commit = () => {
    if (!current) return;
    void savePrediction({ id: key, value: current, correct: judgePrediction(b, current), at: Date.now() });
  };

  return (
    <div className="card predict">
      <div className="card-kicker">Predict first</div>
      <Html html={b.questionHtml} />
      {b.kind === 'choice' && (
        <fieldset className="choices" disabled={committed}>
          <legend className="sr-only">Options</legend>
          {b.options.map((o) => {
            const chosen = (rec?.value ?? value) === o.key;
            const cls = committed ? (o.key === b.answer ? 'choice correct' : chosen ? 'choice wrong' : 'choice') : 'choice';
            return (
              <label key={o.key} className={cls}>
                <input type="radio" name={key} value={o.key} checked={chosen} onChange={() => setValue(o.key)} />
                <span className="choice-key">{o.key})</span>
                <Html html={o.html} inline />
              </label>
            );
          })}
        </fieldset>
      )}
      {b.kind === 'numeric' && (
        <label className="numeric">
          Your estimate:{' '}
          <input
            type="text"
            inputMode="decimal"
            value={rec?.value ?? value}
            disabled={committed}
            onChange={(e) => setValue(e.target.value)}
          />
        </label>
      )}
      {b.kind === 'sketch' && (
        <Sketch
          n={n}
          values={rec ? rec.value.split(',').map(Number) : sketch}
          onChange={setSketch}
          answer={committed ? b.answer.split(',').map(Number) : undefined}
          xlabel={b.xlabel}
          ylabel={b.ylabel}
          disabled={committed}
        />
      )}
      {!committed ? (
        <button className="btn primary" onClick={commit} disabled={!current}>
          Commit prediction
        </button>
      ) : (
        <div className={rec.correct ? 'reveal good' : 'reveal bad'} role="status">
          <strong>{rec.correct ? 'Your prediction matched.' : 'Not quite.'}</strong>{' '}
          {b.kind === 'numeric' && <span>Answer: {b.answer}. </span>}
          {b.kind === 'sketch' && <span>The dashed curve is the actual shape. </span>}
          <Html html={b.explainHtml} />
        </div>
      )}
    </div>
  );
}
