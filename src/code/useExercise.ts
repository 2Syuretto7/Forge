import { useCallback, useEffect, useRef, useState } from 'react';
import type { Exercise } from '../content/types';
import { allPassed, checkCode, onStatus, runCode, warmUp } from './runner';
import type { TestResult } from './protocol';
import { exerciseOf, recordCheck, recordHint, revealSolution, saveCode, useStore } from '../store/store';

export const SOLUTION_AFTER_FAILS = 3;

// Editor state, running and checking for one exercise. With `fresh` (review
// katas) the code starts from the starter, nothing is saved, and onResult
// receives the outcome instead of the store.
export function useExercise(lessonId: string, exercise: Exercise, opts: { fresh?: boolean; onResult?: (passed: boolean) => void } = {}) {
  const { fresh, onResult } = opts;
  const key = `${lessonId}/${exercise.id}`;
  const rec = useStore((s) => s.exercises[key]);
  const [code, setCode] = useState(() => (fresh ? exercise.starter : exerciseOf(key).lastCode || exercise.starter));
  const [busy, setBusy] = useState<'run' | 'check' | null>(null);
  const [output, setOutput] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<TestResult[] | null>(null);
  const [lastRun, setLastRun] = useState<'run' | 'check' | null>(null);
  const [py, setPy] = useState({ state: 'idle', text: '' });
  const saveTimer = useRef<number | undefined>(undefined);

  useEffect(() => onStatus(setPy), []);
  useEffect(() => warmUp(), []);

  const onChange = useCallback(
    (v: string) => {
      setCode(v);
      if (fresh) return;
      window.clearTimeout(saveTimer.current);
      saveTimer.current = window.setTimeout(() => void saveCode(key, v), 600);
    },
    [key, fresh],
  );

  const run = async () => {
    if (busy) return;
    setBusy('run');
    setResults(null);
    try {
      const r = await runCode(code);
      setOutput(r.output);
      setError(r.error);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLastRun('run');
      setBusy(null);
    }
  };

  const check = async () => {
    if (busy) return;
    setBusy('check');
    setError(null);
    try {
      const r = await checkCode(code, exercise.tests);
      setOutput(r.output);
      setResults(r.results);
      if (onResult) onResult(allPassed(r.results));
      else await recordCheck(key, allPassed(r.results), code);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLastRun('check');
      setBusy(null);
    }
  };

  const failed = rec?.failedChecks ?? 0;
  const passed = rec?.status === 'passed' || rec?.status === 'passed_with_solution';
  return {
    key,
    rec,
    code,
    onChange,
    run,
    check,
    busy,
    output,
    error,
    results,
    lastRun,
    py,
    hintsShown: rec?.hintsUsed ?? 0,
    showHint: () => recordHint(key),
    failed,
    passed,
    solutionUnlocked: failed >= SOLUTION_AFTER_FAILS || passed,
    revealSolution: () => (passed ? Promise.resolve() : revealSolution(key)),
    allPassed: results ? allPassed(results) : false,
  };
}
