// Pure derivations over content + learner state: availability, percent,
// movement requirements, hours. Kept pure so they are unit-testable.
import type { Block, ContentIndex, Lesson, LessonSummary, Movement } from '../content/types';
import type { State } from './store';
import { localDate, isDue } from '../review/sm2';

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
