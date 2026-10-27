// Percent-format Python -> Jupyter notebook, with learner and solved variants
// and the autograder cell of Section 5.6 appended.
import crypto from 'node:crypto';

export const COLAB_OWNER = '2Syuretto7';
export const COLAB_REPO = 'Forge';

interface Cell {
  kind: 'markdown' | 'code';
  lines: string[];
}

function splitCells(src: string): Cell[] {
  const cells: Cell[] = [];
  let cur: Cell | null = null;
  for (const line of src.replace(/\r\n/g, '\n').split('\n')) {
    const m = /^# %%(.*)$/.exec(line);
    if (m) {
      if (cur) cells.push(cur);
      cur = { kind: /\[markdown\]/.test(m[1]) ? 'markdown' : 'code', lines: [] };
      continue;
    }
    if (!cur) {
      if (line.trim() === '') continue;
      cur = { kind: 'code', lines: [] };
    }
    cur.lines.push(line);
  }
  if (cur) cells.push(cur);
  for (const c of cells) {
    while (c.lines.length && c.lines[c.lines.length - 1].trim() === '') c.lines.pop();
    while (c.lines.length && c.lines[0].trim() === '') c.lines.shift();
    if (c.kind === 'markdown') c.lines = c.lines.map((l) => l.replace(/^# ?/, ''));
  }
  return cells.filter((c) => c.lines.length);
}

export function learnerLines(lines: string[]): string[] {
  const out: string[] = [];
  let inSol = false;
  for (const line of lines) {
    const b = /^(\s*)# BEGIN SOLUTION(?:\s*->\s*(.*))?$/.exec(line);
    if (b) {
      inSol = true;
      const indent = b[1];
      const repl = b[2]?.trim();
      if (repl) out.push(...repl.split(' ;; ').map((r) => indent + r));
      else out.push(`${indent}raise NotImplementedError("Write your code here")`);
      continue;
    }
    if (/^\s*# END SOLUTION\s*$/.test(line)) {
      inSol = false;
      continue;
    }
    if (!inSol) out.push(line);
  }
  return out;
}

function solvedLines(lines: string[]): string[] {
  return lines.filter((l) => !/^\s*# (BEGIN|END) SOLUTION/.test(l));
}

export function autograderSource(id: string, tests: string): string {
  const escaped = tests.replace(/\\/g, '\\\\').replace(/'''/g, "\\'\\'\\'");
  return `# Forge autograder: run this cell last. It runs the capstone tests and prints your completion code.
import hashlib as _hashlib, sys as _sys, types as _types, unittest as _unittest
_FORGE_ID = "${id}"
_FORGE_TESTS = '''${escaped}'''
sub = _types.SimpleNamespace(**{_k: _v for _k, _v in globals().items() if not _k.startswith('_')})
_sys.modules['sub'] = sub
_ns = {'__name__': 'forge_tests'}
exec(compile(_FORGE_TESTS, 'tests.py', 'exec'), _ns)
_passed = []
for _name, _fn in list(_ns.items()):
    if _name.startswith('test_') and callable(_fn):
        try:
            _fn()
            _passed.append(_name)
            print('PASS', _name)
        except _unittest.SkipTest as _e:
            print('SKIP', _name, '-', _e)
        except Exception as _e:
            print('FAIL', _name, '-', type(_e).__name__, _e)
_digest = _hashlib.sha256(f"{_FORGE_ID}:{','.join(sorted(_passed))}:forge".encode()).hexdigest()[:8]
print(f"Completion code: FORGE-{_FORGE_ID}-{_digest}")`;
}

function cellId(seed: string) {
  return crypto.createHash('sha256').update(seed).digest('hex').slice(0, 8);
}

function toSource(lines: string[]) {
  return lines.map((l, i) => (i < lines.length - 1 ? l + '\n' : l));
}

export function buildNotebook(id: string, src: string, tests: string, variant: 'learner' | 'solved') {
  const cells = splitCells(src);
  const nbCells = cells.map((c, i) => {
    const lines = c.kind === 'code' ? (variant === 'learner' ? learnerLines(c.lines) : solvedLines(c.lines)) : c.lines;
    if (c.kind === 'markdown') {
      return { cell_type: 'markdown', id: cellId(`${id}-${i}`), metadata: {}, source: toSource(lines) };
    }
    return {
      cell_type: 'code',
      execution_count: null,
      id: cellId(`${id}-${i}`),
      metadata: {},
      outputs: [],
      source: toSource(lines),
    };
  });
  nbCells.push({
    cell_type: 'code',
    execution_count: null,
    id: cellId(`${id}-autograder`),
    metadata: { tags: ['forge-autograder'] },
    outputs: [],
    source: toSource(autograderSource(id, tests).split('\n')),
  });
  const nb = {
    cells: nbCells,
    metadata: {
      accelerator: 'GPU',
      colab: { provenance: [], gpuType: 'T4' },
      kernelspec: { display_name: 'Python 3', language: 'python', name: 'python3' },
      language_info: { name: 'python' },
    },
    nbformat: 4,
    nbformat_minor: 5,
  };
  return JSON.stringify(nb, null, 1) + '\n';
}

export function colabUrl(id: string) {
  return `https://colab.research.google.com/github/${COLAB_OWNER}/${COLAB_REPO}/blob/main/notebooks/${id}.ipynb`;
}
