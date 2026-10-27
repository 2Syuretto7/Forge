// Copies the Pyodide runtime (npm package) and the vendored NumPy wheel into
// public/pyodide so the site serves Python itself, with no CDN dependency.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ROOT } from './lib/content';

const SRC = path.join(ROOT, 'node_modules', 'pyodide');
const VENDOR = path.join(ROOT, 'vendor', 'pyodide');
const OUT = path.join(ROOT, 'public', 'pyodide');
const CORE = ['pyodide.mjs', 'pyodide.asm.mjs', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json'];

fs.mkdirSync(OUT, { recursive: true });
for (const f of CORE) fs.copyFileSync(path.join(SRC, f), path.join(OUT, f));

const lock = JSON.parse(fs.readFileSync(path.join(SRC, 'pyodide-lock.json'), 'utf8'));
const numpy = lock.packages.numpy as { file_name: string; sha256: string };
const wheel = path.join(VENDOR, numpy.file_name);
if (!fs.existsSync(wheel)) {
  console.error(`setup_pyodide: ${numpy.file_name} is not in vendor/pyodide (Pyodide version changed?)`);
  process.exit(1);
}
const digest = crypto.createHash('sha256').update(fs.readFileSync(wheel)).digest('hex');
if (digest !== numpy.sha256) {
  console.error(`setup_pyodide: SHA-256 mismatch for ${numpy.file_name}`);
  process.exit(1);
}
fs.copyFileSync(wheel, path.join(OUT, numpy.file_name));
console.log(`setup_pyodide: Pyodide ${lock.info.version ?? ''} core + ${numpy.file_name}`);
