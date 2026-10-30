// Pure derivations over content + learner state: availability, percent,
// movement requirements, hours. Kept pure so they are unit-testable.
import type { Block, ContentIndex, Exercise, Lesson, LessonSummary, Movement } from '../content/types';
import type { State } from './store';
import type { ExerciseRec } from './db';
import { addDays, localDate, isDue } from '../review/sm2';

export const FEYNMAN_PASS = 14;

export type NodeState = 'locked' | 'available' | 'in_progress' | 'complete' | 'unpublished';

export function lessonComplete(s: State, id: string) {
  return s.progress[id]?.status === 'complete';
}

export function lessonPercent(s: State, l: LessonSummary) {
  const done = s.progress[l.id]?.movementsDone ?? [];
  if (!l.movements.length) return 0;
  return l.movements.filter((m) => done.includes(m.id)).length / l.movements.length;
}

export function nodeState(s: State, idx: ContentIndex, l: LessonSummary): NodeState {
  if (!idx.available.includes(l.id)) return 'unpublished';
  const p = s.progress[l.id];
  if (p?.status === 'complete') return 'complete';
  if (missingPrereqs(s, idx, l).length) return 'locked';
  if (p && (p.movementsDone.length > 0 || p.status === 'in_progress')) return 'in_progress';
  return 'available';
}

// ---- slow and steady (docs/math-track.md, Pedagogy) ------------------------

export const CLOSE_AFTER_DAYS = 7;
export const CLOSE_SHARE = 0.8;
export const SESSION_MINUTES = 90;
const DAY_MS = 86_400_000;

// Every Feynman block of a lesson has passed (the 14 of 20 bar, graded or self-assessed).
export function feynmanCleared(s: State, l: LessonSummary) {
  return (l.feynman ?? []).every((f) => (s.feynman[`${l.id}/${f}`]?.bestTotal ?? 0) >= FEYNMAN_PASS);
}

export interface Missing {
  id: string;
  reason: 'incomplete' | 'feynman';
}

// Rule 1: a lesson unlocks when every published prerequisite is complete and its Feynman
// blocks have passed. Lessons not yet published never block anything.
export function missingPrereqs(s: State, idx: ContentIndex, l: LessonSummary): Missing[] {
  const out: Missing[] = [];
  for (const pr of l.prereqs) {
    if (!idx.available.includes(pr)) continue;
    const pl = idx.lessons.find((x) => x.id === pr);
    if (!lessonComplete(s, pr)) out.push({ id: pr, reason: 'incomplete' });
    else if (pl && !feynmanCleared(s, pl)) out.push({ id: pr, reason: 'feynman' });
  }
  return out;
}

// Rule 1: one lesson in progress at a time. Returns the lesson that has to be finished first.
export function blockingLesson(s: State, idx: ContentIndex, id: string): string | null {
  const mine = s.progress[id];
  if (mine && mine.status !== 'not_started') return null;
  const other = idx.lessons.find(
    (l) => l.id !== id && idx.available.includes(l.id) && s.progress[l.id]?.status === 'in_progress',
  );
  return other?.id ?? null;
}

export type LessonGate = { kind: 'locked'; missing: Missing[] } | { kind: 'busy'; other: string } | null;

// Whether the learner may work through (and complete movements of) this lesson now.
export function lessonGate(s: State, idx: ContentIndex, l: LessonSummary): LessonGate {
  if (lessonComplete(s, l.id)) return null;
  const missing = missingPrereqs(s, idx, l);
  if (missing.length) return { kind: 'locked', missing };
  const other = blockingLesson(s, idx, l.id);
  return other ? { kind: 'busy', other } : null;
}

// Due reviews that still exist in the content (items of lessons no longer in it drop out).
export function dueReviewIds(s: State, idx: ContentIndex, today = localDate()) {
  const known = new Set(idx.reviews.map((r) => r.id));
  return dueItems(s, today)
    .map((r) => r.itemId)
    .filter((id) => known.has(id))
    .sort();
}

// Rule 2: a movement the learner has not opened yet opens only when no review is due.
export function reviewsFirst(s: State, idx: ContentIndex, lessonId: string, movementId: string, today = localDate()) {
  const p = s.progress[lessonId];
  if (p?.status === 'complete' || p?.movementsDone.includes(movementId) || p?.movementsOpened?.includes(movementId)) return 0;
  return dueReviewIds(s, idx, today).length;
}

export interface Closure {
  closed: boolean;
  from: number; // when the one-week check starts
  passed: number;
  total: number;
}

// Rule 3: a completed lesson closes once, a week or more after completion, at least 80%
// of its review cards have been answered correctly (grade 3 or more) in that window.
export function closure(s: State, idx: ContentIndex, id: string, now = Date.now()): Closure | null {
  const p = s.progress[id];
  if (p?.status !== 'complete') return null;
  const from = (p.completedAt ?? now) + CLOSE_AFTER_DAYS * DAY_MS;
  const items = lessonReviewIds(idx, id).filter((r) => s.reviews[r]);
  let passed = 0;
  for (const r of items) {
    const late = s.reviews[r].history.filter((h) => h.at >= from);
    if (late.length && late[late.length - 1].grade >= 3) passed += 1;
  }
  const closed = now >= from && (items.length === 0 || passed / items.length >= CLOSE_SHARE);
  return { closed, from, passed, total: items.length };
}

export function hoursDone(s: State, idx: ContentIndex) {
  let minutes = 0;
  for (const l of idx.lessons) {
    const done = s.progress[l.id]?.movementsDone ?? [];
    for (const m of l.movements) if (done.includes(m.id)) minutes += m.minutes;
  }
  return minutes / 60;
}

export function totalHours(idx: ContentIndex) {
  return idx.lessons.reduce((a, l) => a + l.hours, 0);
}

export function flatBlocks(blocks: Block[], acc: Block[] = []): Block[] {
  for (const b of blocks) {
    acc.push(b);
    if (b.t === 'aside') flatBlocks(b.blocks, acc);
  }
  return acc;
}

export interface Requirement {
  label: string;
  done: boolean;
}

export function movementRequirements(s: State, lesson: Lesson, m: Movement): Requirement[] {
  const reqs: Requirement[] = [];
  for (const b of flatBlocks(m.blocks)) {
    if (b.t === 'exercise') {
      const ex = lesson.exercises[b.ref];
      const st = s.exercises[`${lesson.id}/${b.ref}`]?.status;
      if (ex?.notebook) continue; // completed through the colab block
      reqs.push({
        label: `Exercise: ${ex?.title ?? b.ref}`,
        done: st === 'passed' || st === 'passed_with_solution',
      });
    } else if (b.t === 'predict') {
      reqs.push({ label: `Prediction ${b.id}`, done: !!s.predictions[`${lesson.id}/${b.id}`] });
    } else if (b.t === 'feynman') {
      const f = s.feynman[`${lesson.id}/${b.id}`];
      reqs.push({
        label: 'Feynman explanation',
        done: !!f && (f.bestTotal >= FEYNMAN_PASS || f.submissions >= 3 || f.selfAssessed),
      });
    } else if (b.t === 'colab') {
      reqs.push({ label: 'Colab completion code', done: !!s.colab[lesson.id] });
    }
  }
  return reqs;
}

export function lessonReviewIds(idx: ContentIndex, lessonId: string) {
  return idx.reviews.filter((r) => r.lesson === lessonId).map((r) => r.id);
}

export function dueItems(s: State, today = localDate()) {
  return Object.values(s.reviews).filter((r) => isDue(r, today));
}

export function theoryShare(l: Pick<LessonSummary, 'theoryMinutes' | 'practiceMinutes'>) {
  const t = l.theoryMinutes + l.practiceMinutes;
  return t ? l.theoryMinutes / t : 0;
}

// ---- XP, streaks and the exercise sequence ---------------------------------

// Experience points, in the spirit of DataCamp: an exercise is worth 100, each
// hint taken costs 30 (never below 25), and finishing with the solution earns 10.
export const XP = {
  exercise: 100,
  hint: 30,
  exerciseMin: 25,
  withSolution: 10,
  prediction: 10,
  predictionCorrect: 10,
  movement: 25,
  lesson: 250,
  feynman: 50,
  colab: 300,
  review: 5,
};

export function exerciseXpAvailable(hintsUsed: number) {
  return Math.max(XP.exerciseMin, XP.exercise - XP.hint * hintsUsed);
}

export function exerciseXp(rec: ExerciseRec | undefined) {
  if (!rec) return 0;
  if (rec.status === 'passed') return exerciseXpAvailable(rec.hintsUsed);
  if (rec.status === 'passed_with_solution') return XP.withSolution;
  return 0;
}

export function feynmanPassed(s: State, key: string) {
  const f = s.feynman[key];
  return !!f && (f.bestTotal >= FEYNMAN_PASS || f.submissions >= 3 || f.selfAssessed);
}

export function totalXp(s: State) {
  let xp = 0;
  for (const e of Object.values(s.exercises)) xp += exerciseXp(e);
  for (const p of Object.values(s.predictions)) xp += XP.prediction + (p.correct ? XP.predictionCorrect : 0);
  for (const p of Object.values(s.progress)) {
    xp += XP.movement * p.movementsDone.length;
    if (p.status === 'complete') xp += XP.lesson;
  }
  for (const k of Object.keys(s.feynman)) if (feynmanPassed(s, k)) xp += XP.feynman;
  xp += XP.colab * Object.keys(s.colab).length;
  for (const r of Object.values(s.reviews)) xp += XP.review * r.history.length;
  return xp;
}

// Days with any activity: recorded days plus the dates of timestamped records.
export function activeDays(s: State) {
  const days = new Set(s.settings.activityDays ?? []);
  const add = (t: number | null | undefined) => t && days.add(localDate(new Date(t)));
  for (const p of Object.values(s.predictions)) add(p.at);
  for (const f of Object.values(s.feynman)) add(f.at);
  for (const c of Object.values(s.colab)) add(c.verifiedAt);
  for (const r of Object.values(s.reviews)) for (const h of r.history) add(h.at);
  for (const p of Object.values(s.progress)) {
    add(p.startedAt);
    add(p.completedAt);
  }
  return days;
}

// Consecutive active days ending today, or ending yesterday while today is still open.
export function streak(s: State, today = localDate()) {
  const days = activeDays(s);
  let d = days.has(today) ? today : addDays(today, -1);
  let n = 0;
  while (days.has(d)) {
    n += 1;
    d = addDays(d, -1);
  }
  return n;
}

export interface ExerciseStep {
  ref: string;
  movement: string;
}

// The browser exercises of a lesson in the order they appear (notebook capstones excluded).
export function exerciseSteps(lesson: Lesson): ExerciseStep[] {
  const steps: ExerciseStep[] = [];
  for (const m of lesson.movements)
    for (const b of flatBlocks(m.blocks)) {
      const ex: Exercise | undefined = b.t === 'exercise' ? lesson.exercises[b.ref] : undefined;
      if (ex && !ex.notebook) steps.push({ ref: ex.id, movement: m.id });
    }
  return steps;
}

export function exercisePassed(s: State, lessonId: string, ref: string) {
  const st = s.exercises[`${lessonId}/${ref}`]?.status;
  return st === 'passed' || st === 'passed_with_solution';
}

export function exercisesSolved(s: State) {
  return Object.values(s.exercises).filter((e) => e.status === 'passed' || e.status === 'passed_with_solution').length;
}

// Where "Resume" goes: the last lesson screen visited, else the first unfinished
// movement of the first lesson that is open and not complete.
export function resumeTarget(s: State, idx: ContentIndex): { lessonId: string; path: string } | null {
  const last = s.settings.lastPath;
  const m = last && /^\/lesson\/([LM]\d\d)/.exec(last);
  const lastLesson = m ? idx.lessons.find((l) => l.id === m[1]) : undefined;
  // A lesson previewed while locked, or while another is in progress, is not a resume point.
  if (lastLesson && idx.available.includes(lastLesson.id) && !lessonComplete(s, lastLesson.id) && !lessonGate(s, idx, lastLesson))
    return { lessonId: lastLesson.id, path: last };
  const open = idx.lessons.filter((l) => idx.available.includes(l.id) && !lessonComplete(s, l.id));
  const started = open.filter((l) => s.progress[l.id]?.status === 'in_progress');
  const pick = started[0] ?? open.find((l) => nodeState(s, idx, l) === 'available') ?? open[0];
  if (!pick) return null;
  const done = s.progress[pick.id]?.movementsDone ?? [];
  const mv = pick.movements.find((x) => !done.includes(x.id)) ?? pick.movements[0];
  return { lessonId: pick.id, path: `/lesson/${pick.id}/${mv.id}` };
}
