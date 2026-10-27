import { useState } from 'react';
import { Link } from 'react-router-dom';
import type { Block } from '../content/types';
import { saveFeynman, useStore } from '../store/store';
import { CONCEPT_CRITERIA, DESIGN_CRITERIA, WORD_LIMITS } from './prompt';
import { gradeExplanation, type GradeResult } from './client';
import { FEYNMAN_PASS } from '../store/derive';

type F = Extract<Block, { t: 'feynman' }>;

export const wordCount = (s: string) => (s.trim() ? s.trim().split(/\s+/).length : 0);

export function Feynman({ b, lessonId, lessonTitle }: { b: F; lessonId: string; lessonTitle: string }) {
  const key = `${lessonId}/${b.id}`;
  const rec = useStore((s) => s.feynman[key]);
  const settings = useStore((s) => s.settings);
  const [text, setText] = useState(rec?.text ?? '');
  const [busy, setBusy] = useState(false);
  const [last, setLast] = useState<GradeResult | null>(null);
  const [error, setError] = useState<{ msg: string; raw?: string } | null>(null);
  const [self, setSelf] = useState<Record<string, number>>({});
  const criteria = b.rubric === 'design' ? DESIGN_CRITERIA : CONCEPT_CRITERIA;
  const [min, max] = WORD_LIMITS[b.rubric];
  const words = wordCount(text);
  const lengthOk = words >= min && words <= max;
  const hasKey = !!settings.apiKey;
  const passed = !!rec && (rec.bestTotal >= FEYNMAN_PASS || rec.submissions >= 3 || rec.selfAssessed);

  const submit = async () => {
    setBusy(true);
    setError(null);
    const out = await gradeExplanation({
      apiKey: settings.apiKey,
      model: settings.modelId,
      rubric: b.rubric,
      lessonTitle,
      prompt: b.prompt,
      keyPoints: b.keyPoints,
      text,
    });
    setBusy(false);
    if (!out.ok) {
      setError({ msg: out.error, raw: out.raw });
      return;
    }
    const r = out.result;
    setLast(r);
    const better = !rec || r.total > rec.bestTotal;
    await saveFeynman({
      id: key,
      text: better ? text : rec!.text,
      scores: better ? r.scores : rec!.scores,
      gaps: better ? r.gaps : rec!.gaps,
      followUp: better ? r.followUp : rec!.followUp,
      bestTotal: Math.max(r.total, rec?.bestTotal ?? 0),
      submissions: (rec?.submissions ?? 0) + 1,
      selfAssessed: rec?.selfAssessed ?? false,
      at: Date.now(),
    });
  };

  const submitSelf = async () => {
    const total = criteria.reduce((s, c) => s + (self[c.key] ?? 0), 0);
    await saveFeynman({
      id: key,
      text,
      scores: Object.fromEntries(criteria.map((c) => [c.key, self[c.key] ?? 0])),
      gaps: [],
      followUp: '',
      bestTotal: Math.max(total, rec?.bestTotal ?? 0),
      submissions: rec?.submissions ?? 0,
      selfAssessed: true,
      at: Date.now(),
    });
  };

  const shown = last ?? (rec && !rec.selfAssessed && rec.submissions > 0 ? { scores: rec.scores, gaps: rec.gaps, followUp: rec.followUp, total: rec.bestTotal } : null);

  return (
    <div className="card feynman">
      <div className="card-kicker">{b.rubric === 'design' ? 'Design document' : 'Explain it plainly'}</div>
      <p className="feynman-prompt">{b.prompt}</p>
      <details className="keypoints">
        <summary>What a complete answer covers ({b.keyPoints.length} points)</summary>
        <ul>
          {b.keyPoints.map((k) => (
            <li key={k}>{k}</li>
          ))}
        </ul>
      </details>
      <label className="sr-only" htmlFor={`fey-${key}`}>
        Your explanation
      </label>
      <textarea
        id={`fey-${key}`}
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={b.rubric === 'design' ? 18 : 9}
        spellCheck
      />
      <div className={`wordcount ${lengthOk ? '' : 'bad'}`}>
        {words} words (aim for {min} to {max})
      </div>
      {hasKey ? (
        <button className="btn primary" onClick={() => void submit()} disabled={busy || !lengthOk}>
          {busy ? 'Grading' : rec?.submissions ? 'Revise and resubmit' : 'Submit for feedback'}
        </button>
      ) : (
        <p className="muted">
          <Link to="/settings">Add your key in Settings to get feedback.</Link> Until then, score yourself against the rubric below.
        </p>
      )}
      {error && (
        <div className="reveal bad" role="alert">
          {error.msg}
          {error.raw && <pre className="raw">{error.raw}</pre>}
        </div>
      )}
      {shown && (
        <div className="grade" role="status">
          <table>
            <tbody>
              {criteria.map((c) => (
                <tr key={c.key}>
                  <th scope="row">{c.label}</th>
                  <td>{shown.scores[c.key] ?? 0} / 4</td>
                </tr>
              ))}
              <tr className="total">
                <th scope="row">Total</th>
                <td>
                  {shown.total} / 20 {rec && <span className="muted">(best {rec.bestTotal})</span>}
                </td>
              </tr>
            </tbody>
          </table>
          {shown.gaps.length > 0 && (
            <>
              <h4>Gaps</h4>
              <ul>
                {shown.gaps.map((g, i) => (
                  <li key={i}>{g}</li>
                ))}
              </ul>
            </>
          )}
          {shown.followUp && (
            <p>
              <strong>Follow-up question:</strong> {shown.followUp}
            </p>
          )}
        </div>
      )}
      {(!hasKey || (rec && rec.submissions >= 3)) && (
        <details className="selfassess" open={!hasKey}>
          <summary>Self-assessment against the rubric</summary>
          {criteria.map((c) => (
            <fieldset key={c.key} className="selfrow">
              <legend>
                {c.label}: <span className="muted">{c.description}</span>
              </legend>
              {[0, 1, 2, 3, 4].map((n) => (
                <label key={n}>
                  <input type="radio" name={`${key}-${c.key}`} checked={self[c.key] === n} onChange={() => setSelf((s) => ({ ...s, [c.key]: n }))} /> {n}
                </label>
              ))}
            </fieldset>
          ))}
          <button className="btn" onClick={() => void submitSelf()} disabled={words < 30 || criteria.some((c) => self[c.key] == null)}>
            Save self-assessment
          </button>
        </details>
      )}
      {passed && <p className="reveal good">This explanation counts toward completing the movement.</p>}
    </div>
  );
}
