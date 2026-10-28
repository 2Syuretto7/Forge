import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useIndex, useLesson } from '../content/load';
import type { ContentIndex, Lesson, Movement } from '../content/types';
import { completeMovement, logTime, rememberPath, touchLesson, useStore } from '../store/store';
import { exercisePassed, exerciseSteps, lessonComplete, lessonReviewIds, movementRequirements } from '../store/derive';
import { AnnotatedBlock, type BlockCtx } from './BlockView';
import { RecallBridge } from '../review/RecallBridge';
import { Meter } from './Meter';
import { Check, ChevronLeft, ChevronRight, Code, Cross, Menu } from '../app/icons';
import styles from './Lesson.module.css';

function useTimeLog(lessonId: string | undefined) {
  useEffect(() => {
    if (!lessonId) return;
    const t = window.setInterval(() => {
      if (document.visibilityState === 'visible') void logTime(lessonId, 1 / 60);
    }, 60_000);
    return () => window.clearInterval(t);
  }, [lessonId]);
}

const MODE_LABEL = { theory: 'Theory', practice: 'Practice', both: 'Theory and practice' } as const;

function Syllabus({ lesson, current, done, onClose }: { lesson: Lesson; current: string; done: string[]; onClose: () => void }) {
  const state = useStore((s) => s);
  const steps = exerciseSteps(lesson);
  return (
    <div className={styles.drawer} role="dialog" aria-modal="true" aria-label={`${lesson.id} syllabus`}>
      <div className={styles.drawerHead}>
        <div>
          <div className={styles.drawerKicker}>Syllabus</div>
          <div className={styles.drawerTitle}>
            {lesson.id}. {lesson.title}
          </div>
        </div>
        <button className="btn ghost small" onClick={onClose} aria-label="Close syllabus">
          <Cross size={16} />
        </button>
      </div>
      <Meter lesson={lesson} done={done} />
      <ol className={styles.syllabus}>
        {lesson.movements.map((m, i) => {
          const exs = steps.filter((s) => s.movement === m.id);
          const isDone = done.includes(m.id);
          return (
            <li key={m.id}>
              <Link
                to={`/lesson/${lesson.id}/${m.id}`}
                className={`${styles.sItem} ${m.id === current ? styles.sCurrent : ''}`}
                aria-current={m.id === current ? 'page' : undefined}
                onClick={onClose}
              >
                <span className={`${styles.sNum} ${isDone ? styles.sDone : ''}`} aria-label={isDone ? 'done' : 'not done'}>
                  {isDone ? <Check size={13} /> : i}
                </span>
                <span className={styles.sTitle}>{m.title}</span>
                <span className={styles.sMeta}>
                  {MODE_LABEL[m.mode]}, {m.minutes} min
                </span>
              </Link>
              {exs.length > 0 && (
                <ol className={styles.sExercises}>
                  {exs.map((s) => {
                    const passed = exercisePassed(state, lesson.id, s.ref);
                    return (
                      <li key={s.ref}>
                        <Link to={`/lesson/${lesson.id}/ex/${s.ref}`} className={styles.sEx} onClick={onClose}>
                          <span className={passed ? styles.sExDone : styles.sExIcon} aria-label={passed ? 'passed' : 'exercise'}>
                            {passed ? <Check size={11} /> : <Code size={11} />}
                          </span>
                          {lesson.exercises[s.ref].title}
                        </Link>
                      </li>
                    );
                  })}
                </ol>
              )}
            </li>
          );
        })}
      </ol>
      <p className="muted small">Capstone: {lesson.capstone}</p>
    </div>
  );
}

function MovementBody({ lesson, index, movement, ctx }: { lesson: Lesson; index: ContentIndex; movement: Movement; ctx: BlockCtx }) {
  const state = useStore((s) => s);
  const progress = state.progress[lesson.id];
  const navigate = useNavigate();
  const reqs = movementRequirements(state, lesson, movement);
  const done = progress?.movementsDone.includes(movement.id) ?? false;
  const ready = reqs.every((r) => r.done);
  const pos = lesson.movements.findIndex((m) => m.id === movement.id);
  const prev = lesson.movements[pos - 1];
  const next = lesson.movements[pos + 1];
  const isLast = pos === lesson.movements.length - 1;
  const notes = index.annotations.filter(
    (a) => a.target === lesson.id && a.movement === movement.id && lessonComplete(state, a.source),
  );
  const nDone = reqs.filter((r) => r.done).length;

  const complete = async () => {
    await completeMovement(
      lesson.id,
      movement.id,
      lesson.movements.map((m) => m.id),
      lessonReviewIds(index, lesson.id),
    );
    if (next) navigate(`/lesson/${lesson.id}/${next.id}`);
    window.scrollTo({ top: 0 });
  };

  return (
    <article className={styles.movement}>
      <header className={styles.mhead}>
        <div className={styles.kicker}>
          <span>
            Step {pos + 1} of {lesson.movements.length}
          </span>
          <span className={`tag ${movement.mode}`}>{MODE_LABEL[movement.mode]}</span>
          <span className="muted">{movement.minutes} min</span>
        </div>
        <h1>{movement.title}</h1>
      </header>
      {pos === 0 && (
        <>
          <RecallBridge lesson={lesson} index={index} />
          {lesson.reuses.length > 0 && (
            <ul className="chips" aria-label="Concepts reused from earlier lessons">
              {lesson.reuses.map((r) => (
                <li key={r.from + r.concept} className="edge-chip back">
                  <Link to={`/lesson/${r.from}`}>
                    Reuses {r.from}: {r.concept}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
      {movement.blocks.map((b, i) => (
        <AnnotatedBlock key={i} b={b} ctx={ctx} notes={notes.filter((n) => n.block === i)} />
      ))}
      {isLast && lesson.hooks.length > 0 && (
        <section className="card hooks" aria-label="Where this goes next">
          <div className="card-kicker">Where this goes next</div>
          <ul>
            {lesson.hooks.map((h) => (
              <li key={h.to}>
                <strong>{h.to}</strong>: {h.text}
              </li>
            ))}
          </ul>
        </section>
      )}
      {reqs.length > 0 && (
        <section className={styles.checklist} aria-label="To complete this step">
          <div className={styles.checkHead}>
            To complete this step <span className="muted">{nDone} of {reqs.length} done</span>
          </div>
          <ul className={styles.reqs}>
            {reqs.map((r, i) => (
              <li key={i} className={r.done ? styles.reqDone : styles.reqTodo}>
                <span className={styles.reqBox} aria-hidden="true">
                  {r.done && <Check size={12} />}
                </span>
                <span className="sr-only">{r.done ? 'Done: ' : 'To do: '}</span>
                {r.label}
              </li>
            ))}
          </ul>
        </section>
      )}
      <footer className={styles.bottomBar}>
        {prev ? (
          <Link className="btn outline" to={`/lesson/${lesson.id}/${prev.id}`} aria-label={`Back: ${prev.title}`}>
            <ChevronLeft size={15} /> Back
          </Link>
        ) : (
          <Link className="btn outline" to="/">
            <ChevronLeft size={15} /> Dashboard
          </Link>
        )}
        <div className={styles.barMid}>
          {done ? (
            <span className={styles.barDone}>
              <Check size={14} /> Movement complete.
            </span>
          ) : reqs.length > 0 ? (
            <span className="muted">
              {nDone} of {reqs.length} tasks done
            </span>
          ) : (
            <span className="muted">Read, then continue</span>
          )}
        </div>
        {done ? (
          next ? (
            <Link className="btn primary" to={`/lesson/${lesson.id}/${next.id}`}>
              Next: {next.title.split(':')[0]} <ChevronRight size={15} />
            </Link>
          ) : (
            <Link className="btn primary" to="/">
              Back to dashboard <ChevronRight size={15} />
            </Link>
          )
        ) : (
          <button className="btn primary" disabled={!ready} onClick={() => void complete()}>
            {ready ? (isLast ? 'Complete movement and lesson' : 'Complete movement') : 'Finish the tasks to continue'}
          </button>
        )}
      </footer>
    </article>
  );
}

export function LessonPlayer() {
  const { id = '', movement: movementParam } = useParams();
  const lessonId = id.toUpperCase();
  const { data: index, error: indexError } = useIndex();
  const { data: lesson, error } = useLesson(lessonId);
  const progress = useStore((s) => s.progress[lessonId]);
  const state = useStore((s) => s);
  const prereqsDone = lesson ? lesson.prereqs.filter((p) => !lessonComplete(state, p)) : [];
  const [navOpen, setNavOpen] = useState(false);
  useTimeLog(lesson?.id);

  useEffect(() => {
    if (lesson) void touchLesson(lesson.id);
  }, [lesson]);

  const movement = useMemo(() => {
    if (!lesson) return null;
    const byParam = lesson.movements.find((m) => m.id === movementParam);
    if (byParam) return byParam;
    const firstOpen = lesson.movements.find((m) => !progress?.movementsDone.includes(m.id));
    return firstOpen ?? lesson.movements[0];
  }, [lesson, movementParam, progress]);

  useEffect(() => {
    document.title = lesson ? `${lesson.id} ${lesson.title} | Forge` : 'Forge';
  }, [lesson]);
  useEffect(() => {
    if (lesson && movement) void rememberPath(`/lesson/${lesson.id}/${movement.id}`);
  }, [lesson, movement]);
  useEffect(() => {
    if (!navOpen) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setNavOpen(false);
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [navOpen]);

  if (error || indexError)
    return (
      <main className="page narrow" id="main">
        <h1>{lessonId}</h1>
        <p className="reveal bad">{error ?? indexError}</p>
        <Link to="/">Back to your dashboard</Link>
      </main>
    );
  if (!lesson || !index || !movement)
    return (
      <main className="page narrow" id="main">
        <p className="muted">Loading lesson</p>
      </main>
    );

  const numbered = exerciseSteps(lesson).filter((s) => !lesson.exercises[s.ref].capstone);
  const ctx: BlockCtx = { lesson, index, exerciseNumber: (ref) => numbered.findIndex((s) => s.ref === ref) + 1 };
  const doneIds = progress?.movementsDone ?? [];

  return (
    <div className={styles.page}>
      <div className={styles.lessonBar}>
        <button className={`btn ghost small ${styles.syllabusBtn}`} onClick={() => setNavOpen(true)} aria-expanded={navOpen}>
          <Menu size={16} /> Syllabus
        </button>
        <div className={styles.lessonName}>
          <span className={styles.lessonId}>{lesson.id}</span> <span className={styles.lessonTitle}>{lesson.title}</span>
        </div>
        <nav className={styles.steps} aria-label="Movements">
          <ol>
            {lesson.movements.map((m, i) => {
              const isDone = doneIds.includes(m.id);
              const current = m.id === movement.id;
              return (
                <li key={m.id}>
                  <Link
                    to={`/lesson/${lesson.id}/${m.id}`}
                    className={`${styles.step} ${isDone ? styles.stepDone : ''} ${current ? styles.stepCurrent : ''}`}
                    aria-current={current ? 'page' : undefined}
                    aria-label={`Step ${i + 1}: ${m.title}${isDone ? ', done' : ''}`}
                    title={m.title}
                  />
                </li>
              );
            })}
          </ol>
        </nav>
        <span className={styles.stepCount}>
          {doneIds.length}/{lesson.movements.length}
        </span>
      </div>
      {navOpen && (
        <>
          <div className={styles.scrim} onClick={() => setNavOpen(false)} aria-hidden="true" />
          <Syllabus lesson={lesson} current={movement.id} done={doneIds} onClose={() => setNavOpen(false)} />
        </>
      )}
      <main className={styles.center} id="main">
        {prereqsDone.length > 0 && (
          <p className="banner">
            Preview: this lesson builds on {prereqsDone.join(', ')}, which you have not completed. Everything here works; the map unlocks it fully once
            those are done.
          </p>
        )}
        <MovementBody key={movement.id} lesson={lesson} index={index} movement={movement} ctx={ctx} />
      </main>
    </div>
  );
}
