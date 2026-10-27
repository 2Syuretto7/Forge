// Main-thread side of the Pyodide worker: lazy start, request routing,
// 20-second limit per check, restart after a timeout.
import type { TestResult, WorkerRequest, WorkerResponse } from './protocol';

export const CHECK_TIMEOUT_MS = 20_000;

type Status = { state: 'idle' | 'loading' | 'ready' | 'error'; text: string };
type Pending = { resolve: (v: WorkerResponse) => void; timer: number };

let worker: Worker | null = null;
let readyPromise: Promise<void> | null = null;
let status: Status = { state: 'idle', text: 'Python not started' };
const statusListeners = new Set<(s: Status) => void>();
const pending = new Map<number, Pending>();
let nextId = 1;

function setStatus(s: Status) {
  status = s;
  statusListeners.forEach((l) => l(s));
}

export function onStatus(l: (s: Status) => void) {
  statusListeners.add(l);
  l(status);
  return () => {
    statusListeners.delete(l);
  };
}

function start(): Promise<void> {
  if (readyPromise) return readyPromise;
  setStatus({ state: 'loading', text: 'Starting Python' });
  const w = new Worker(new URL('./pyodide.worker.ts', import.meta.url), { type: 'module' });
  worker = w;
  readyPromise = new Promise<void>((resolve, reject) => {
    w.onmessage = (ev: MessageEvent<WorkerResponse>) => {
      const m = ev.data;
      if (m.type === 'ready') {
        setStatus({ state: 'ready', text: 'Python ready' });
        resolve();
      } else if (m.type === 'status') setStatus({ state: 'loading', text: m.text });
      else if (m.type === 'init-error') {
        setStatus({ state: 'error', text: `Python failed to load: ${m.message}` });
        readyPromise = null;
        reject(new Error(m.message));
      } else if ('id' in m) {
        const p = pending.get(m.id);
        if (p) {
          clearTimeout(p.timer);
          pending.delete(m.id);
          p.resolve(m);
        }
      }
    };
    w.onerror = (e) => {
      setStatus({ state: 'error', text: `Python worker error: ${e.message}` });
      readyPromise = null;
      reject(new Error(e.message));
    };
  });
  const base = new URL(import.meta.env.BASE_URL, window.location.href).href;
  w.postMessage({ type: 'init', base } satisfies WorkerRequest);
  return readyPromise;
}

function restart() {
  worker?.terminate();
  worker = null;
  readyPromise = null;
  for (const [, p] of pending) clearTimeout(p.timer);
  pending.clear();
  setStatus({ state: 'idle', text: 'Python restarted after a timeout' });
  void start().catch(() => undefined);
}

export function warmUp() {
  void start().catch(() => undefined);
}

type RunOrCheck = { type: 'run'; code: string } | { type: 'check'; code: string; tests: string };

async function request(msg: RunOrCheck, timeoutMs: number) {
  await start();
  const id = nextId++;
  return new Promise<WorkerResponse | 'timeout'>((resolve) => {
    const timer = window.setTimeout(() => {
      pending.delete(id);
      resolve('timeout');
      restart();
    }, timeoutMs);
    pending.set(id, { resolve, timer });
    worker!.postMessage({ ...msg, id } as WorkerRequest);
  });
}

export async function runCode(code: string): Promise<{ output: string; error: string | null }> {
  const r = await request({ type: 'run', code }, CHECK_TIMEOUT_MS);
  if (r === 'timeout') return { output: '', error: `Stopped after ${CHECK_TIMEOUT_MS / 1000} s. Python was restarted.` };
  if (r.type !== 'run-result') throw new Error('Unexpected worker reply');
  return { output: r.output, error: r.error };
}

export async function checkCode(code: string, tests: string): Promise<{ output: string; results: TestResult[] }> {
  const r = await request({ type: 'check', code, tests }, CHECK_TIMEOUT_MS);
  if (r === 'timeout')
    return {
      output: '',
      results: [
        {
          name: 'time limit',
          status: 'error',
          message: `Check exceeded ${CHECK_TIMEOUT_MS / 1000} s (infinite loop or very slow code). Python was restarted.`,
          seconds: CHECK_TIMEOUT_MS / 1000,
        },
      ],
    };
  if (r.type !== 'check-result') throw new Error('Unexpected worker reply');
  return { output: r.output, results: r.results };
}

export function allPassed(results: TestResult[]) {
  return results.length > 0 && results.every((r) => r.status === 'pass');
}
