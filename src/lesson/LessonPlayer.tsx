import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useIndex, useLesson } from '../content/load';
import type { ContentIndex, Lesson, Movement } from '../content/types';
import { completeMovement, logTime, touchLesson, useStore } from '../store/store';
import { lessonComplete, lessonReviewIds, movementRequirements } from '../store/derive';
import { AnnotatedBlock, type BlockCtx } from './BlockView';
import { CodePane } from '../code/CodePane';
import { RecallBridge } from '../review/RecallBridge';
import { Meter } from './Meter';
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

function MovementBody({ lesson, index, movement, ctx }: { lesson: Lesson; index: ContentIndex; movement: Movement; ctx: BlockCtx }) {
  const state = useStore((s) => s);
  const progress = state.progress[lesson.id];
  const navigate = useNavigate();
  const reqs = movementRequirements(state, lesson, movement);
  const done = progress?.movementsDone.includes(movement.id) ?? false;
  const ready = reqs.every((r) => r.done);
  const pos = lesson.movements.findIndex((m) => m.id === movement.id);
  const next = lesson.movements[pos + 1];
  const isLast = pos === lesson.movements.length - 1;
  const notes = index.annotations.filter(
    (a) => a.target === lesson.id && a.movement === movement.id && lessonComplete(state, a.source),
  );

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
          Movement {pos} of {lesson.movements.length - 1} <span className={`tag ${movement.mode}`}>{movement.mode}</span>{' '}
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
      <footer className={styles.mfoot}>
        {reqs.length > 0 && (
          <ul className={styles.reqs} aria-label="To complete this movement">
            {reqs.map((r, i) => (
              <li key={i} className={r.done ? styles.reqDone : styles.reqTodo}>
                <span aria-hidden="true">{r.done ? '[x]' : '[ ]'}</span> {r.label}
              </li>
            ))}
          </ul>
        )}
        {done ? (
          <div className={styles.doneRow}>
            <span className="reveal good">Movement complete.</span>
            {next && (
              <Link className="btn primary" to={`/lesson/${lesson.id}/${next.id}`}>
                Next: {next.title}
              </Link>
            )}
          </div>
        ) : (
          <button className="btn primary" disabled={!ready} onClick={() => void complete()}>
            {ready ? (isLast ? 'Complete movement and lesson' : 'Complete movement') : 'Finish the items above to complete'}
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
  const [active, setActive] = useState<string | null>(null);
  const [navOpen, setNavOpen] = useState(false);
  useTimeLog(lesson?.id);

  useEffect(() => {
    if (lesson) void touchLesson(lesson.id);
  }, [lesson]);
  useEffect(() => setActive(null), [lessonId]);

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

  if (error || indexError)
    return (
      <main className="page narrow" id="main">
        <h1>{lessonId}</h1>
        <p className="reveal bad">{error ?? indexError}</p>
        <Link to="/">Back to the map</Link>
      </main>
    );
  if (!lesson || !index || !movement)
    return (
      <main className="page narrow" id="main">
        <p className="muted">Loading lesson</p>
      </main>
    );

  const ctx: BlockCtx = { lesson, index, activeExercise: active, openExercise: setActive };
  const exercise = active ? lesson.exercises[active] : null;
  const doneIds = progress?.movementsDone ?? [];

  return (
    <div className={`${styles.layout} ${exercise ? styles.withCode : ''}`}>
      <nav className={styles.nav} aria-label="Movements">
        <button className={`btn ghost ${styles.navToggle}`} onClick={() => setNavOpen((v) => !v)} aria-expanded={navOpen}>
          {lesson.id} movements
        </button>
        <div className={`${styles.navInner} ${navOpen ? styles.navOpen : ''}`}>
          <Link to="/" className={styles.back}>
            Map
          </Link>
          <div className={styles.lessonTitle}>
            <span className="muted">{lesson.id}</span> {lesson.title}
          </div>
          <Meter lesson={lesson} done={doneIds} />
          <ol className={styles.mlist}>
            {lesson.movements.map((m, i) => (
              <li key={m.id}>
                <Link
                  to={`/lesson/${lesson.id}/${m.id}`}
                  className={`${styles.mlink} ${m.id === movement.id ? styles.current : ''}`}
                  aria-current={m.id === movement.id ? 'page' : undefined}
                  onClick={() => setNavOpen(false)}
                >
                  <span className={styles.mcheck} aria-label={doneIds.includes(m.id) ? 'done' : 'not done'}>
                    {doneIds.includes(m.id) ? 'done' : i}
                  </span>
                  <span className={styles.mtitle}>{m.title}</span>
                  <span className={`tag ${m.mode}`}>{m.mode === 'both' ? 'both' : m.mode === 'theory' ? 'theory' : 'practice'}</span>
                  <span className={styles.mmin}>{m.minutes}m</span>
                </Link>
              </li>
            ))}
          </ol>
          <p className="muted small">Capstone: {lesson.capstone}</p>
        </div>
      </nav>
      <main className={styles.center} id="main">
        {prereqsDone.length > 0 && (
          <p className="banner">
            Preview: this lesson builds on {prereqsDone.join(', ')}, which you have not completed. Everything here works; the map unlocks it fully once
            those are done.
          </p>
        )}
        <MovementBody key={movement.id} lesson={lesson} index={index} movement={movement} ctx={ctx} />
      </main>
      {exercise && (
        <aside className={styles.code} aria-label="Code pane">
          <CodePane key={`${lesson.id}/${exercise.id}`} lessonId={lesson.id} exercise={exercise} onClose={() => setActive(null)} />
        </aside>
      )}
    </div>
  );
}
