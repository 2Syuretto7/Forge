/// <reference lib="webworker" />
// Runs learner Python in Pyodide with NumPy. One worker per page; the main
// thread terminates and replaces it when a check exceeds its time limit.
import harnessSrc from './harness.py?raw';
import type { WorkerRequest, WorkerResponse } from './protocol';

interface PyodideLike {
  loadPackage(name: string): Promise<void>;
  runPython(code: string): unknown;
  globals: { set(name: string, value: unknown): void };
  setStdout(o: { batched: (s: string) => void }): void;
  setStderr(o: { batched: (s: string) => void }): void;
}

const ctx = self as unknown as DedicatedWorkerGlobalScope;
let py: PyodideLike | null = null;
let out: string[] = [];
const post = (m: WorkerResponse) => ctx.postMessage(m);

async function init(base: string) {
  post({ type: 'status', text: 'Loading Python runtime' });
  const mod = (await import(/* @vite-ignore */ `${base}pyodide/pyodide.mjs`)) as {
    loadPyodide(o: { indexURL: string }): Promise<PyodideLike>;
  };
  py = await mod.loadPyodide({ indexURL: `${base}pyodide/` });
  post({ type: 'status', text: 'Loading NumPy' });
  await py.loadPackage('numpy');
  py.setStdout({ batched: (s) => out.push(s) });
  py.setStderr({ batched: (s) => out.push(s) });
  py.globals.set('_forge_harness_src', harnessSrc);
  py.runPython(`
import sys, types
_m = types.ModuleType('forge_harness')
exec(compile(_forge_harness_src, 'harness.py', 'exec'), _m.__dict__)
sys.modules['forge_harness'] = _m
import numpy
`);
  post({ type: 'ready' });
}

ctx.onmessage = async (ev: MessageEvent<WorkerRequest>) => {
  const msg = ev.data;
  if (msg.type === 'init') {
    try {
      await init(msg.base);
    } catch (e) {
      post({ type: 'init-error', message: (e as Error).message });
    }
    return;
  }
  if (!py) return;
  out = [];
  if (msg.type === 'run') {
    py.globals.set('_forge_code', msg.code);
    const err = py.runPython(`
import traceback, types, sys
_err = None
try:
    _main = types.ModuleType('__main__')
    exec(compile(_forge_code, '<your code>', 'exec'), _main.__dict__)
except BaseException as _e:
    _tb = traceback.format_exception(type(_e), _e, _e.__traceback__)
    _err = ''.join(l for l in _tb if 'File "<exec>"' not in l)
_err
`) as string | undefined;
    post({ type: 'run-result', id: msg.id, output: out.join('\n'), error: err ?? null });
  } else if (msg.type === 'check') {
    py.globals.set('_forge_code', msg.code);
    py.globals.set('_forge_tests', msg.tests);
    const json = py.runPython(`
import json, forge_harness
json.dumps(forge_harness.run_tests(_forge_code, _forge_tests))
`) as string;
    post({ type: 'check-result', id: msg.id, output: out.join('\n'), results: JSON.parse(json) });
  }
};
