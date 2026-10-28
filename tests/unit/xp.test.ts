import { beforeEach, describe, expect, it } from 'vitest';
import { clearAll } from '../../src/store/db';
import { completeMovement, getState, loadStore, recordCheck, recordHint, revealSolution, savePrediction, resetProgress } from '../../src/store/store';
import { XP, exerciseXpAvailable, streak, totalXp, resumeTarget } from '../../src/store/derive';
import { localDate } from '../../src/review/sm2';
import type { ContentIndex } from '../../src/content/types';

beforeEach(async () => {
  await clearAll(false);
  await loadStore();
});

describe('XP', () => {
  it('pays 100 per exercise, 30 less per hint, never below 25, and 10 with the solution', async () => {
    expect(exerciseXpAvailable(0)).toBe(100);
    expect(exerciseXpAvailable(2)).toBe(40);
    expect(exerciseXpAvailable(5)).toBe(XP.exerciseMin);
    await recordCheck('L01/e01', true, 'x');
    await recordHint('L01/e02');
    await recordCheck('L01/e02', true, 'x');
    await revealSolution('L01/e03');
    expect(totalXp(getState())).toBe(100 + 70 + 10);
  });

  it('counts predictions, movements and the lesson bonus', async () => {
    await savePrediction({ id: 'L01/p1', value: 'a', correct: true, at: Date.now() });
    await savePrediction({ id: 'L01/p2', value: 'b', correct: false, at: Date.now() });
    await completeMovement('L01', 'm0', ['m0', 'm1'], []);
    await completeMovement('L01', 'm1', ['m0', 'm1'], []);
    expect(totalXp(getState())).toBe(20 + 10 + 2 * XP.movement + XP.lesson);
  });
});

describe('streak', () => {
  it('counts consecutive active days, kept alive until the end of today', async () => {
    await recordCheck('L01/e01', false, 'x');
    const today = localDate();
    expect(getState().settings.activityDays).toEqual([today]);
    expect(streak(getState(), today)).toBe(1);
    const s = { ...getState(), settings: { ...getState().settings, activityDays: ['2026-03-01', '2026-03-02', '2026-03-04'] } };
    expect(streak(s, '2026-03-04')).toBe(1);
    expect(streak(s, '2026-03-05')).toBe(1);
    expect(streak(s, '2026-03-03')).toBe(2);
    expect(streak(s, '2026-03-07')).toBe(0);
  });

  it('is cleared with the progress', async () => {
    await recordCheck('L01/e01', true, 'x');
    await resetProgress();
    expect(streak(getState())).toBe(0);
    expect(getState().settings.lastPath).toBe('');
  });
});

describe('resume', () => {
  const idx = {
    available: ['L01', 'L02'],
    edges: [],
    lessons: [
      { id: 'L01', prereqs: [], movements: [{ id: 'm0-recall' }, { id: 'm1-puzzle' }] },
      { id: 'L02', prereqs: ['L01'], movements: [{ id: 'm0-recall' }] },
    ],
  } as unknown as ContentIndex;

  it('starts at the first open lesson, then follows the last screen visited', async () => {
    expect(resumeTarget(getState(), idx)).toEqual({ lessonId: 'L01', path: '/lesson/L01/m0-recall' });
    await completeMovement('L01', 'm0-recall', ['m0-recall', 'm1-puzzle'], []);
    expect(resumeTarget(getState(), idx)?.path).toBe('/lesson/L01/m1-puzzle');
    const s = { ...getState(), settings: { ...getState().settings, lastPath: '/lesson/L01/ex/e03' } };
    expect(resumeTarget(s, idx)?.path).toBe('/lesson/L01/ex/e03');
  });
});
