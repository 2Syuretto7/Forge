// IndexedDB schema (EXECUTION_PLAN.md Section 8): database "forge", version 1.
import { openDB, type DBSchema, type IDBPDatabase } from 'idb';

export const SCHEMA_VERSION = 1;

export type LessonStatus = 'not_started' | 'in_progress' | 'complete';
export type ExerciseStatus = 'unseen' | 'attempted' | 'passed' | 'passed_with_solution';

export interface ProgressRec {
  lessonId: string;
  status: LessonStatus;
  movementsDone: string[];
  startedAt: number | null;
  completedAt: number | null;
  hoursLogged: number;
}

export interface ExerciseRec {
  id: string; // lessonId/exerciseId
  status: ExerciseStatus;
  attempts: number;
  failedChecks: number;
  hintsUsed: number;
  lastCode: string;
}

export interface PredictionRec {
  id: string; // lessonId/predictId
  value: string;
  correct: boolean;
  at: number;
}

export interface FeynmanRec {
  id: string; // lessonId/feynmanId
  text: string;
  scores: Record<string, number>;
  gaps: string[];
  followUp: string;
  bestTotal: number;
  submissions: number;
  selfAssessed: boolean;
  at: number;
}

export interface ReviewRec {
  itemId: string;
  ease: number;
  interval: number;
  due: string; // YYYY-MM-DD, local date
  reps: number;
  lapses: number;
  history: { at: number; grade: number }[];
}

export interface ColabRec {
  lessonId: string;
  code: string;
  verifiedAt: number;
}

export interface SettingRec {
  key: string;
  value: unknown;
}

export interface ForgeDB extends DBSchema {
  progress: { key: string; value: ProgressRec };
  exercises: { key: string; value: ExerciseRec };
  predictions: { key: string; value: PredictionRec };
  feynman: { key: string; value: FeynmanRec };
  reviews: { key: string; value: ReviewRec };
  colab: { key: string; value: ColabRec };
  settings: { key: string; value: SettingRec };
}

export type StoreName = 'progress' | 'exercises' | 'predictions' | 'feynman' | 'reviews' | 'colab' | 'settings';
export const STORE_NAMES: StoreName[] = ['progress', 'exercises', 'predictions', 'feynman', 'reviews', 'colab', 'settings'];
export const KEY_PATHS: Record<StoreName, string> = {
  progress: 'lessonId',
  exercises: 'id',
  predictions: 'id',
  feynman: 'id',
  reviews: 'itemId',
  colab: 'lessonId',
  settings: 'key',
};

let dbPromise: Promise<IDBPDatabase<ForgeDB>> | null = null;

export function getDb() {
  if (!dbPromise) {
    dbPromise = openDB<ForgeDB>('forge', SCHEMA_VERSION, {
      upgrade(db) {
        for (const s of STORE_NAMES) {
          if (!db.objectStoreNames.contains(s)) db.createObjectStore(s, { keyPath: KEY_PATHS[s] });
        }
      },
    });
  }
  return dbPromise;
}

export function resetDbHandle() {
  dbPromise = null;
}

export interface ExportFile {
  schemaVersion: number;
  app: 'forge';
  exportedAt: string;
  stores: Record<StoreName, unknown[]>;
}

export async function exportAll(): Promise<ExportFile> {
  const db = await getDb();
  const stores = {} as Record<StoreName, unknown[]>;
  for (const s of STORE_NAMES) stores[s] = await db.getAll(s);
  return { schemaVersion: SCHEMA_VERSION, app: 'forge', exportedAt: new Date().toISOString(), stores };
}

export function validateExport(data: unknown): ExportFile {
  const d = data as ExportFile;
  if (!d || typeof d !== 'object' || d.schemaVersion !== SCHEMA_VERSION || typeof d.stores !== 'object')
    throw new Error('Not a Forge progress file (schemaVersion 1 expected)');
  for (const s of STORE_NAMES) {
    if (!Array.isArray(d.stores[s])) throw new Error(`Missing store "${s}" in file`);
    for (const rec of d.stores[s]) {
      if (!rec || typeof rec !== 'object' || !(KEY_PATHS[s] in (rec as object)))
        throw new Error(`A record in "${s}" lacks its key "${KEY_PATHS[s]}"`);
    }
  }
  return d;
}

export async function importAll(data: unknown) {
  const d = validateExport(data);
  const db = await getDb();
  const tx = db.transaction(STORE_NAMES, 'readwrite');
  for (const s of STORE_NAMES) {
    const st = tx.objectStore(s);
    await st.clear();
    for (const rec of d.stores[s]) await st.put(rec as never);
  }
  await tx.done;
}

export async function clearAll(keepSettings: boolean) {
  const db = await getDb();
  const names = STORE_NAMES.filter((s) => !(keepSettings && s === 'settings'));
  const tx = db.transaction(names, 'readwrite');
  for (const s of names) await tx.objectStore(s).clear();
  await tx.done;
}
