// Runs every exercise solution against its tests inside Pyodide (the runtime
// learners use in the browser), and reports any failure or slow check.
// Usage: node scripts/run_pyodide_tests.mjs [L01 L02 ...]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadPyodide } from 'pyodide';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const LIMIT_S = 10; // the browser limit is 20 s; leave headroom for slower machines
const only = new Set(process.argv.slice(2));

const lock = JSON.parse(fs.readFileSync(path.join(ROOT, 'node_modules/pyodide/pyodide-lock.json'), 'utf8'));
const wheel = path.join(ROOT, 'vendor/pyodide', lock.packages.numpy.file_name);
const py = await loadPyodide({ indexURL: path.join(ROOT, 'node_modules/pyodide') + '/' });
await py.loadPackage(wheel);
py.setStdout({ batched: () => {} });
py.globals.set('_src', fs.readFileSync(path.join(ROOT, 'src/code/harness.py'), 'utf8'));
py.runPython(`
import sys, types
_m = types.ModuleType('forge_harness')
exec(compile(_src, 'harness.py', 'exec'), _m.__dict__)
sys.modules['forge_harness'] = _m
`);

const lessonsDir = path.join(ROOT, 'content/lessons');
let total = 0;
let bad = 0;
for (const lesson of fs.readdirSync(lessonsDir).sort()) {
  if (only.size && !only.has(lesson)) continue;
  const dirs = [];
  const exDir = path.join(lessonsDir, lesson, 'exercises');
  if (fs.existsSync(exDir)) for (const e of fs.readdirSync(exDir).sort()) dirs.push(path.join(exDir, e));
  const cap = path.join(lessonsDir, lesson, 'capstone');
  if (fs.existsSync(path.join(cap, 'starter.py'))) dirs.push(cap);
  for (const d of dirs) {
    total++;
    py.globals.set('_code', fs.readFileSync(path.join(d, 'solution.py'), 'utf8'));
    py.globals.set('_tests', fs.readFileSync(path.join(d, 'tests.py'), 'utf8'));
    const t0 = performance.now();
    const res = JSON.parse(py.runPython('import json, forge_harness\njson.dumps(forge_harness.run_tests(_code, _tests))'));
    const secs = (performance.now() - t0) / 1000;
    const failed = res.filter((r) => r.status !== 'pass');
    if (failed.length || secs > LIMIT_S) {
      bad++;
      console.log(`FAIL ${path.relative(ROOT, d)} (${secs.toFixed(2)} s)`);
      for (const f of failed) console.log(`     ${f.status} ${f.name}: ${f.message}`);
    }
  }
}
console.log(`run_pyodide_tests: ${total - bad}/${total} exercises OK in Pyodide`);
process.exit(bad ? 1 : 0);
