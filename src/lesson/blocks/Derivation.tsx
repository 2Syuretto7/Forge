import { useState } from 'react';
import type { Block } from '../../content/types';
import { checkAnswer, parseBlank } from '../../lib/expr';
import { Html } from './Html';

type D = Extract<Block, { t: 'derivation' }>;

function BlankInput({ raw, index, onSolved }: { raw: string; index: number; onSolved: () => void }) {
  const spec = parseBlank(raw);
  const [val, setVal] = useState('');
  const [state, setState] = useState<'idle' | 'ok' | 'bad' | 'shown'>('idle');
  const [msg, setMsg] = useState('');
  const [tries, setTries] = useState(0);
  const check = () => {
    const r = checkAnswer(spec, val);
    setTries((t) => t + 1);
    if (r.ok) {
      setState('ok');
      setMsg('');
      onSolved();
    } else {
      setState('bad');
      setMsg(r.error ?? 'Not equivalent to the expected expression.');
    }
  };
  return (
    <div className={`blank-row ${state}`}>
      <label>
        Blank {index + 1}:{' '}
        <input
          value={state === 'shown' ? spec.answer : val}
          onChange={(e) => {
            setVal(e.target.value);
            if (state === 'bad') setState('idle');
          }}
          onKeyDown={(e) => e.key === 'Enter' && check()}
          disabled={state === 'ok' || state === 'shown'}
          aria-invalid={state === 'bad'}
          spellCheck={false}
          placeholder={spec.kind === 'word' ? 'word or phrase' : 'expression, e.g. 2*x/(n-1)'}
        />
      </label>
      {state !== 'ok' && state !== 'shown' && (
        <button className="btn small" onClick={check} disabled={!val.trim()}>
          Check
        </button>
      )}
      {state === 'bad' && tries >= 2 && (
        <button
          className="btn small ghost"
          onClick={() => {
            setState('shown');
            onSolved();
          }}
        >
          Show answer
        </button>
      )}
      <span className="blank-msg" role="status">
        {state === 'ok' ? 'Correct' : state === 'shown' ? 'Answer shown' : msg}
      </span>
    </div>
  );
}

export function Derivation({ b }: { b: D }) {
  const [shown, setShown] = useState(1);
  const [solved, setSolved] = useState<Record<string, boolean>>({});
  const stepDone = (i: number) => b.steps[i].blanks.every((_, j) => solved[`${i}-${j}`]);
  const canAdvance = shown < b.steps.length && stepDone(shown - 1);
  return (
    <div className="card derivation">
      <div className="card-kicker">Derivation</div>
      {b.title && <h3 className="derivation-title">{b.title}</h3>}
      <ol className="steps">
        {b.steps.slice(0, shown).map((s, i) => (
          <li key={i} className="step">
            <Html html={s.html} />
            {s.blanks.map((raw, j) => (
              <BlankInput key={j} raw={raw} index={j} onSolved={() => setSolved((x) => ({ ...x, [`${i}-${j}`]: true }))} />
            ))}
          </li>
        ))}
      </ol>
      {shown < b.steps.length ? (
        <button className="btn" onClick={() => setShown((n) => n + 1)} disabled={!canAdvance}>
          {canAdvance ? `Next step (${shown + 1} of ${b.steps.length})` : 'Fill the blank to continue'}
        </button>
      ) : (
        <div className="derivation-done">Derivation complete.</div>
      )}
    </div>
  );
}
