import { beforeEach, describe, expect, it } from 'vitest';
import { clearAll, getDb } from '../../src/store/db';
import {
  completeMovement,
  getState,
  gradeReview,
  CURRICULUM,
  loadStore,
  openMovement,
  resetProgress,
  saveFeynman,
  scheduleReviews,
  startCurriculum,
} from '../../src/store/store';
import {
  CLOSE_AFTER_DAYS,
  FEYNMAN_PASS,
  blockingLesson,
  closure,
  dueReviewIds,
  lessonGate,
  missingPrereqs,
  nodeState,
  reviewsFirst,
} from '../../src/store/derive';
import { addDays, localDate } from '../../src/review/sm2';
import type { ContentIndex, LessonSummary } from '../../src/content/types';

const lesson = (id: string, prereqs: string[], feynman: string[] = ['f1']) =>
  ({ id, prereqs, feynman, movements: [{ id: 'm0' }, { id: 'm1' }] }) as unknown as LessonSummary;

// A small chain: M01 -> M02 -> M03, M02 -> M04, and M05 not yet published.
const idx = {
  available: ['M01', 'M02', 'M03', 'M04', 'X01'],
  lessons: [lesson('M01', []), lesson('M02', ['M01']), lesson('M03', ['M02', 'M05']), lesson('M04', ['M02']), lesson('M05', []), lesson('X01', [])],
  edges: [],
  reviews: [
    { id: 'M01/p1', lesson: 'M01' },
    { id: 'M01/p2', lesson: 'M01' },
    { id: 'M01/concept1', lesson: 'M01' },
    { id: 'M01/concept2', lesson: 'M01' },
    { id: 'M01/concept3', lesson: 'M01' },
  ],
} as unknown as ContentIndex;

const finish = async (id: string, score = 18) => {
  await completeMovement(id, 'm0', ['m0', 'm1'], []);
  await completeMovement(id, 'm1', ['m0', 'm1'], id === 'M01' ? idx.reviews.map((r) => r.id) : []);
  await saveFeynman({ id: `${id}/f1`, text: 'x', scores: {}, gaps: [], followUp: '', bestTotal: score, submissions: 1, selfAssessed: false, at: Date.now() });
};

beforeEach(async () => {
  await clearAll(false);
  await loadStore();
});

describe('rule 1: prerequisites, Feynman passes and one lesson at a time', () => {
  it('unlocks a lesson only when its published prerequisites are complete and their Feynman blocks passed', async () => {
    expect(nodeState(getState(), idx, idx.lessons[1])).toBe('locked');
    await finish('M01', FEYNMAN_PASS - 1);
    expect(missingPrereqs(getState(), idx, idx.lessons[1])).toEqual([{ id: 'M01', reason: 'feynman' }]);
    await saveFeynman({ ...getState().feynman['M01/f1'], bestTotal: FEYNMAN_PASS });
    expect(nodeState(getState(), idx, idx.lessons[1])).toBe('available');
    await finish('M02');
    // M05 is unpublished, so it does not hold M03 back.
    expect(nodeState(getState(), idx, idx.lessons[2])).toBe('available');
  });

  it('lets only one lesson be in progress', async () => {
    await finish('M01');
    await finish('M02');
    await openMovement('M03', 'm0');
    expect(getState().progress.M03.status).toBe('in_progress');
    expect(blockingLesson(getState(), idx, 'M04')).toBe('M03');
    expect(lessonGate(getState(), idx, idx.lessons[3])).toEqual({ kind: 'busy', other: 'M03' });
    expect(lessonGate(getState(), idx, idx.lessons[2])).toBeNull();
  });
});

describe('rule 2: reviews before a new movement', () => {
  it('holds a movement not yet opened while reviews are due, but never one already opened', async () => {
    await finish('M01');
    const later = addDays(localDate(), 2);
    expect(dueReviewIds(getState(), idx, later)).toHaveLength(5);
    expect(reviewsFirst(getState(), idx, 'M02', 'm0', later)).toBe(5);
    await openMovement('M02', 'm0');
    expect(reviewsFirst(getState(), idx, 'M02', 'm0', later)).toBe(0);
    expect(reviewsFirst(getState(), idx, 'M02', 'm1', later)).toBe(5);
    // Items of lessons no longer in the content never count.
    await scheduleReviews(['M99/d1/s1'], addDays(localDate(), -5));
    expect(dueReviewIds(getState(), idx, later)).toHaveLength(5);
  });
});

describe('rule 3: a lesson closes at 80% on its own cards a week after completion', () => {
  it('stays open before the week and closes once 4 of 5 cards pass after it', async () => {
    await finish('M01');
    const done = getState().progress.M01.completedAt!;
    expect(closure(getState(), idx, 'M01', done + 3 * 86_400_000)?.closed).toBe(false);
    const week = done + CLOSE_AFTER_DAYS * 86_400_000;
    const ids = idx.reviews.map((r) => r.id);
    // Grades given before the week mark do not count.
    for (const id of ids) await gradeReview(id, 5);
    expect(closure(getState(), idx, 'M01', week + 1000)?.closed).toBe(false);
    const s = getState();
    const late = (grade: number) => ({ at: week + 500, grade });
    const reviews = Object.fromEntries(
      ids.map((id, i) => [id, { ...s.reviews[id], history: [...s.reviews[id].history, late(i < 4 ? 4 : 1)] }]),
    );
    const c = closure({ ...s, reviews }, idx, 'M01', week + 1000)!;
    expect(c).toMatchObject({ closed: true, passed: 4, total: 5 });
    const fewer = Object.fromEntries(ids.map((id, i) => [id, { ...reviews[id], history: [...reviews[id].history, late(i < 3 ? 4 : 1)] }]));
    expect(closure({ ...s, reviews: fewer }, idx, 'M01', week + 1000)?.closed).toBe(false);
  });
});

describe('a new curriculum resets progress once', () => {
  it('clears progress made under an earlier curriculum, keeps the key, and does not reset again', async () => {
    const db = await getDb();
    await db.put('progress', { lessonId: 'M01', status: 'complete', movementsDone: ['m0'], startedAt: 1, completedAt: 2, hoursLogged: 3 });
    await db.put('exercises', { id: 'M01/e01', status: 'passed', attempts: 2, failedChecks: 1, hintsUsed: 0, lastCode: 'x' });
    await db.put('settings', { key: 'apiKey', value: 'sk-test' });
    await db.put('settings', { key: 'curriculum', value: 'old' });
    await loadStore();
    expect(await startCurriculum()).toBe(true);
    let s = getState();
    expect(s.progress).toEqual({});
    expect(s.exercises).toEqual({});
    expect(s.settings.apiKey).toBe('sk-test');
    expect(s.settings.curriculum).toBe(CURRICULUM);
    await openMovement('M01', 'm0');
    await loadStore();
    expect(await startCurriculum()).toBe(false);
    s = getState();
    expect(s.progress.M01.status).toBe('in_progress');
  });

  it('never resets a file the learner imports', async () => {
    const { exportProgress, importProgress } = await import('../../src/store/store');
    await openMovement('M02', 'm0');
    const file = await exportProgress();
    await resetProgress();
    await importProgress({ ...file, stores: { ...file.stores, settings: [] } });
    await loadStore();
    expect(await startCurriculum()).toBe(false);
    expect(getState().progress.M02).toBeDefined();
  });
});
