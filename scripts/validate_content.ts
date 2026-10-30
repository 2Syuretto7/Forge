// Enforces every content rule in EXECUTION_PLAN.md Sections 2 and 6.5, and the math-track
// rules of docs/math-track.md for lessons M01-M38.
// Usage: tsx scripts/validate_content.ts [--allow-unpublished]
//   --allow-unpublished: lessons listed in graph.yaml without content yet are shown as
//   unpublished instead of failing the build (used while a track is being written).
import fs from 'node:fs';
import path from 'node:path';
import { loadGraph, hasLesson, loadLesson, lessonDir, ROOT, type LoadedLesson, type Graph } from './lib/content';
import { collectDirectives } from './lib/markdown';
import { findAnnotations, notebookFor } from './build_content';
import { reviewItemsFor } from './gen_reviews';
import { validateBlank } from '../src/lib/expr';
import type { Block, Edge } from '../src/content/types';

const BANNED_CS = ['TODO', 'TBD'];
const BANNED_CI = ['lorem', 'coming soon', 'placeholder'];
const EMOJI = /(?:[\u{1F000}-\u{1FAFF}]|[\u{2600}-\u{27BF}]|\u{2B50}|\u{2B55}|\u{FE0F}|\u{200D})/u;

export function bannedIn(text: string): string[] {
  const hits: string[] = [];
  for (const b of BANNED_CS) if (new RegExp(`\\b${b}\\b`).test(text)) hits.push(b);
  const lower = text.toLowerCase();
  for (const b of BANNED_CI) if (lower.includes(b)) hits.push(b);
  if (EMOJI.test(text)) hits.push('emoji');
  return hits;
}

function walk(dir: string, acc: string[] = []): string[] {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    if (fs.statSync(p).isDirectory()) walk(p, acc);
    else acc.push(p);
  }
  return acc;
}

// The lessons that may start a path with no inbound edge. L02 and L03 stay roots until
// their material has moved into the math track (docs/math-track.md, Migration).
const ROOTS = ['M01', 'L02', 'L03'];

// An edge chip, hook or reuse may follow an edge in its direction, or a horizontal
// edge either way: a horizontal link is mutual.
export function linked(edges: Edge[], from: string, to: string) {
  return edges.some((e) => (e.from === from && e.to === to) || (e.type === 'horizontal' && e.from === to && e.to === from));
}

export function neighbours(edges: Edge[], id: string, dir: 'in' | 'out') {
  const s = new Set<string>();
  for (const e of edges) {
    if ((dir === 'out' ? e.from : e.to) === id) s.add(dir === 'out' ? e.to : e.from);
    if (e.type === 'horizontal' && (dir === 'out' ? e.to : e.from) === id) s.add(dir === 'out' ? e.from : e.to);
  }
  return s;
}

export function graphErrors(graph: Graph): string[] {
  const errs: string[] = [];
  const ids = new Set(graph.lessons.map((l) => l.id));
  const stageIdx = new Map(graph.stages.map((s, i) => [s, i]));
  const lessonStage = new Map(graph.lessons.map((l) => [l.id, stageIdx.get(l.stage) ?? -1]));
  const seen = new Set<string>();
  const lessonOf = new Map(graph.lessons.map((l) => [l.id, l]));
  for (const l of graph.lessons) {
    if (!graph.tracks.includes(l.track) && l.track !== 'all') errs.push(`${l.id}: unknown track ${l.track}`);
    if (!stageIdx.has(l.stage)) errs.push(`${l.id}: unknown stage ${l.stage}`);
    if (l.track === 'math' && !l.strand) errs.push(`${l.id}: math lesson without a strand`);
    if (l.strand && l.strand !== 'ALL' && !graph.strands.includes(l.strand)) errs.push(`${l.id}: unknown strand ${l.strand}`);
  }
  for (const e of graph.edges) {
    const key = `${e.from}->${e.to}`;
    const typed = `${key} (${e.type})`;
    // The same pair may be both a prerequisite and a long-range thread (M13 to M32), never twice the same type.
    if (seen.has(typed)) errs.push(`duplicate edge ${typed}`);
    seen.add(typed);
    if (!ids.has(e.from) || !ids.has(e.to)) errs.push(`edge ${key} references a missing lesson`);
    if (!['vertical', 'horizontal', 'long_range'].includes(e.type)) errs.push(`edge ${key} has bad type ${e.type}`);
    if (e.type === 'vertical' && (lessonStage.get(e.from) ?? 0) > (lessonStage.get(e.to) ?? 0))
      errs.push(`vertical edge ${key} points from a later stage to an earlier one`);
    if (e.type === 'horizontal' && lessonStage.get(e.from) !== lessonStage.get(e.to))
      errs.push(`horizontal edge ${key} crosses stages`);
    const a = lessonOf.get(e.from);
    const b = lessonOf.get(e.to);
    // Horizontal edges link different tracks, or two math lessons in different strands.
    if (e.type === 'horizontal' && a && b && a.track === b.track && !(a.track === 'math' && a.strand !== b.strand))
      errs.push(`horizontal edge ${key} stays within one track and strand`);
    if (e.type === 'long_range' && lessonStage.get(e.from) === lessonStage.get(e.to))
      errs.push(`long-range edge ${key} stays within one stage`);
  }
  // DAG check on vertical edges.
  const adj = new Map<string, string[]>();
  for (const e of graph.edges.filter((x) => x.type === 'vertical')) adj.set(e.from, [...(adj.get(e.from) ?? []), e.to]);
  const state = new Map<string, number>();
  const visit = (n: string): boolean => {
    if (state.get(n) === 1) return false;
    if (state.get(n) === 2) return true;
    state.set(n, 1);
    for (const m of adj.get(n) ?? []) if (!visit(m)) return false;
    state.set(n, 2);
    return true;
  };
  for (const id of ids) if (!visit(id)) errs.push(`vertical edges contain a cycle through ${id}`);
  const first = graph.lessons[0]?.id;
  const last = graph.lessons[graph.lessons.length - 1]?.id;
  for (const l of graph.lessons) {
    const inbound = graph.edges.filter((e) => e.to === l.id);
    const outbound = graph.edges.filter((e) => e.from === l.id);
    const roots = ROOTS;
    if (!roots.includes(l.id) && inbound.length === 0) errs.push(`${l.id}: no inbound edge`);
    if (l.id !== last && outbound.length === 0) errs.push(`${l.id}: no outbound edge`);
    if (![...inbound, ...outbound].some((e) => e.type !== 'vertical')) errs.push(`${l.id}: no horizontal or long-range edge`);
  }
  void first;
  return errs;
}

// docs/math-track.md, "Lesson template" and "Minimum density per lesson".
export function mathTrackErrors(l: LoadedLesson, graph: Graph, all: Block[]): string[] {
  const errs: string[] = [];
  const { lesson, yaml } = l;
  const id = lesson.id;
  const n = Number(id.slice(1));
  const total = yaml.movements.reduce((s, m) => s + m.minutes, 0);
  if (yaml.hours !== 10 && yaml.hours !== 12) errs.push(`${id}: math lessons are 10 or 12 hours, not ${yaml.hours}`);
  if (yaml.movements.length !== 8) errs.push(`${id}: math lessons have all eight movements`);
  if (lesson.theoryMinutes * 2 !== total) errs.push(`${id}: theory ${lesson.theoryMinutes} of ${total} minutes is not exactly half`);
  const exIds = Object.keys(lesson.exercises).filter((e) => e !== 'capstone');
  if (exIds.length < 14 || exIds.length > 16) errs.push(`${id}: ${exIds.length} exercises (math lessons have 14 to 16 plus the capstone)`);
  const prefix = n >= 15 ? 'test_grad' : 'test_invariant';
  const checked = exIds.filter((e) => lesson.exercises[e].testNames.some((t) => t.startsWith(prefix)));
  if (checked.length < 3) errs.push(`${id}: ${checked.length} exercises with a ${prefix}* check (need 3)`);
  const count = (t: Block['t']) => all.filter((b) => b.t === t).length;
  if (count('predict') < 5) errs.push(`${id}: ${count('predict')} predictions (need 5)`);
  if (count('derivation') < 4) errs.push(`${id}: ${count('derivation')} derivations (need 4)`);
  const widgetsIn = (prefixes: string[]) =>
    lesson.movements.filter((m) => prefixes.some((p) => m.id.startsWith(p))).flatMap((m) => collectDirectives(m.blocks)).filter((b) => b.t === 'widget').length;
  if (widgetsIn(['m1', 'm2']) < 1) errs.push(`${id}: no widget in the puzzle or derivation`);
  if (widgetsIn(['m4', 'm5']) < 1) errs.push(`${id}: no widget in scale or break it`);
  const feynman = all.filter((b): b is Extract<Block, { t: 'feynman' }> => b.t === 'feynman');
  const explain = feynman.filter((f) => !f.id.startsWith('proof'));
  if (explain.length !== 1) errs.push(`${id}: ${explain.length} plain-language Feynman blocks (need exactly 1)`);
  for (const f of explain)
    if (f.keyPoints.length < 4 || f.keyPoints.length > 6) errs.push(`${id}: feynman ${f.id} has ${f.keyPoints.length} key points (need 4 to 6)`);
  const proofs = feynman.filter((f) => f.id.startsWith('proof'));
  if (lesson.stage !== 'prelude' && proofs.length < 1) errs.push(`${id}: no written proof (a feynman block with id proof*)`);
  for (const f of proofs) if (f.rubric !== 'concept') errs.push(`${id}: proof ${f.id} must use the concept rubric`);
  const chips = (dir: 'to' | 'from') => new Set(all.flatMap((b) => (b.t === 'edge' && b.dir === dir ? [b.lesson] : []))).size;
  const ins = neighbours(graph.edges, id, 'in').size;
  const outs = neighbours(graph.edges, id, 'out').size;
  if (chips('from') < Math.min(2, ins)) errs.push(`${id}: ${chips('from')} edge chips from earlier lessons (need ${Math.min(2, ins)})`);
  if (chips('to') < Math.min(2, outs)) errs.push(`${id}: ${chips('to')} edge chips to later lessons (need ${Math.min(2, outs)})`);
  const cards = reviewItemsFor(l).length;
  if (cards < 8 || cards > 12) errs.push(`${id}: ${cards} review cards (need 8 to 12)`);
  return errs;
}

export function lessonErrors(l: LoadedLesson, graph: Graph, loaded: Map<string, LoadedLesson>): string[] {
  const errs = l.issues.map((i) => i.message);
  const { lesson, yaml } = l;
  const id = lesson.id;
  const total = yaml.movements.reduce((s, m) => s + m.minutes, 0);
  if (yaml.id !== id) errs.push(`${id}: lesson.yaml id is ${yaml.id}`);
  if (yaml.hours < 6 || yaml.hours > 12) errs.push(`${id}: hours ${yaml.hours} outside 6..12`);
  if (Math.abs(total / 60 - yaml.hours) > 0.01) errs.push(`${id}: movement minutes sum to ${total / 60} h, lesson.yaml says ${yaml.hours} h`);
  if (yaml.movements.length < 6 || yaml.movements.length > 8) errs.push(`${id}: ${yaml.movements.length} movements (need 6..8)`);
  const share = lesson.theoryMinutes / total;
  if (share < 0.45 || share > 0.55) errs.push(`${id}: theory share ${(share * 100).toFixed(1)}% outside 45..55%`);
  for (const m of yaml.movements)
    if (!['theory', 'practice', 'both'].includes(m.mode)) errs.push(`${id}: ${m.file} has bad mode ${m.mode}`);
  if (!yaml.capstone) errs.push(`${id}: lesson.yaml capstone text missing`);

  const exIds = Object.keys(lesson.exercises).filter((e) => e !== 'capstone');
  if (exIds.length < 12) errs.push(`${id}: ${exIds.length} exercises (need 12)`);
  if (!lesson.exercises.capstone) errs.push(`${id}: no capstone`);
  const gradEx = exIds.filter((e) => lesson.exercises[e].testNames.some((n) => n.startsWith('test_grad')));
  // Math-track lessons follow their own rule (test_invariant* before M15), in mathTrackErrors.
  if (gradEx.length < 3 && !/^M\d\d$/.test(id)) errs.push(`${id}: ${gradEx.length} exercises with a test_grad* gradient check (need 3)`);
  for (const e of [...exIds, 'capstone']) {
    const ex = lesson.exercises[e];
    if (ex && ex.testNames.length === 0) errs.push(`${id}/${e}: tests.py defines no test_* functions`);
    if (ex && ex.hints.length === 0 && !ex.capstone) errs.push(`${id}/${e}: no hints`);
  }

  const all: Block[] = lesson.movements.flatMap((m) => collectDirectives(m.blocks));
  const count = (t: Block['t']) => all.filter((b) => b.t === t).length;
  for (const t of ['predict', 'derivation', 'feynman', 'widget'] as const)
    if (count(t) === 0) errs.push(`${id}: no :::${t}`);
  if (!lesson.movements.some((m) => m.breakIt)) errs.push(`${id}: no break-it movement`);
  const refs = new Set<string>();
  const dup = (kind: string, ids: string[]) => {
    const s = new Set<string>();
    for (const x of ids) {
      if (s.has(x)) errs.push(`${id}: duplicate ${kind} id ${x}`);
      s.add(x);
    }
  };
  dup('predict', all.filter((b) => b.t === 'predict').map((b) => (b as { id: string }).id));
  dup('derivation', all.filter((b) => b.t === 'derivation').map((b) => (b as { id: string }).id));
  dup('feynman', all.filter((b) => b.t === 'feynman').map((b) => (b as { id: string }).id));
  for (const b of all) {
    if (b.t === 'exercise') {
      if (!lesson.exercises[b.ref]) errs.push(`${id}: exercise ref ${b.ref} does not exist`);
      if (refs.has(b.ref)) errs.push(`${id}: exercise ${b.ref} embedded twice`);
      refs.add(b.ref);
    }
    if (b.t === 'widget' && !fs.existsSync(path.join(ROOT, 'src', 'widgets', `${b.name}.tsx`)))
      errs.push(`${id}: widget ${b.name} has no src/widgets/${b.name}.tsx`);
    if (b.t === 'edge') {
      const ok = b.dir === 'to' ? linked(graph.edges, id, b.lesson) : linked(graph.edges, b.lesson, id);
      if (!ok) errs.push(`${id}: edge marker ${b.dir} ${b.lesson} has no matching graph edge`);
    }
    if (b.t === 'derivation')
      for (const s of b.steps)
        for (const blank of s.blanks) {
          const err = validateBlank(blank);
          if (err) errs.push(`${id}: derivation ${b.id} blank "${blank}": ${err}`);
        }
    if (b.t === 'feynman' && b.keyPoints.length < 2) errs.push(`${id}: feynman ${b.id} needs at least 2 key points`);
    if (b.t === 'colab' && b.notebook !== id) errs.push(`${id}: colab block points at ${b.notebook}`);
  }
  for (const e of [...exIds, 'capstone']) if (lesson.exercises[e] && !refs.has(e)) errs.push(`${id}: exercise ${e} is never embedded`);

  for (const r of lesson.reuses) if (!linked(graph.edges, r.from, id)) errs.push(`${id}: reuses ${r.from} without an edge into ${id}`);
  for (const h of lesson.hooks) if (!linked(graph.edges, id, h.to)) errs.push(`${id}: hook to ${h.to} without an edge out of ${id}`);
  if (lesson.track === 'math' && /^M\d\d$/.test(id)) errs.push(...mathTrackErrors(l, graph, all));
  for (const a of yaml.annotations ?? []) if (!graph.lessons.some((g) => g.id === a.target)) errs.push(`${id}: annotation target ${a.target} unknown`);
  for (const k of yaml.katas ?? []) if (!lesson.exercises[k]) errs.push(`${id}: kata ${k} is not an exercise`);

  const compiled = JSON.stringify(lesson);
  const katexErrors = (compiled.match(/katex-error/g) ?? []).length;
  if (katexErrors) errs.push(`${id}: ${katexErrors} KaTeX rendering error(s); search the compiled lesson for katex-error`);

  for (const f of walk(lessonDir(id))) {
    const text = fs.readFileSync(f, 'utf8');
    const hits = bannedIn(text);
    if (hits.length) errs.push(`${path.relative(ROOT, f)}: banned content (${hits.join(', ')})`);
    // remark-math renders $$...$$ on one line as inline math; display math needs its own lines.
    if (f.endsWith('.md'))
      text.split('\n').forEach((line, i) => {
        if (line.includes('$$') && line.trim() !== '$$')
          errs.push(`${path.relative(ROOT, f)}:${i + 1}: put display math delimiters $$ on lines of their own`);
      });
  }

  if (lesson.gpu) {
    if (!all.some((b) => b.t === 'colab')) errs.push(`${id}: GPU lesson without a :::colab block`);
    const nbPath = path.join(ROOT, 'notebooks', `${id}.ipynb`);
    const expected = notebookFor(l, 'learner');
    if (!expected) errs.push(`${id}: GPU lesson without capstone/solution.py notebook source`);
    else if (!fs.existsSync(nbPath)) errs.push(`${id}: notebooks/${id}.ipynb missing (run npm run content)`);
    else {
      const actual = fs.readFileSync(nbPath, 'utf8');
      if (actual !== expected) errs.push(`${id}: notebooks/${id}.ipynb is stale (run npm run content)`);
      if (!actual.includes('forge-autograder') || !actual.includes('Completion code: FORGE-'))
        errs.push(`${id}: notebook lacks the autograder cell`);
      const hits = bannedIn(actual);
      if (hits.length) errs.push(`notebooks/${id}.ipynb: banned content (${hits.join(', ')})`);
      const solvedPath = path.join(ROOT, 'notebooks', 'solved', `${id}.ipynb`);
      if (!fs.existsSync(solvedPath) || fs.readFileSync(solvedPath, 'utf8') !== notebookFor(l, 'solved'))
        errs.push(`${id}: notebooks/solved/${id}.ipynb is missing or stale (run npm run content)`);
    }
  }

  const reviewPath = path.join(ROOT, 'content', 'reviews', `${id}.json`);
  const reviewExpected = JSON.stringify(reviewItemsFor(l), null, 1) + '\n';
  if (!fs.existsSync(reviewPath) || fs.readFileSync(reviewPath, 'utf8') !== reviewExpected)
    errs.push(`${id}: content/reviews/${id}.json is stale (run npm run content)`);
  void loaded;
  return errs;
}

function main() {
  const allowUnpublished = process.argv.includes('--allow-unpublished');
  const graph = loadGraph();
  const errs = graphErrors(graph);
  const loaded = new Map<string, LoadedLesson>();
  for (const g of graph.lessons) if (!allowUnpublished && !hasLesson(g.id)) errs.push(`${g.id}: content/lessons/${g.id}/lesson.yaml missing`);
  for (const d of fs.readdirSync(path.join(ROOT, 'content', 'lessons')))
    if (!graph.lessons.some((g) => g.id === d)) errs.push(`content/lessons/${d} is not in graph.yaml`);
  for (const g of graph.lessons) if (hasLesson(g.id)) loaded.set(g.id, loadLesson(g.id, graph));
  for (const id of loaded.keys()) errs.push(...lessonErrors(loaded.get(id)!, graph, loaded));
  const { missing } = findAnnotations(loaded);
  errs.push(...missing);
  for (const f of walk(path.join(ROOT, 'content')).filter((p) => p.endsWith('graph.yaml'))) {
    const hits = bannedIn(fs.readFileSync(f, 'utf8'));
    if (hits.length) errs.push(`${f}: banned content (${hits.join(', ')})`);
  }
  if (errs.length) {
    console.error(`validate_content: ${errs.length} problem(s)`);
    for (const e of errs) console.error('  - ' + e);
    process.exit(1);
  }
  console.log(`validate_content: OK (${loaded.size} lessons, ${graph.edges.length} edges)`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) main();
