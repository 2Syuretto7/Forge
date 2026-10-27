import { useState } from 'react';
import type { ReviewItem } from '../content/types';
import { checkAnswer, parseBlank } from '../lib/expr';
import { judgePrediction } from '../lesson/blocks/Predict';
import { Html } from '../lesson/blocks/Html';
import { useLesson } from '../content/load';
import { CodePane } from '../code/CodePane';

export const GRADE_LABELS = [
  'Blackout',
  'Wrong, but familiar',
  'Wrong, easy once seen',
  'Right, with effort',
  'Right, small hesitation',
  'Right, instantly',
];

function KataBody({ item, onChecked }: { item: ReviewItem; onChecked: (ok: boolean) => void }) {
  const { data, error } = useLesson(item.lesson);
  if (error) return <p className="reveal bad">{error}</p>;
  if (!data) return <p className="muted">Loading exercise</p>;
  const ex = data.exercises[item.exercise ?? ''];
  if (!ex) return <p className="reveal bad">Exercise not found.</p>;
  return (
    <div className="kata">
      <Html html={ex.promptHtml} />
      <div className="kata-pane">
        <CodePane lessonId={item.lesson} exercise={ex} fresh onResult={onChecked} />
      </div>
    </div>
  );
}

export function ReviewCard({ item, onGrade }: { item: ReviewItem; onGrade: (q: number) => void }) {
  const [input, setInput] = useState('');
  const [checked, setChecked] = useState<null | boolean>(null);
  const [revealed, setRevealed] = useState(false);
  const [error, setError] = useState('');

  const check = () => {
    if (item.kind === 'derivation') {
      const r = checkAnswer(parseBlank(item.answer), input);
      setChecked(r.ok);
      setError(r.ok ? '' : (r.error ?? ''));
    } else if (item.kind === 'prediction') {
      setChecked(
        judgePrediction({ kind: item.answerKind === 'choice' ? 'choice' : 'numeric', answer: item.answer, tol: item.tol ?? 0 }, input),
      );
    }
    setRevealed(true);
  };

  const suggested = checked == null ? null : checked ? 4 : 1;
  const kindLabel = { derivation: 'Re-derive', prediction: 'Predict', concept: 'Concept check', kata: 'Code kata' }[item.kind];

  return (
    <article className="card review-card" aria-label={`${kindLabel} from ${item.lesson}`}>
      <div className="card-kicker">
        {kindLabel} <span className="muted">from {item.lesson}</span>
      </div>
      {item.kind === 'kata' ? (
        <KataBody
          item={item}
          onChecked={(ok) => {
            setChecked(ok);
            setRevealed(true);
          }}
        />
      ) : (
        <Html html={item.kind === 'concept' ? `<p>${item.prompt}</p>` : item.prompt} />
      )}
      {item.kind === 'derivation' && (
        <label className="numeric">
          Fill the blank:{' '}
          <input value={input} onChange={(e) => setInput(e.target.value)} disabled={revealed} spellCheck={false} onKeyDown={(e) => e.key === 'Enter' && check()} />
        </label>
      )}
      {item.kind === 'prediction' && item.answerKind === 'choice' && (
        <fieldset className="choices" disabled={revealed}>
          <legend className="sr-only">Options</legend>
          {(item.options ?? []).map((o) => (
            <label key={o.key} className={revealed ? (o.key === item.answer ? 'choice correct' : input === o.key ? 'choice wrong' : 'choice') : 'choice'}>
              <input type="radio" name={item.id} checked={input === o.key} onChange={() => setInput(o.key)} />
              <span className="choice-key">{o.key})</span> <Html html={o.html} inline />
            </label>
          ))}
        </fieldset>
      )}
      {item.kind === 'prediction' && item.answerKind === 'numeric' && (
        <label className="numeric">
          Your estimate: <input value={input} onChange={(e) => setInput(e.target.value)} disabled={revealed} inputMode="decimal" />
        </label>
      )}
      {!revealed && item.kind !== 'kata' && (
        <div className="row">
          {item.kind === 'concept' ? (
            <button className="btn primary" onClick={() => setRevealed(true)}>
              Show answer
            </button>
          ) : (
            <button className="btn primary" onClick={check} disabled={!input.trim()}>
              Check
            </button>
          )}
        </div>
      )}
      {revealed && item.kind !== 'kata' && (
        <div className={checked === false ? 'reveal bad' : checked ? 'reveal good' : 'reveal'} role="status">
          {checked != null && <strong>{checked ? 'Correct. ' : 'Not quite. '}</strong>}
          {error && <span>{error} </span>}
          {item.kind === 'derivation' && (
            <span>
              Expected: <code>{parseBlank(item.answer).answer}</code>
            </span>
          )}
          {item.kind === 'concept' && <p>{item.answer}</p>}
          {item.kind === 'prediction' && item.answerKind === 'numeric' && <span>Answer: {item.answer}. </span>}
          {item.explain && <Html html={item.explain} />}
        </div>
      )}
      {revealed && (
        <div className="grade-row" role="group" aria-label="How well did you recall it?">
          <span className="muted">How well did you recall it?</span>
          {GRADE_LABELS.map((label, q) => (
            <button key={q} className={`btn small ${suggested === q ? 'primary' : ''}`} onClick={() => onGrade(q)} title={label}>
              {q}: {label}
            </button>
          ))}
        </div>
      )}
    </article>
  );
}

export function resolveItem(id: string, items: ReviewItem[]): ReviewItem | null {
  const found = items.find((i) => i.id === id);
  if (found) return found;
  const m = /^(L\d\d)\/kata\/(.+)$/.exec(id);
  if (m) return { id, lesson: m[1], kind: 'kata', prompt: m[2], answer: '', answerKind: 'code', exercise: m[2] };
  return null;
}
