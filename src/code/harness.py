# Forge exercise harness. Shared by the browser runner (Pyodide) and CI
# (scripts/run_exercise_tests.py), so both judge code identically.
import sys
import time
import types
import traceback
import unittest


def _short_tb(exc, filename_hint=None):
    tb = traceback.extract_tb(exc.__traceback__)
    frames = [f for f in tb if f.filename in ('<your code>', 'tests.py')]
    where = ''
    if frames:
        f = frames[-1]
        where = f' ({"your code" if f.filename == "<your code>" else "tests.py"}, line {f.lineno})'
    msg = str(exc).strip()
    name = type(exc).__name__
    if isinstance(exc, AssertionError):
        return (msg or 'assertion failed') + where
    return f'{name}: {msg}{where}' if msg else f'{name}{where}'


def load_module(code):
    mod = types.ModuleType('sub')
    mod.__file__ = '<your code>'
    sys.modules['sub'] = mod
    exec(compile(code, '<your code>', 'exec'), mod.__dict__)
    return mod


def run_tests(code, tests_src):
    """Return a list of {name, status, message, seconds} dicts."""
    results = []
    try:
        load_module(code)
    except Exception as exc:  # noqa: BLE001 - report any load failure
        return [{'name': 'load', 'status': 'error', 'message': _short_tb(exc), 'seconds': 0.0}]
    ns = {'__name__': 'forge_tests'}
    try:
        exec(compile(tests_src, 'tests.py', 'exec'), ns)
    except Exception as exc:  # noqa: BLE001
        return [{'name': 'tests', 'status': 'error', 'message': _short_tb(exc), 'seconds': 0.0}]
    for name, fn in list(ns.items()):
        if not (name.startswith('test_') and callable(fn)):
            continue
        t0 = time.perf_counter()
        try:
            fn()
            status, message = 'pass', ''
        except unittest.SkipTest as exc:
            status, message = 'skip', str(exc)
        except NotImplementedError:
            status, message = 'fail', 'NotImplementedError: function not written yet'
        except Exception as exc:  # noqa: BLE001
            status, message = 'fail', _short_tb(exc)
        results.append({'name': name, 'status': status, 'message': message,
                        'seconds': round(time.perf_counter() - t0, 3)})
    return results
