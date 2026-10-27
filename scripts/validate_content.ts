// Enforces every content rule in EXECUTION_PLAN.md Sections 2 and 6.5.
// Usage: tsx scripts/validate_content.ts [--phase L01,L02,...]
import fs from 'node:fs';
import path from 'node:path';
import { loadGraph, hasLesson, loadLesson, lessonDir, ROOT, type LoadedLesson, type Graph } from './lib/content';
import { collectDirectives } from './lib/markdown';
import { findAnnotations, notebookFor } from './build_content';
import { reviewItemsFor } from './gen_reviews';
import { validateBlank } from '../src/lib/expr';
import type { Block } from '../src/content/types';

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

export function graphErrors(graph: Graph): string[] {
  const errs: string[] = [];
  const ids = new Set(graph.lessons.map((l) => l.id));
  const stageIdx = new Map(graph.stages.map((s, i) => [s, i]));
  const lessonStage = new Map(graph.lessons.map((l) => [l.id, stageIdx.get(l.stage) ?? -1]));
  const seen = new Set<string>();
  for (const l of graph.lessons) {
    if (!graph.tracks.includes(l.track) && l.track !== 'all') errs.push(`${l.id}: unknown track ${l.track}`);
    if (!stageIdx.has(l.stage)) errs.push(`${l.id}: unknown stage ${l.stage}`);
  }
  for (const e of graph.edges) {
    const key = `${e.from}->${e.to}`;
    if (seen.has(key)) errs.push(`duplicate edge ${key}`);
    seen.add(key);
    if (!ids.has(e.from) || !ids.has(e.to)) errs.push(`edge ${key} references a missing lesson`);
    if (!['vertical', 'horizontal', 'long_range'].includes(e.type)) errs.push(`edge ${key} has bad type ${e.type}`);
    if (e.type === 'vertical' && (lessonStage.get(e.from) ?? 0) > (lessonStage.get(e.to) ?? 0))
      errs.push(`vertical edge ${key} points from a later stage to an earlier one`);
    if (e.type === 'horizontal' && lessonStage.get(e.from) !== lessonStage.get(e.to))
      errs.push(`horizontal edge ${key} crosses stages`);
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
    const roots = ['L01', 'L02', 'L03'];
    if (!roots.includes(l.id) && inbound.length === 0) errs.push(`${l.id}: no inbound edge`);
    if (l.id !== last && outbound.length === 0) errs.push(`${l.id}: no outbound edge`);
    if (![...inbound, ...outbound].some((e) => e.type !== 'vertical')) errs.push(`${l.id}: no horizontal or long-range edge`);
  }
  void first;
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
  if (gradEx.length < 3) errs.push(`${id}: ${gradEx.length} exercises with a test_grad* gradient check (need 3)`);
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
      const ok =
        b.dir === 'to'
          ? graph.edges.some((e) => e.from === id && e.to === b.lesson)
          : graph.edges.some((e) => e.to === id && e.from === b.lesson);
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

  for (const r of lesson.reuses)
    if (!graph.edges.some((e) => e.from === r.from && e.to === id)) errs.push(`${id}: reuses ${r.from} without an edge into ${id}`);
  for (const h of lesson.hooks)
    if (!graph.edges.some((e) => e.from === id && e.to === h.to)) errs.push(`${id}: hook to ${h.to} without an edge out of ${id}`);
  for (const a of yaml.annotations ?? []) if (!graph.lessons.some((g) => g.id === a.target)) errs.push(`${id}: annotation target ${a.target} unknown`);
  for (const k of yaml.katas ?? []) if (!lesson.exercises[k]) errs.push(`${id}: kata ${k} is not an exercise`);

  const compiled = JSON.stringify(lesson);
  const katexErrors = (compiled.match(/katex-error/g) ?? []).length;
  if (katexErrors) errs.push(`${id}: ${katexErrors} KaTeX rendering error(s); search the compiled lesson for katex-error`);

  for (const f of walk(lessonDir(id))) {
    const hits = bannedIn(fs.readFileSync(f, 'utf8'));
    if (hits.length) errs.push(`${path.relative(ROOT, f)}: banned content (${hits.join(', ')})`);
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
  const argv = process.argv.slice(2);
  const pi = argv.indexOf('--phase');
  const graph = loadGraph();
  const expected = pi >= 0 ? argv[pi + 1].split(',').map((s) => s.trim()) : graph.lessons.map((l) => l.id);
  const errs = graphErrors(graph);
  const loaded = new Map<string, LoadedLesson>();
  for (const id of expected) {
    if (!graph.lessons.some((l) => l.id === id)) errs.push(`--phase lists unknown lesson ${id}`);
    else if (!hasLesson(id)) errs.push(`${id}: content/lessons/${id}/lesson.yaml missing`);
  }
  for (const g of graph.lessons) if (hasLesson(g.id)) loaded.set(g.id, loadLesson(g.id, graph));
  for (const id of loaded.keys()) {
    if (!expected.includes(id)) errs.push(`${id}: present but not listed in --phase`);
    errs.push(...lessonErrors(loaded.get(id)!, graph, loaded));
  }
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
