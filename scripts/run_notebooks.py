"""Execute every solved notebook in SMALL=1 CPU mode with papermill.

Fails if a notebook raises or if its autograder reports any FAIL line.
Tests that need full-scale (GPU) results raise unittest.SkipTest in SMALL mode.
Usage: python3 scripts/run_notebooks.py [L08 L11 ...]
"""
import os
import re
import subprocess
import sys
import json
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLVED = os.path.join(ROOT, 'build', 'notebooks')


def outputs_text(nb_path):
    with open(nb_path, encoding='utf-8') as f:
        nb = json.load(f)
    chunks = []
    for cell in nb['cells']:
        for out in cell.get('outputs', []):
            if 'text' in out:
                chunks.append(''.join(out['text']))
    return '\n'.join(chunks)


def main():
    only = set(sys.argv[1:])
    if not os.path.isdir(SOLVED):
        print('run_notebooks: build/notebooks missing; run npm run content first')
        sys.exit(1)
    names = sorted(n for n in os.listdir(SOLVED) if n.endswith('.ipynb'))
    if only:
        names = [n for n in names if n[:-6] in only]
    env = dict(os.environ, SMALL='1', TRITON_INTERPRET='1', PYTHONHASHSEED='0')
    failed = []
    for name in names:
        src = os.path.join(SOLVED, name)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, name)
            cmd = [sys.executable, '-m', 'papermill', src, out, '--cwd', os.path.join(ROOT, 'notebooks'),
                   '--kernel', 'python3', '--no-progress-bar']
            print(f'run_notebooks: {name}', flush=True)
            proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
            text = outputs_text(out) if os.path.exists(out) else ''
            fails = re.findall(r'^FAIL .*$', text, flags=re.M)
            code = re.search(r'Completion code: (FORGE-\w+-[0-9a-f]{8})', text)
            if proc.returncode != 0 or fails or not code:
                failed.append(name)
                print(proc.stderr[-4000:])
                for f in fails:
                    print('   ', f)
                if not code:
                    print('    no completion code printed')
            else:
                print(f'    ok, {code.group(1)} (SMALL mode)')
    print(f'run_notebooks: {len(names) - len(failed)}/{len(names)} notebooks OK')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
