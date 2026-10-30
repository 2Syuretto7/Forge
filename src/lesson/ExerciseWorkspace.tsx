import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useIndex, useLesson } from '../content/load';
import type { Exercise, Lesson } from '../content/types';
import { Editor } from '../code/Editor';
import { SOLUTION_AFTER_FAILS, useExercise } from '../code/useExercise';
import { rememberPath, touchLesson, useStore } from '../store/store';
import { XP, exercisePassed, exerciseSteps, exerciseXp, exerciseXpAvailable, lessonGate, type ExerciseStep } from '../store/derive';
import { Html } from './blocks/Html';
import { Bolt, Bulb, Check, ChevronLeft, ChevronRight, Code, Cross, Play, Reset } from '../app/icons';
import styles from './Workspace.module.css';

type Pane = 'instructions' | 'code' | 'console';

function exerciseLabel(ex: Exercise, n: number, total: number) {
  return ex.capstone ? 'Capstone' : `Exercise ${n} of ${total}`;
}

function Workspace({ lesson, exercise, steps, pos }: { lesson: Lesson; exercise: Exercise; steps: ExerciseStep[]; pos: number }) {
  const w = useExercise(lesson.id, exercise);
  const navigate = useNavigate();
  const state = useStore((s) => s);
  const [pane, setPane] = useState<Pane>('instructions');
  const [consoleTab, setConsoleTab] = useState<'output' | 'tests'>('output');
  const [showSolution, setShowSolution] = useState(false);
  const step = steps[pos];
  const movement = lesson.movements.find((m) => m.id === step.movement)!;
  const inMovement = steps.filter((s) => s.movement === step.movement);
  const posInMovement = inMovement.findIndex((s) => s.ref === step.ref);
  const prev = inMovement[posInMovement - 1];
  const next = inMovement[posInMovement + 1];
  const movementUrl = `/lesson/${lesson.id}/${movement.id}`;
  const exUrl = (ref: string) => `/lesson/${lesson.id}/ex/${ref}`;
  const xpNow = w.passed ? exerciseXp(w.rec) : exerciseXpAvailable(w.hintsShown);
  const nPass = w.results?.filter((r) => r.status === 'pass').length ?? 0;
  const numbered = steps.filter((s) => !lesson.exercises[s.ref].capstone);
  const number = numbered.findIndex((s) => s.ref === step.ref) + 1;

  const submit = async () => {
    await w.check();
    setConsoleTab('tests');
    setPane((p) => (p === 'code' ? 'console' : p));
  };
  const runIt = async () => {
    await w.run();
    setConsoleTab('output');
    setPane((p) => (p === 'code' ? 'console' : p));
  };

  const nextLabel = next ? 'Next exercise' : `Back to ${movement.title.split(':')[0]}`;
  const goNext = () => navigate(next ? exUrl(next.ref) : movementUrl);

  return (
    <div className={styles.ws} data-pane={pane}>
      <div className={styles.paneTabs} role="tablist" aria-label="Workspace panels">
        {(['instructions', 'code', 'console'] as Pane[]).map((p) => (
          <button key={p} role="tab" aria-selected={pane === p} className={styles.paneTab} onClick={() => setPane(p)}>
            {p === 'instructions' ? 'Instructions' : p === 'code' ? 'Code' : 'Console'}
          </button>
        ))}
      </div>

      <section className={styles.instructions} aria-label="Instructions">
        <nav className={styles.crumbs} aria-label="Breadcrumb">
          <Link to={`/lesson/${lesson.id}`}>{lesson.id}</Link>
          <ChevronRight size={12} />
          <Link to={movementUrl}>{movement.title.split(':')[0]}</Link>
        </nav>
        <div className={styles.exHead}>
          <span className={styles.exKicker}>{exerciseLabel(exercise, number, numbered.length)}</span>
          <span className={`${styles.xpTag} ${w.passed ? styles.xpEarned : ''}`} title={w.passed ? 'XP earned' : 'XP available'}>
            <Bolt size={13} /> {xpNow} XP
          </span>
        </div>
        <h1 className={styles.title}>{exercise.title}</h1>
        {w.passed && (
          <div className={styles.passed} role="status">
            <Check size={16} /> {w.rec?.status === 'passed_with_solution' ? 'Completed with the solution' : 'Passed'}
          </div>
        )}
        <div className={styles.prompt}>
          <Html html={exercise.promptHtml} />
        </div>

        <section className={styles.help} aria-label="Hints and solution">
          {exercise.hints.slice(0, w.hintsShown).map((h, i) => (
            <div key={i} className={styles.hint}>
              <div className={styles.hintHead}>
                <Bulb size={15} /> Hint {i + 1}
              </div>
              <Html html={h} />
            </div>
          ))}
          <div className={styles.helpRow}>
            {w.hintsShown < exercise.hints.length && (
              <button className="btn outline small" onClick={() => void w.showHint()}>
                <Bulb size={15} /> Take hint{!w.passed && ` (-${XP.hint} XP)`}
              </button>
            )}
            <button
              className="btn outline small"
              disabled={!w.solutionUnlocked}
              onClick={() => {
                setShowSolution((v) => !v);
                void w.revealSolution();
              }}
              title={w.solutionUnlocked ? '' : `Unlocks after ${SOLUTION_AFTER_FAILS} failed submissions`}
            >
              {showSolution ? 'Hide solution' : w.solutionUnlocked ? 'Show solution' : `Solution unlocks after ${SOLUTION_AFTER_FAILS - w.failed} more failed checks`}
            </button>
          </div>
          {showSolution && (
            <div className={styles.solution}>
              <pre>{exercise.solution}</pre>
              <button className="btn small" onClick={() => w.onChange(exercise.solution)}>
                Load solution into editor
              </button>
            </div>
          )}
        </section>
      </section>

      <section className={styles.workarea} aria-label="Code">
        <div className={styles.editorWrap}>
          <div className={styles.editorBar}>
            <span className={styles.fileTab}>
              <Code size={14} /> script.py
            </span>
            <span className={styles.pyStatus} aria-live="polite">
              {w.py.state !== 'ready' ? w.py.text : ''}
            </span>
            <button
              className={styles.barBtn}
              onClick={() => {
                if (window.confirm('Replace your code with the starter code?')) w.onChange(exercise.starter);
              }}
            >
              <Reset size={14} /> Reset
            </button>
          </div>
          <div className={styles.editor}>
            <Editor value={w.code} onChange={w.onChange} onRun={() => void runIt()} onCheck={() => void submit()} label={`Python editor for ${exercise.title}`} />
          </div>
          <div className={styles.runBar}>
            <span className={styles.keys}>Shift+Enter runs, Ctrl+Enter submits</span>
            <button className={`btn ${styles.runBtn}`} onClick={() => void runIt()} disabled={!!w.busy}>
              <Play size={13} /> {w.busy === 'run' ? 'Running' : 'Run code'}
            </button>
            <button className="btn primary" onClick={() => void submit()} disabled={!!w.busy}>
              {w.busy === 'check' ? 'Checking' : 'Submit answer'}
            </button>
          </div>
        </div>

        <section className={styles.console} aria-label="Console">
          <div className={styles.consoleTabs} role="tablist" aria-label="Console views">
            <button role="tab" aria-selected={consoleTab === 'output'} className={styles.consoleTab} onClick={() => setConsoleTab('output')}>
              Output
            </button>
            <button role="tab" aria-selected={consoleTab === 'tests'} className={styles.consoleTab} onClick={() => setConsoleTab('tests')}>
              Tests{w.results ? ` ${nPass}/${w.results.length}` : ''}
            </button>
          </div>
          <div className={styles.consoleBody}>
            {consoleTab === 'output' ? (
              w.output || w.error ? (
                <pre className={styles.out} aria-label="Program output">
                  {w.output}
                  {w.error && <span className={styles.err}>{w.error}</span>}
                </pre>
              ) : (
                <p className={styles.placeholderText}>Run your code to see its output here.</p>
              )
            ) : w.results ? (
              <div role="status">
                {w.allPassed ? (
                  <div className={styles.success}>
                    <div>
                      <strong>Correct.</strong> {nPass}/{w.results.length} tests passed
                      {w.rec?.status === 'passed' && (
                        <span className={styles.gain}>
                          <Bolt size={13} /> +{exerciseXp(w.rec)} XP
                        </span>
                      )}
                    </div>
                    <button className="btn primary small" onClick={goNext}>
                      {nextLabel} <ChevronRight size={14} />
                    </button>
                  </div>
                ) : (
                  <div className={styles.failure}>
                    <strong>Not yet.</strong> {nPass}/{w.results.length} tests passed. Read the first failure, fix it, and submit again.
                  </div>
                )}
                <ul className={styles.tests}>
                  {w.results.map((r) => (
                    <li key={r.name} className={r.status === 'pass' ? styles.tPass : styles.tFail}>
                      <span className={styles.tIcon} aria-label={r.status === 'pass' ? 'passed' : r.status === 'skip' ? 'skipped' : 'failed'}>
                        {r.status === 'pass' ? <Check size={14} /> : <Cross size={14} />}
                      </span>
                      <code>{r.name}</code>
                      {r.message && <div className={styles.tMsg}>{r.message}</div>}
                    </li>
                  ))}
                </ul>
                {(w.output || w.error) && (
                  <pre className={styles.out}>
                    {w.output}
                    {w.error && <span className={styles.err}>{w.error}</span>}
                  </pre>
                )}
              </div>
            ) : (
              <p className={styles.placeholderText}>Submit your answer to run the tests.</p>
            )}
          </div>
        </section>
      </section>

      <footer className={styles.footer}>
        <Link to={prev ? exUrl(prev.ref) : movementUrl} className="btn outline">
          <ChevronLeft size={15} /> {prev ? 'Previous' : 'Lesson'}
        </Link>
        <ol className={styles.dots} aria-label={`Exercises in ${movement.title}`}>
          {inMovement.map((s, i) => {
            const done = exercisePassed(state, lesson.id, s.ref);
            const current = s.ref === step.ref;
            return (
              <li key={s.ref}>
                <Link
                  to={exUrl(s.ref)}
                  className={`${styles.dot} ${done ? styles.dotDone : ''} ${current ? styles.dotCurrent : ''}`}
                  aria-current={current ? 'step' : undefined}
                  aria-label={`${lesson.exercises[s.ref].title}${done ? ', passed' : ''}`}
                >
                  {done ? <Check size={12} /> : i + 1}
                </Link>
              </li>
            );
          })}
        </ol>
        <button className={`btn ${w.passed ? 'primary' : 'outline'}`} onClick={goNext}>
          {nextLabel} <ChevronRight size={15} />
        </button>
      </footer>
    </div>
  );
}

export function ExerciseWorkspace() {
  const { id = '', ex = '' } = useParams();
  const lessonId = id.toUpperCase();
  const { data: lesson, error } = useLesson(lessonId);
  const { data: index } = useIndex();
  const state = useStore((s) => s);
  // Working an exercise starts its lesson only when the lesson may be started (one at a time).
  const open = !!lesson && !!index && !lessonGate(state, index, lesson);

  useEffect(() => {
    if (!lesson) return;
    document.title = `${lesson.exercises[ex]?.title ?? ex} | ${lesson.id} | Forge`;
  }, [lesson, ex]);
  useEffect(() => {
    if (!open) return;
    void touchLesson(lesson!.id);
    void rememberPath(`/lesson/${lesson!.id}/ex/${ex}`);
  }, [open, lesson, ex]);

  if (error)
    return (
      <main className="page narrow" id="main">
        <p className="reveal bad">{error}</p>
        <Link to="/">Back to your dashboard</Link>
      </main>
    );
  if (!lesson)
    return (
      <main className="page narrow" id="main">
        <p className="muted">Loading exercise</p>
      </main>
    );
  const steps = exerciseSteps(lesson);
  const pos = steps.findIndex((s) => s.ref === ex);
  const exercise = lesson.exercises[ex];
  if (!exercise || pos < 0)
    return (
      <main className="page narrow" id="main">
        <h1>Exercise not found</h1>
        <p>
          {exercise?.notebook ? 'This capstone runs in Colab; open it from the lesson.' : 'There is no such exercise in this lesson.'}{' '}
          <Link to={`/lesson/${lesson.id}`}>Back to {lesson.id}</Link>
        </p>
      </main>
    );
  return (
    <main id="main" className={styles.main}>
      <Workspace key={`${lesson.id}/${ex}`} lesson={lesson} exercise={exercise} steps={steps} pos={pos} />
    </main>
  );
}
