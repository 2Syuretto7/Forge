// In-memory mirror of IndexedDB with write-through actions. Components read
// it synchronously through useStore(); every action persists immediately.
import { useSyncExternalStore } from 'react';
import {
  getDb,
  exportAll,
  importAll,
  clearAll,
  STORE_NAMES,
  type ColabRec,
  type ExerciseRec,
  type FeynmanRec,
  type PredictionRec,
  type ProgressRec,
  type ReviewRec,
  type StoreName,
  type ExerciseStatus,
} from './db';
import { grade as sm2Grade, localDate, newReview } from '../review/sm2';

export interface Settings {
  apiKey: string;
  modelId: string;
  theme: 'system' | 'light' | 'dark';
  // Local dates (YYYY-MM-DD) on which the learner did anything: the day streak.
  activityDays: string[];
  // The last lesson screen visited, for "Resume".
  lastPath: string;
  // The curriculum the stored progress belongs to (see startCurriculum).
  curriculum: string;
}

export const DEFAULT_MODEL = 'claude-sonnet-5-5';
export const DEFAULT_SETTINGS: Settings = { apiKey: '', modelId: DEFAULT_MODEL, theme: 'system', activityDays: [], lastPath: '', curriculum: '' };

// The math track (M01 to M38) replaced L01 to L04. At the owner's request, progress made
// under an earlier curriculum is reset once rather than carried over.
export const CURRICULUM = 'math-track-2026-10';

export interface State {
  loaded: boolean;
  progress: Record<string, ProgressRec>;
  exercises: Record<string, ExerciseRec>;
  predictions: Record<string, PredictionRec>;
  feynman: Record<string, FeynmanRec>;
  reviews: Record<string, ReviewRec>;
  colab: Record<string, ColabRec>;
  settings: Settings;
}

const empty = (): State => ({
  loaded: false,
  progress: {},
  exercises: {},
  predictions: {},
  feynman: {},
  reviews: {},
  colab: {},
  settings: { ...DEFAULT_SETTINGS },
});

let state: State = empty();
const listeners = new Set<() => void>();

function set(next: Partial<State>) {
  state = { ...state, ...next };
  listeners.forEach((l) => l());
}

export function getState() {
  return state;
}

export function subscribe(l: () => void) {
  listeners.add(l);
  return () => listeners.delete(l);
}

export function useStore<T>(selector: (s: State) => T): T {
  return useSyncExternalStore(subscribe, () => selector(state), () => selector(state));
}

export async function loadStore() {
  const db = await getDb();
  const next = empty();
  next.loaded = true;
  for (const r of await db.getAll('progress')) next.progress[r.lessonId] = r;
  for (const r of await db.getAll('exercises')) next.exercises[r.id] = r;
  for (const r of await db.getAll('predictions')) next.predictions[r.id] = r;
  for (const r of await db.getAll('feynman')) next.feynman[r.id] = r;
  for (const r of await db.getAll('reviews')) next.reviews[r.itemId] = r;
  for (const r of await db.getAll('colab')) next.colab[r.lessonId] = r;
  for (const r of await db.getAll('settings')) (next.settings as unknown as Record<string, unknown>)[r.key] = r.value;
  state = next;
  listeners.forEach((l) => l());
}

async function put<S extends StoreName>(store: S, rec: unknown) {
  const db = await getDb();
  await db.put(store, rec as never);
}

// ---- activity ------------------------------------------------------------

export async function noteActivity(today = localDate()) {
  const days = state.settings.activityDays ?? [];
  if (days.includes(today)) return;
  await saveSetting('activityDays', [...days, today]);
}

export async function rememberPath(path: string) {
  if (state.settings.lastPath === path) return;
  await saveSetting('lastPath', path);
}

// ---- progress -------------------------------------------------------------

function progressOf(lessonId: string): ProgressRec {
  return (
    state.progress[lessonId] ?? {
      lessonId,
      status: 'not_started',
      movementsDone: [],
      startedAt: null,
      completedAt: null,
      hoursLogged: 0,
    }
  );
}

// Opening a movement starts its lesson and records the movement as opened, so a review
// that falls due later does not lock the learner out of work already begun.
export async function openMovement(lessonId: string, movementId: string) {
  const p = progressOf(lessonId);
  const opened = p.movementsOpened ?? [];
  if (p.status !== 'not_started' && opened.includes(movementId)) return;
  const next: ProgressRec = {
    ...p,
    status: p.status === 'not_started' ? 'in_progress' : p.status,
    startedAt: p.startedAt ?? Date.now(),
    movementsOpened: opened.includes(movementId) ? opened : [...opened, movementId],
  };
  set({ progress: { ...state.progress, [lessonId]: next } });
  await put('progress', next);
}

export async function touchLesson(lessonId: string) {
  const p = progressOf(lessonId);
  if (p.status !== 'not_started') return;
  const next: ProgressRec = { ...p, status: 'in_progress', startedAt: Date.now() };
  set({ progress: { ...state.progress, [lessonId]: next } });
  await put('progress', next);
}

export async function logTime(lessonId: string, hours: number) {
  const p = progressOf(lessonId);
  const next: ProgressRec = {
    ...p,
    status: p.status === 'not_started' ? 'in_progress' : p.status,
    startedAt: p.startedAt ?? Date.now(),
    hoursLogged: Math.round((p.hoursLogged + hours) * 10000) / 10000,
  };
  set({ progress: { ...state.progress, [lessonId]: next } });
  await put('progress', next);
  await noteActivity();
}

export async function completeMovement(lessonId: string, movementId: string, allMovements: string[], reviewItemIds: string[]) {
  const p = progressOf(lessonId);
  const done = p.movementsDone.includes(movementId) ? p.movementsDone : [...p.movementsDone, movementId];
  const complete = allMovements.every((m) => done.includes(m));
  const next: ProgressRec = {
    ...p,
    movementsDone: done,
    status: complete ? 'complete' : 'in_progress',
    startedAt: p.startedAt ?? Date.now(),
    completedAt: complete ? (p.completedAt ?? Date.now()) : null,
  };
  // Persist before showing the movement as done, so a reload right after cannot lose it.
  await put('progress', next);
  if (complete && p.status !== 'complete') await scheduleReviews(reviewItemIds);
  set({ progress: { ...state.progress, [lessonId]: next } });
  await noteActivity();
}

// ---- exercises ------------------------------------------------------------

export function exerciseOf(id: string): ExerciseRec {
  return state.exercises[id] ?? { id, status: 'unseen', attempts: 0, failedChecks: 0, hintsUsed: 0, lastCode: '' };
}

async function saveExercise(rec: ExerciseRec) {
  set({ exercises: { ...state.exercises, [rec.id]: rec } });
  await put('exercises', rec);
}

export async function saveCode(id: string, code: string) {
  const e = exerciseOf(id);
  await saveExercise({ ...e, lastCode: code, status: e.status === 'unseen' ? 'attempted' : e.status });
}

export async function recordCheck(id: string, passed: boolean, code: string) {
  const e = exerciseOf(id);
  let status: ExerciseStatus = e.status;
  if (passed) status = e.status === 'passed_with_solution' ? 'passed_with_solution' : 'passed';
  else if (status === 'unseen') status = 'attempted';
  await saveExercise({
    ...e,
    status,
    attempts: e.attempts + 1,
    failedChecks: e.failedChecks + (passed ? 0 : 1),
    lastCode: code,
  });
  await noteActivity();
}

export async function recordHint(id: string) {
  const e = exerciseOf(id);
  await saveExercise({ ...e, hintsUsed: e.hintsUsed + 1, status: e.status === 'unseen' ? 'attempted' : e.status });
}

export async function revealSolution(id: string) {
  const e = exerciseOf(id);
  await saveExercise({ ...e, status: 'passed_with_solution' });
  // Flag for review: an exercise finished with the solution becomes a code kata.
  const [lesson, ex] = id.split('/');
  await scheduleReviews([`${lesson}/kata/${ex}`]);
}

// ---- predictions, feynman, colab -----------------------------------------

export async function savePrediction(rec: PredictionRec) {
  if (state.predictions[rec.id]) return;
  set({ predictions: { ...state.predictions, [rec.id]: rec } });
  await put('predictions', rec);
  await noteActivity();
}

export async function saveFeynman(rec: FeynmanRec) {
  set({ feynman: { ...state.feynman, [rec.id]: rec } });
  await put('feynman', rec);
  await noteActivity();
}

export async function saveColab(rec: ColabRec) {
  set({ colab: { ...state.colab, [rec.lessonId]: rec } });
  await put('colab', rec);
  await noteActivity();
}

// ---- reviews -------------------------------------------------------------

export async function scheduleReviews(itemIds: string[], today = localDate()) {
  const add: Record<string, ReviewRec> = {};
  for (const id of itemIds) if (!state.reviews[id]) add[id] = newReview(id, today);
  if (!Object.keys(add).length) return;
  set({ reviews: { ...state.reviews, ...add } });
  const db = await getDb();
  const tx = db.transaction('reviews', 'readwrite');
  for (const r of Object.values(add)) await tx.store.put(r);
  await tx.done;
}

export async function gradeReview(itemId: string, q: number, today = localDate()) {
  const rec = state.reviews[itemId] ?? newReview(itemId, today);
  const next = sm2Grade(rec, q, today);
  set({ reviews: { ...state.reviews, [itemId]: next } });
  await put('reviews', next);
  await noteActivity(today);
}

// ---- settings and data management ---------------------------------------

export async function saveSetting<K extends keyof Settings>(key: K, value: Settings[K]) {
  set({ settings: { ...state.settings, [key]: value } });
  await put('settings', { key, value });
}

export async function exportProgress() {
  return exportAll();
}

export async function importProgress(data: unknown) {
  await importAll(data);
  await loadStore();
  // An imported file is the learner's chosen state: never reset it at the next start.
  await saveSetting('curriculum', CURRICULUM);
}

export async function resetProgress() {
  await clearAll(true);
  await loadStore();
  // The key and theme stay; the streak and the resume point go with the progress.
  await saveSetting('activityDays', []);
  await saveSetting('lastPath', '');
  await saveSetting('curriculum', CURRICULUM);
}

// Run once at startup: progress stored under an earlier curriculum is reset (the API key,
// model and theme stay). Returns true when there was progress to reset.
export async function startCurriculum() {
  if (state.settings.curriculum === CURRICULUM) return false;
  const had =
    Object.keys(state.progress).length +
      Object.keys(state.exercises).length +
      Object.keys(state.predictions).length +
      Object.keys(state.feynman).length +
      Object.keys(state.reviews).length +
      Object.keys(state.colab).length >
    0;
  await resetProgress();
  return had;
}

export { STORE_NAMES };
