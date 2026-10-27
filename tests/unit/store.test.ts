import { beforeEach, describe, expect, it } from 'vitest';
import { exportAll, importAll, clearAll, validateExport } from '../../src/store/db';
import {
  completeMovement,
  getState,
  loadStore,
  recordCheck,
  revealSolution,
  saveColab,
  saveFeynman,
  savePrediction,
  saveSetting,
} from '../../src/store/store';

beforeEach(async () => {
  await clearAll(false);
  await loadStore();
});

describe('progress store', () => {
  it('persists across reloads', async () => {
    await recordCheck('L01/e01', true, 'x = 1');
    await loadStore();
    expect(getState().exercises['L01/e01'].status).toBe('passed');
  });

  it('completing every movement completes the lesson and schedules reviews', async () => {
    await completeMovement('L01', 'm0', ['m0', 'm1'], ['L01/p1']);
    expect(getState().progress.L01.status).toBe('in_progress');
    await completeMovement('L01', 'm1', ['m0', 'm1'], ['L01/p1']);
    expect(getState().progress.L01.status).toBe('complete');
    expect(getState().reviews['L01/p1']).toBeDefined();
  });

  it('revealing a solution marks completion and schedules a kata', async () => {
    await revealSolution('L02/e03');
    expect(getState().exercises['L02/e03'].status).toBe('passed_with_solution');
    expect(getState().reviews['L02/kata/e03']).toBeDefined();
  });

  it('export and import round-trip exactly', async () => {
    await recordCheck('L01/e01', false, 'a');
    await recordCheck('L01/e01', true, 'b');
    await savePrediction({ id: 'L01/p1', value: 'b', correct: true, at: 123 });
    await saveFeynman({
      id: 'L01/f1',
      text: 'words',
      scores: { correctness: 3 },
      gaps: ['x'],
      followUp: 'q',
      bestTotal: 15,
      submissions: 1,
      selfAssessed: false,
      at: 5,
    });
    await saveColab({ lessonId: 'L08', code: 'FORGE-L08-00000000', verifiedAt: 9 });
    await saveSetting('modelId', 'claude-sonnet-5-5');
    await completeMovement('L01', 'm0', ['m0', 'm1'], ['L01/p1']);
    const first = await exportAll();
    await clearAll(false);
    await importAll(JSON.parse(JSON.stringify(first)));
    const second = await exportAll();
    expect(second.stores).toEqual(first.stores);
    await loadStore();
    expect(getState().feynman['L01/f1'].bestTotal).toBe(15);
  });

  it('rejects files that are not Forge exports', () => {
    expect(() => validateExport({ foo: 1 })).toThrow();
    expect(() => validateExport({ schemaVersion: 1, stores: {} })).toThrow();
  });
});
