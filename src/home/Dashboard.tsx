import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useIndex } from '../content/load';
import type { ContentIndex, LessonSummary } from '../content/types';
import { useStore, type State } from '../store/store';
import {
  dueItems,
  exercisesSolved,
  hoursDone,
  lessonPercent,
  nodeState,
  resumeTarget,
  streak,
  totalHours,
  totalXp,
  type NodeState,
} from '../store/derive';
import { STAGE_LABEL, TRACK_LABEL } from '../graph/labels';
import { Bolt, Book, Check, Clock, Cloud, Code, Flame, Lock, Play } from '../app/icons';
import styles from './Dashboard.module.css';

const ACTION: Record<NodeState, string> = {
  available: 'Start',
  in_progress: 'Continue',
  complete: 'Review',
  locked: 'Preview',
  unpublished: '',
};

const STATUS: Record<NodeState, string> = {
  available: 'Not started',
  in_progress: 'In progress',
  complete: 'Completed',
  locked: 'Locked',
  unpublished: 'Coming later',
};

function Progress({ value, label }: { value: number; label: string }) {
  return (
    <div className={styles.progress} role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(value * 100)}>
      <div className={styles.progressFill} style={{ width: `${Math.round(value * 100)}%` }} />
    </div>
  );
}

function Resume({ state, idx }: { state: State; idx: ContentIndex }) {
  const target = resumeTarget(state, idx);
  if (!target)
    return (
      <section className={styles.hero} aria-label="Your progress">
        <div className={styles.heroText}>
          <div className={styles.kicker}>Path complete</div>
          <h2 className={styles.heroTitle}>You have finished all 24 lessons.</h2>
          <p className={styles.heroSub}>Keep your reviews going so it stays with you.</p>
        </div>
      </section>
    );
  const lesson = idx.lessons.find((l) => l.id === target.lessonId)!;
  const started = !!state.progress[lesson.id];
  const done = state.progress[lesson.id]?.movementsDone.length ?? 0;
  const mid = /\/lesson\/L\d\d\/(m\d-[a-z]+)/.exec(target.path)?.[1];
  const movement = lesson.movements.find((m) => m.id === mid);
  const onExercise = target.path.includes('/ex/');
  return (
    <section className={styles.hero} aria-label="Resume learning">
      <div className={styles.heroText}>
        <div className={styles.kicker}>{started ? 'Pick up where you left off' : 'Start here'}</div>
        <h2 className={styles.heroTitle}>
          <span className={styles.heroId}>{lesson.id}</span> {lesson.title}
        </h2>
        <p className={styles.heroSub}>
          {onExercise ? 'Back to your exercise' : movement ? movement.title : lesson.teaser}
        </p>
        <div className={styles.heroProgress}>
          <Progress value={lessonPercent(state, lesson)} label={`${lesson.id} progress`} />
          <span>
            {done} of {lesson.movements.length} steps
          </span>
        </div>
      </div>
      <Link to={target.path} className="btn primary large">
        <Play /> {started ? 'Resume' : 'Start learning'}
      </Link>
    </section>
  );
}

function Stats({ state, idx }: { state: State; idx: ContentIndex }) {
  const days = streak(state);
  const solved = exercisesSolved(state);
  return (
    <section className={styles.stats} aria-label="Your stats">
      <div className={styles.stat}>
        <span className={`${styles.statIcon} ${styles.xp}`}>
          <Bolt size={18} />
        </span>
        <div>
          <div className={styles.statValue}>{totalXp(state).toLocaleString('en-US')}</div>
          <div className={styles.statLabel}>XP earned</div>
        </div>
      </div>
      <div className={styles.stat}>
        <span className={`${styles.statIcon} ${styles.streak}`}>
          <Flame size={18} />
        </span>
        <div>
          <div className={styles.statValue}>{days}</div>
          <div className={styles.statLabel}>day streak</div>
        </div>
      </div>
      <div className={styles.stat}>
        <span className={`${styles.statIcon} ${styles.code}`}>
          <Code size={18} />
        </span>
        <div>
          <div className={styles.statValue}>{solved}</div>
          <div className={styles.statLabel}>exercises solved</div>
        </div>
      </div>
      <div className={styles.stat}>
        <span className={`${styles.statIcon} ${styles.clock}`}>
          <Clock size={18} />
        </span>
        <div>
          <div className={styles.statValue}>
            {Math.round(hoursDone(state, idx) * 10) / 10}
            <span className={styles.statOf}> / {totalHours(idx)} h</span>
          </div>
          <div className={styles.statLabel}>path completed</div>
        </div>
      </div>
    </section>
  );
}

function LessonRow({ l, state, idx }: { l: LessonSummary; state: State; idx: ContentIndex }) {
  const st = nodeState(state, idx, l);
  const pct = lessonPercent(state, l);
  const done = state.progress[l.id]?.movementsDone.length ?? 0;
  return (
    <li className={`${styles.lesson} ${styles['s_' + st]}`}>
      <span className={styles.badge} aria-hidden="true">
        {st === 'complete' ? <Check size={18} /> : st === 'locked' ? <Lock size={16} /> : l.id.slice(1)}
      </span>
      <div className={styles.lessonBody}>
        <div className={styles.lessonTop}>
          {st === 'unpublished' ? (
            <span className={styles.lessonTitle}>{l.title}</span>
          ) : (
            <Link to={`/lesson/${l.id}`} className={styles.lessonTitle}>
              <span className="sr-only">{l.id} </span>
              {l.title}
            </Link>
          )}
          <span className={`${styles.status} ${styles['st_' + st]}`}>{STATUS[st]}</span>
        </div>
        <div className={styles.meta}>
          <span>{TRACK_LABEL[l.track]}</span>
          <span>
            <Clock size={13} /> {l.hours} h
          </span>
          <span>{l.gpu ? <><Cloud size={13} /> Colab GPU capstone</> : <><Book size={13} /> In the browser</>}</span>
          {st === 'locked' && <span>Needs {l.prereqs.filter((p) => state.progress[p]?.status !== 'complete').join(', ')}</span>}
        </div>
        {(st === 'in_progress' || st === 'complete') && (
          <div className={styles.lessonProgress}>
            <Progress value={pct} label={`${l.id} progress`} />
            <span className="muted small">
              {done}/{l.movements.length}
            </span>
          </div>
        )}
      </div>
      {st !== 'unpublished' && (
        <Link
          to={`/lesson/${l.id}`}
          className={`btn small ${st === 'in_progress' || st === 'available' ? 'primary' : 'outline'}`}
          aria-label={`${ACTION[st]} ${l.id}`}
        >
          {ACTION[st]}
        </Link>
      )}
    </li>
  );
}

function Syllabus({ state, idx }: { state: State; idx: ContentIndex }) {
  return (
    <section aria-labelledby="syllabus-h">
      <h2 id="syllabus-h" className={styles.sectionTitle}>
        Your path: 24 lessons, {totalHours(idx)} hours
      </h2>
      {idx.stages.map((s, i) => {
        const lessons = idx.lessons.filter((l) => l.stage === s);
        const complete = lessons.filter((l) => state.progress[l.id]?.status === 'complete').length;
        return (
          <section key={s} className={styles.stage} aria-labelledby={`stage-${s}`}>
            <header className={styles.stageHead}>
              <div>
                <div className={styles.kicker}>Stage {i + 1}</div>
                <h3 id={`stage-${s}`} className={styles.stageTitle}>
                  {STAGE_LABEL[s]}
                </h3>
              </div>
              <div className={styles.stageMeta}>
                <Progress value={lessons.length ? complete / lessons.length : 0} label={`${STAGE_LABEL[s]} lessons completed`} />
                <span className="muted small">
                  {complete} of {lessons.length} lessons
                </span>
              </div>
            </header>
            <ol className={styles.lessons}>
              {lessons.map((l) => (
                <LessonRow key={l.id} l={l} state={state} idx={idx} />
              ))}
            </ol>
          </section>
        );
      })}
    </section>
  );
}

export function Dashboard() {
  const { data: idx, error } = useIndex();
  const state = useStore((s) => s);
  const due = dueItems(state).length;
  useEffect(() => {
    document.title = 'Learn | Forge';
  }, []);
  if (error)
    return (
      <main className="page" id="main">
        <p className="reveal bad">{error}</p>
      </main>
    );
  if (!idx)
    return (
      <main className="page" id="main">
        <p className="muted">Loading your dashboard</p>
      </main>
    );
  return (
    <main className={styles.page} id="main">
      <h1 className={styles.title}>{state.progress && Object.keys(state.progress).length ? 'Welcome back' : 'Welcome to Forge'}</h1>
      <Resume state={state} idx={idx} />
      <div className={styles.row}>
        <Stats state={state} idx={idx} />
        {due > 0 && (
          <section className={styles.reviews} aria-label="Reviews due">
            <div>
              <div className={styles.statValue}>{due}</div>
              <div className={styles.statLabel}>review{due === 1 ? '' : 's'} due today</div>
            </div>
            <Link to="/review" className="btn accent">
              Practice now
            </Link>
          </section>
        )}
      </div>
      <Syllabus state={state} idx={idx} />
    </main>
  );
}
