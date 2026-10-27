import { useCallback, useEffect, useRef, useState } from 'react';
import type { Exercise } from '../content/types';
import { Editor } from './Editor';
import { allPassed, checkCode, onStatus, runCode, warmUp } from './runner';
import type { TestResult } from './protocol';
import { exerciseOf, recordCheck, recordHint, revealSolution, saveCode, useStore } from '../store/store';
import styles from './Code.module.css';

interface Props {
  lessonId: string;
  exercise: Exercise;
  onClose?: () => void;
  // Review katas start from the starter code and report the outcome.
  fresh?: boolean;
  onResult?: (passed: boolean) => void;
}

export const SOLUTION_AFTER_FAILS = 3;

export function CodePane({ lessonId, exercise, onClose, fresh, onResult }: Props) {
  const key = `${lessonId}/${exercise.id}`;
  const rec = useStore((s) => s.exercises[key]);
  const [code, setCode] = useState(() => (fresh ? exercise.starter : exerciseOf(key).lastCode || exercise.starter));
  const [busy, setBusy] = useState<'run' | 'check' | null>(null);
  const [output, setOutput] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<TestResult[] | null>(null);
  const [showSolution, setShowSolution] = useState(false);
  const [py, setPy] = useState({ state: 'idle', text: '' });
  const saveTimer = useRef<number | undefined>(undefined);

  useEffect(() => onStatus(setPy), []);
  useEffect(() => warmUp(), []);

  const onChange = useCallback(
    (v: string) => {
      setCode(v);
      if (fresh) return;
      window.clearTimeout(saveTimer.current);
      saveTimer.current = window.setTimeout(() => void saveCode(key, v), 600);
    },
    [key, fresh],
  );

  const run = async () => {
    if (busy) return;
    setBusy('run');
    setResults(null);
    try {
      const r = await runCode(code);
      setOutput(r.output);
      setError(r.error);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(null);
    }
  };

  const check = async () => {
    if (busy) return;
    setBusy('check');
    setError(null);
    try {
      const r = await checkCode(code, exercise.tests);
      setOutput(r.output);
      setResults(r.results);
      if (onResult) onResult(allPassed(r.results));
      else await recordCheck(key, allPassed(r.results), code);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(null);
    }
  };

  const hintsShown = rec?.hintsUsed ?? 0;
  const failed = rec?.failedChecks ?? 0;
  const solutionUnlocked = failed >= SOLUTION_AFTER_FAILS || rec?.status === 'passed_with_solution' || rec?.status === 'passed';
  const passed = rec?.status === 'passed' || rec?.status === 'passed_with_solution';
  const nPass = results?.filter((r) => r.status === 'pass').length ?? 0;

  return (
    <section className={styles.pane} aria-label={`Code for ${exercise.title}`}>
      <header className={styles.head}>
        <div>
          <div className={styles.kicker}>{exercise.capstone ? 'Capstone' : `Exercise ${exercise.id.replace(/^e0?/, '')}`}</div>
          <h2 className={styles.title}>{exercise.title}</h2>
        </div>
        {onClose && (
          <button className="btn ghost" onClick={onClose} aria-label="Close code pane">
            Close
          </button>
        )}
      </header>
      <div className={styles.status} aria-live="polite">
        {passed && (
          <span className={styles.badgePass}>
            {rec?.status === 'passed_with_solution' ? 'Completed with solution' : 'Passed'}
          </span>
        )}
        {py.state !== 'ready' && <span className={styles.py}>{py.text}</span>}
      </div>
      <div className={styles.editor}>
        <Editor value={code} onChange={onChange} onRun={run} onCheck={check} label={`Python editor for ${exercise.title}`} />
      </div>
      <div className={styles.actions}>
        <button className="btn" onClick={run} disabled={!!busy} title="Shift+Enter">
          {busy === 'run' ? 'Running' : 'Run'}
        </button>
        <button className="btn primary" onClick={check} disabled={!!busy} title="Ctrl/Cmd+Enter">
          {busy === 'check' ? 'Checking' : 'Check'}
        </button>
        <button
          className="btn ghost"
          onClick={() => {
            if (window.confirm('Replace your code with the starter code?')) onChange(exercise.starter);
          }}
        >
          Reset
        </button>
      </div>
      {results && (
        <div className={styles.results} role="status">
          <div className={allPassed(results) ? styles.sumPass : styles.sumFail}>
            {nPass}/{results.length} tests passed
          </div>
          <ul className={styles.testList}>
            {results.map((r) => (
              <li key={r.name} className={r.status === 'pass' ? styles.tPass : styles.tFail}>
                <span className={styles.tMark}>{r.status === 'pass' ? 'PASS' : r.status === 'skip' ? 'SKIP' : 'FAIL'}</span>
                <code>{r.name}</code>
                {r.message && <div className={styles.tMsg}>{r.message}</div>}
              </li>
            ))}
          </ul>
        </div>
      )}
      {(output || error) && (
        <pre className={styles.output} aria-label="Program output">
          {output}
          {error && <span className={styles.err}>{error}</span>}
        </pre>
      )}
      <div className={styles.help}>
        {exercise.hints.slice(0, hintsShown).map((h, i) => (
          <div key={i} className={styles.hint}>
            <strong>Hint {i + 1}.</strong> <span dangerouslySetInnerHTML={{ __html: h }} />
          </div>
        ))}
        {hintsShown < exercise.hints.length && (
          <button className="btn ghost" onClick={() => void recordHint(key)}>
            Show hint ({exercise.hints.length - hintsShown} left)
          </button>
        )}
        <button
          className="btn ghost"
          disabled={!solutionUnlocked}
          onClick={() => {
            setShowSolution((v) => !v);
            if (rec?.status !== 'passed_with_solution' && rec?.status !== 'passed') void revealSolution(key);
          }}
          title={solutionUnlocked ? '' : `Unlocks after ${SOLUTION_AFTER_FAILS} failed checks`}
        >
          {showSolution ? 'Hide solution' : solutionUnlocked ? 'Show solution' : `Solution unlocks after ${SOLUTION_AFTER_FAILS - failed} more failed checks`}
        </button>
        {showSolution && (
          <div className={styles.solution}>
            <pre>{exercise.solution}</pre>
            <button className="btn" onClick={() => onChange(exercise.solution)}>
              Load solution into editor
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
