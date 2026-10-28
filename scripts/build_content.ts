// Compiles content/ into public/content/*.json and generates notebooks.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { loadGraph, loadLesson, hasLesson, ROOT, CONTENT, stripMovementBlocks, type LoadedLesson } from './lib/content';
import { buildNotebook } from './lib/notebook';
import type { Annotation, ContentIndex, LessonSummary, ReviewItem } from '../src/content/types';

const OUT = path.join(ROOT, 'public', 'content');
const NB_OUT = path.join(ROOT, 'notebooks');
// Solved notebooks are committed too: CI executes them, and the owner can run one in Colab to
// check the GPU paths (docs/colab-check.md).
const NB_SOLVED = path.join(ROOT, 'notebooks', 'solved');

export function findAnnotations(loaded: Map<string, LoadedLesson>) {
  const annotations: Annotation[] = [];
  const missing: string[] = [];
  for (const [id, l] of loaded) {
    for (const a of l.yaml.annotations ?? []) {
      const target = loaded.get(a.target);
      if (!target) continue;
      let found: Annotation | null = null;
      for (const [mid, texts] of target.plainText) {
        if (a.movement && a.movement !== mid) continue;
        const idx = texts.findIndex((t) => t.toLowerCase().includes(a.anchor.toLowerCase()));
        if (idx >= 0) {
          found = { source: id, target: a.target, movement: mid, block: idx, anchor: a.anchor, text: a.text };
          break;
        }
      }
      if (found) annotations.push(found);
      else missing.push(`${id}: annotation anchor "${a.anchor}" not found in ${a.target}${a.movement ? `/${a.movement}` : ''}`);
    }
  }
  return { annotations, missing };
}

export function loadAll() {
  const graph = loadGraph();
  const loaded = new Map<string, LoadedLesson>();
  for (const l of graph.lessons) if (hasLesson(l.id)) loaded.set(l.id, loadLesson(l.id, graph));
  return { graph, loaded };
}

export function notebookFor(l: LoadedLesson, variant: 'learner' | 'solved') {
  if (!l.notebookSource) return null;
  const gpu = !l.lesson.movements.some((m) => m.blocks.some((b) => b.t === 'colab' && !b.gpu));
  return buildNotebook(l.lesson.id, l.notebookSource, l.lesson.exercises.capstone?.tests ?? '', variant, gpu);
}

function main() {
  const { graph, loaded } = loadAll();
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(path.join(OUT, 'lessons'), { recursive: true });
  fs.mkdirSync(NB_OUT, { recursive: true });
  fs.mkdirSync(NB_SOLVED, { recursive: true });

  const hash = crypto.createHash('sha256');
  const summaries: LessonSummary[] = [];
  for (const g of graph.lessons) {
    const l = loaded.get(g.id);
    if (l) {
      const json = JSON.stringify(l.lesson);
      hash.update(json);
      fs.writeFileSync(path.join(OUT, 'lessons', `${g.id}.json`), json);
      const { exercises: _ex, hooks: _h, reuses: _r, ...summary } = stripMovementBlocks(l.lesson);
      summaries.push(summary);
      const learner = notebookFor(l, 'learner');
      const solved = notebookFor(l, 'solved');
      if (learner && solved) {
        fs.writeFileSync(path.join(NB_OUT, `${g.id}.ipynb`), learner);
        fs.writeFileSync(path.join(NB_SOLVED, `${g.id}.ipynb`), solved);
      }
    } else {
      const prereqs = graph.edges.filter((e) => e.to === g.id && e.type === 'vertical').map((e) => e.from);
      const unlocks = graph.edges.filter((e) => e.from === g.id && e.type === 'vertical').map((e) => e.to);
      summaries.push({
        id: g.id,
        title: g.title,
        track: g.track,
        stage: g.stage,
        gpu: g.gpu,
        hours: 0,
        theoryMinutes: 0,
        practiceMinutes: 0,
        capstone: '',
        movements: [],
        prereqs,
        unlocks,
        teaser: '',
      });
    }
  }

  const { annotations } = findAnnotations(loaded);
  const reviews: ReviewItem[] = [];
  const reviewDir = path.join(CONTENT, 'reviews');
  for (const id of loaded.keys()) {
    const p = path.join(reviewDir, `${id}.json`);
    if (fs.existsSync(p)) reviews.push(...(JSON.parse(fs.readFileSync(p, 'utf8')) as ReviewItem[]));
  }

  const index: ContentIndex = {
    buildId: hash.digest('hex').slice(0, 12),
    tracks: graph.tracks,
    stages: graph.stages,
    lessons: summaries,
    edges: graph.edges,
    annotations,
    reviews,
    available: [...loaded.keys()],
  };
  fs.writeFileSync(path.join(OUT, 'index.json'), JSON.stringify(index));
  console.log(`build_content: ${loaded.size} lessons, ${graph.edges.length} edges, ${reviews.length} review items`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) main();
