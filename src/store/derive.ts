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
  if (!l.prereqs.every((pr) => lessonComplete(s, pr))) return 'locked';
  if (p && (p.movementsDone.length > 0 || p.status === 'in_progress')) return 'in_progress';
  return 'available';
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
  const m = last && /^\/lesson\/(L\d\d)/.exec(last);
  if (m && !lessonComplete(s, m[1])) return { lessonId: m[1], path: last };
  const open = idx.lessons.filter((l) => idx.available.includes(l.id) && !lessonComplete(s, l.id));
  const started = open.filter((l) => s.progress[l.id]?.status === 'in_progress');
  const pick = started[0] ?? open.find((l) => nodeState(s, idx, l) === 'available') ?? open[0];
  if (!pick) return null;
  const done = s.progress[pick.id]?.movementsDone ?? [];
  const mv = pick.movements.find((x) => !done.includes(x.id)) ?? pick.movements[0];
  return { lessonId: pick.id, path: `/lesson/${pick.id}/${mv.id}` };
}
