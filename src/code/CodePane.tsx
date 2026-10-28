import { useState } from 'react';
import type { Exercise } from '../content/types';
import { Editor } from './Editor';
import { SOLUTION_AFTER_FAILS, useExercise } from './useExercise';
import { Check, Cross, Play } from '../app/icons';
import styles from './Code.module.css';

export { SOLUTION_AFTER_FAILS };

interface Props {
  lessonId: string;
  exercise: Exercise;
  // Review katas start from the starter code and report the outcome.
  fresh?: boolean;
  onResult?: (passed: boolean) => void;
}

// A compact editor and console, used for code katas in the review queue.
export function CodePane({ lessonId, exercise, fresh, onResult }: Props) {
  const w = useExercise(lessonId, exercise, { fresh, onResult });
  const [showSolution, setShowSolution] = useState(false);
  const nPass = w.results?.filter((r) => r.status === 'pass').length ?? 0;

  return (
    <section className={styles.pane} aria-label={`Code for ${exercise.title}`}>
      <div className={styles.bar}>
        <span className={styles.file}>script.py</span>
        <span className={styles.py} aria-live="polite">
          {w.py.state !== 'ready' ? w.py.text : ''}
        </span>
      </div>
      <div className={styles.editor}>
        <Editor value={w.code} onChange={w.onChange} onRun={() => void w.run()} onCheck={() => void w.check()} label={`Python editor for ${exercise.title}`} />
      </div>
      <div className={styles.actions}>
        <button
          className={`btn small ${styles.ghostDark}`}
          onClick={() => {
            if (window.confirm('Replace your code with the starter code?')) w.onChange(exercise.starter);
          }}
        >
          Reset
        </button>
        <span className={styles.spacer} />
        <button className={`btn small ${styles.ghostDark}`} onClick={() => void w.run()} disabled={!!w.busy}>
          <Play size={12} /> {w.busy === 'run' ? 'Running' : 'Run code'}
        </button>
        <button className="btn small primary" onClick={() => void w.check()} disabled={!!w.busy}>
          {w.busy === 'check' ? 'Checking' : 'Submit answer'}
        </button>
      </div>
      <div className={styles.console}>
        {w.results && (
          <div role="status">
            <div className={w.allPassed ? styles.sumPass : styles.sumFail}>
              {nPass}/{w.results.length} tests passed
            </div>
            <ul className={styles.testList}>
              {w.results.map((r) => (
                <li key={r.name} className={r.status === 'pass' ? styles.tPass : styles.tFail}>
                  <span className={styles.tMark} aria-label={r.status === 'pass' ? 'passed' : 'failed'}>
                    {r.status === 'pass' ? <Check size={12} /> : <Cross size={12} />}
                  </span>
                  <code>{r.name}</code>
                  {r.message && <div className={styles.tMsg}>{r.message}</div>}
                </li>
              ))}
            </ul>
          </div>
        )}
        {(w.output || w.error) && (
          <pre className={styles.output} aria-label="Program output">
            {w.output}
            {w.error && <span className={styles.err}>{w.error}</span>}
          </pre>
        )}
        {!w.results && !w.output && !w.error && <p className={styles.placeholder}>Run your code or submit your answer.</p>}
        {!fresh && (
          <div className={styles.help}>
            {exercise.hints.slice(0, w.hintsShown).map((h, i) => (
              <div key={i} className={styles.hint}>
                <strong>Hint {i + 1}.</strong> <span dangerouslySetInnerHTML={{ __html: h }} />
              </div>
            ))}
            {w.hintsShown < exercise.hints.length && (
              <button className={`btn small ${styles.ghostDark}`} onClick={() => void w.showHint()}>
                Take hint
              </button>
            )}
            <button
              className={`btn small ${styles.ghostDark}`}
              disabled={!w.solutionUnlocked}
              onClick={() => {
                setShowSolution((v) => !v);
                void w.revealSolution();
              }}
            >
              {showSolution ? 'Hide solution' : 'Show solution'}
            </button>
            {showSolution && <pre className={styles.output}>{exercise.solution}</pre>}
          </div>
        )}
      </div>
    </section>
  );
}
