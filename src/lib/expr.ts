// Small expression language for derivation blanks and review answers.
// Supports + - * / ^ (or **), unary minus, parentheses, implicit products such
// as 2x or (a)(b), the constants pi and e, and a fixed set of functions.
// Equivalence is decided numerically at random points, which is what a CAS
// check reduces to for the scalar expressions used in lessons.

type Node =
  | { k: 'num'; v: number }
  | { k: 'var'; name: string }
  | { k: 'neg'; a: Node }
  | { k: 'bin'; op: string; a: Node; b: Node }
  | { k: 'call'; fn: string; args: Node[] };

const FUNCS: Record<string, (...xs: number[]) => number> = {
  exp: Math.exp,
  log: Math.log,
  ln: Math.log,
  log2: Math.log2,
  log10: Math.log10,
  sqrt: Math.sqrt,
  sin: Math.sin,
  cos: Math.cos,
  tan: Math.tan,
  tanh: Math.tanh,
  abs: Math.abs,
  sigmoid: (x: number) => 1 / (1 + Math.exp(-x)),
  max: Math.max,
  min: Math.min,
};

const CONSTS: Record<string, number> = { pi: Math.PI, e: Math.E };

interface Tok {
  t: 'num' | 'id' | 'op' | 'lp' | 'rp' | 'comma';
  v: string;
}

function tokenize(src: string): Tok[] {
  const out: Tok[] = [];
  let i = 0;
  const s = src.replace(/\*\*/g, '^').replace(/·|×/g, '*').replace(/−/g, '-');
  while (i < s.length) {
    const c = s[i];
    if (/\s/.test(c)) {
      i++;
      continue;
    }
    if (/[0-9.]/.test(c)) {
      const m = /^(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?/.exec(s.slice(i));
      if (!m) throw new Error(`Bad number at ${i}`);
      out.push({ t: 'num', v: m[0] });
      i += m[0].length;
      continue;
    }
    if (/[A-Za-z_]/.test(c)) {
      const m = /^[A-Za-z_][A-Za-z0-9_]*/.exec(s.slice(i))!;
      out.push({ t: 'id', v: m[0] });
      i += m[0].length;
      continue;
    }
    if ('+-*/^'.includes(c)) {
      out.push({ t: 'op', v: c });
      i++;
      continue;
    }
    if (c === '(' || c === '[') {
      out.push({ t: 'lp', v: '(' });
      i++;
      continue;
    }
    if (c === ')' || c === ']') {
      out.push({ t: 'rp', v: ')' });
      i++;
      continue;
    }
    if (c === ',') {
      out.push({ t: 'comma', v: ',' });
      i++;
      continue;
    }
    throw new Error(`Unexpected character "${c}"`);
  }
  return out;
}

export function parseExpr(src: string): Node {
  const toks = tokenize(src);
  let p = 0;
  const peek = () => toks[p];
  const eat = () => toks[p++];

  function primary(): Node {
    const tk = eat();
    if (!tk) throw new Error('Unexpected end of expression');
    if (tk.t === 'num') return { k: 'num', v: parseFloat(tk.v) };
    if (tk.t === 'id') {
      if (FUNCS[tk.v] && peek()?.t === 'lp') {
        eat();
        const args: Node[] = [];
        if (peek()?.t !== 'rp') {
          args.push(sum());
          while (peek()?.t === 'comma') {
            eat();
            args.push(sum());
          }
        }
        if (eat()?.t !== 'rp') throw new Error('Missing )');
        return { k: 'call', fn: tk.v, args };
      }
      return { k: 'var', name: tk.v };
    }
    if (tk.t === 'lp') {
      const n = sum();
      if (eat()?.t !== 'rp') throw new Error('Missing )');
      return n;
    }
    throw new Error(`Unexpected "${tk.v}"`);
  }

  function power(): Node {
    const base = primary();
    if (peek()?.t === 'op' && peek().v === '^') {
      eat();
      return { k: 'bin', op: '^', a: base, b: unary() };
    }
    return base;
  }

  function unary(): Node {
    if (peek()?.t === 'op' && (peek().v === '-' || peek().v === '+')) {
      const op = eat().v;
      const a = unary();
      return op === '-' ? { k: 'neg', a } : a;
    }
    return power();
  }

  function product(): Node {
    let n = unary();
    for (;;) {
      const tk = peek();
      if (tk?.t === 'op' && (tk.v === '*' || tk.v === '/')) {
        eat();
        n = { k: 'bin', op: tk.v, a: n, b: unary() };
      } else if (tk && (tk.t === 'num' || tk.t === 'id' || tk.t === 'lp')) {
        n = { k: 'bin', op: '*', a: n, b: power() };
      } else return n;
    }
  }

  function sum(): Node {
    let n = product();
    while (peek()?.t === 'op' && (peek().v === '+' || peek().v === '-')) {
      const op = eat().v;
      n = { k: 'bin', op, a: n, b: product() };
    }
    return n;
  }

  const n = sum();
  if (p !== toks.length) throw new Error(`Unexpected "${toks[p].v}"`);
  return n;
}

export function variables(n: Node, acc = new Set<string>()): Set<string> {
  switch (n.k) {
    case 'var':
      if (!(n.name in CONSTS)) acc.add(n.name);
      break;
    case 'neg':
      variables(n.a, acc);
      break;
    case 'bin':
      variables(n.a, acc);
      variables(n.b, acc);
      break;
    case 'call':
      n.args.forEach((a) => variables(a, acc));
      break;
  }
  return acc;
}

export function evaluate(n: Node, env: Record<string, number>): number {
  switch (n.k) {
    case 'num':
      return n.v;
    case 'var':
      if (n.name in env) return env[n.name];
      if (n.name in CONSTS) return CONSTS[n.name];
      throw new Error(`Unknown variable ${n.name}`);
    case 'neg':
      return -evaluate(n.a, env);
    case 'bin': {
      const a = evaluate(n.a, env);
      const b = evaluate(n.b, env);
      switch (n.op) {
        case '+':
          return a + b;
        case '-':
          return a - b;
        case '*':
          return a * b;
        case '/':
          return a / b;
        default:
          return Math.pow(a, b);
      }
    }
    case 'call':
      return FUNCS[n.fn](...n.args.map((a) => evaluate(a, env)));
  }
}

// Deterministic PRNG so checks are reproducible.
function mulberry32(seed: number) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export interface BlankSpec {
  kind: 'expr' | 'word';
  answer: string;
  tol?: number;
}

export function parseBlank(raw: string): BlankSpec {
  const [body, ...opts] = raw.split('|').map((s) => s.trim());
  let tol: number | undefined;
  for (const o of opts) {
    const m = /^tol=(.+)$/.exec(o);
    if (m) tol = parseFloat(m[1]);
  }
  if (body.startsWith('word:')) return { kind: 'word', answer: body.slice(5).trim() };
  return { kind: 'expr', answer: body, tol };
}

const norm = (s: string) => s.trim().toLowerCase().replace(/\s+/g, ' ');

export type CheckResult = { ok: boolean; error?: string };

export function checkAnswer(spec: BlankSpec, input: string): CheckResult {
  if (!input.trim()) return { ok: false, error: 'Empty answer' };
  if (spec.kind === 'word') {
    const options = spec.answer.split('/').map(norm);
    return { ok: options.includes(norm(input)) };
  }
  let target: Node;
  let given: Node;
  try {
    target = parseExpr(spec.answer);
  } catch (e) {
    return { ok: false, error: `Answer key does not parse: ${(e as Error).message}` };
  }
  try {
    given = parseExpr(input);
  } catch (e) {
    return { ok: false, error: (e as Error).message };
  }
  const vars = new Set([...variables(target), ...variables(given)]);
  const extra = [...variables(given)].filter((v) => !variables(target).has(v));
  if (extra.length) return { ok: false, error: `Unexpected symbol: ${extra.join(', ')}` };
  const rnd = mulberry32(12345);
  let valid = 0;
  for (let trial = 0; trial < 24 && valid < 8; trial++) {
    const env: Record<string, number> = {};
    for (const v of vars) env[v] = 0.3 + 1.7 * rnd();
    let a: number;
    let b: number;
    try {
      a = evaluate(target, env);
      b = evaluate(given, env);
    } catch (e) {
      return { ok: false, error: (e as Error).message };
    }
    if (!Number.isFinite(a)) continue;
    if (!Number.isFinite(b)) return { ok: false };
    const tol = spec.tol ?? (vars.size === 0 ? Math.max(1e-9, 1e-3 * Math.abs(a)) : 1e-6 * Math.max(1, Math.abs(a)));
    if (Math.abs(a - b) > tol) return { ok: false };
    valid++;
  }
  if (valid === 0) return { ok: false, error: 'Could not evaluate the answer' };
  return { ok: true };
}

export function validateBlank(raw: string): string | null {
  const spec = parseBlank(raw);
  if (spec.kind === 'word') return spec.answer ? null : 'empty word answer';
  try {
    const n = parseExpr(spec.answer);
    const res = checkAnswer(spec, spec.answer);
    if (!res.ok) return res.error ?? 'answer key fails its own check';
    void n;
    return null;
  } catch (e) {
    return (e as Error).message;
  }
}
