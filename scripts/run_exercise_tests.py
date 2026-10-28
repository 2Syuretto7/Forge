"""Run every exercise's solution.py and starter.py against its tests.py.

A solution must pass every test; a starter must fail at least one.
Notebook capstones (GPU lessons) are covered by run_notebooks.py instead.
Usage: python3 scripts/run_exercise_tests.py [L01 L02 ...]
"""
import concurrent.futures as cf
import os
import sys
import time

# One BLAS thread per worker: the pool already uses every core, and nested
# BLAS threads oversubscribe them and distort the timing check.
for _var in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_var, '1')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src', 'code'))
SLOW_SECONDS = 6.0  # Pyodide is a few times slower; keep checks well under 20 s there.


def _read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def check_one(ex_dir):
    import harness  # noqa: E402  (imported per process)
    tests = _read(os.path.join(ex_dir, 'tests.py'))
    problems = []
    t0 = time.perf_counter()
    sol = harness.run_tests(_read(os.path.join(ex_dir, 'solution.py')), tests)
    elapsed = time.perf_counter() - t0
    bad = [r for r in sol if r['status'] != 'pass']
    for r in bad:
        problems.append(f"solution {r['status']}: {r['name']}: {r['message']}")
    if not sol:
        problems.append('no tests ran')
    if elapsed > SLOW_SECONDS:
        problems.append(f'solution tests took {elapsed:.1f}s (limit {SLOW_SECONDS}s)')
    starter = harness.run_tests(_read(os.path.join(ex_dir, 'starter.py')), tests)
    if all(r['status'] == 'pass' for r in starter):
        problems.append('starter passes every test (it must fail at least one)')
    return ex_dir, problems, elapsed


def find_exercises(only):
    lessons_dir = os.path.join(ROOT, 'content', 'lessons')
    out = []
    for lesson in sorted(os.listdir(lessons_dir)):
        if only and lesson not in only:
            continue
        ldir = os.path.join(lessons_dir, lesson)
        exdir = os.path.join(ldir, 'exercises')
        if os.path.isdir(exdir):
            for e in sorted(os.listdir(exdir)):
                if os.path.isdir(os.path.join(exdir, e)):
                    out.append(os.path.join(exdir, e))
        cap = os.path.join(ldir, 'capstone')
        if os.path.exists(os.path.join(cap, 'starter.py')):
            out.append(cap)
    return out


def main():
    only = set(sys.argv[1:])
    exercises = find_exercises(only)
    failures = 0
    with cf.ProcessPoolExecutor(max_workers=os.cpu_count() or 2) as pool:
        futures = {pool.submit(check_one, e): e for e in exercises}
        for fut in cf.as_completed(futures):
            ex = futures[fut]
            rel = os.path.relpath(ex, ROOT)
            try:
                _, problems, elapsed = fut.result(timeout=300)
            except Exception as exc:  # noqa: BLE001
                problems, elapsed = [f'runner crashed: {exc!r}'], 0
            if problems:
                failures += 1
                print(f'FAIL {rel} ({elapsed:.2f}s)')
                for p in problems:
                    print(f'     {p}')
    print(f'run_exercise_tests: {len(exercises) - failures}/{len(exercises)} exercises OK')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
