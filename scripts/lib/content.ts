// Loads content/ into typed structures. Shared by build, validate and reviews.
import fs from 'node:fs';
import path from 'node:path';
import YAML from 'yaml';
import { compileMarkdown, collectDirectives, nodesToHtml, type CompileIssue } from './markdown';
import type {
  Edge,
  Exercise,
  Hook,
  Lesson,
  Mode,
  Movement,
  Reuse,
  Stage,
  Strand,
  Track,
} from '../../src/content/types';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import type { Root, RootContent, List, Parent } from 'mdast';
import { toString as mdToString } from 'mdast-util-to-string';

export const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
export const CONTENT = path.join(ROOT, 'content');
export const LESSONS_DIR = path.join(CONTENT, 'lessons');

export interface GraphLesson {
  id: string;
  title: string;
  track: Track;
  strand?: Strand;
  stage: Stage;
  gpu: boolean;
  compute: 'browser' | 'browser+colab' | 'colab';
}

export interface Graph {
  tracks: Track[];
  stages: Stage[];
  strands: Strand[];
  lessons: GraphLesson[];
  edges: Edge[];
}

export interface LessonYaml {
  id: string;
  hours: number;
  capstone: string;
  teaser?: string;
  movements: { file: string; mode: Mode; minutes: number }[];
  hooks?: Hook[];
  reuses?: Reuse[];
  annotations?: { target: string; movement?: string; anchor: string; text: string }[];
  concepts?: { q: string; a: string }[];
  katas?: string[];
}

export function loadGraph(): Graph {
  const g = YAML.parse(fs.readFileSync(path.join(CONTENT, 'graph.yaml'), 'utf8')) as Graph;
  g.edges = g.edges.map((e) => ({ ...e, from: String(e.from), to: String(e.to) }));
  g.strands = g.strands ?? [];
  return g;
}

export function lessonDir(id: string) {
  return path.join(LESSONS_DIR, id);
}

export function hasLesson(id: string) {
  return fs.existsSync(path.join(lessonDir(id), 'lesson.yaml'));
}

export function loadLessonYaml(id: string): LessonYaml {
  return YAML.parse(fs.readFileSync(path.join(lessonDir(id), 'lesson.yaml'), 'utf8')) as LessonYaml;
}

function read(p: string) {
  return fs.readFileSync(p, 'utf8');
}

export function testNames(src: string): string[] {
  return [...src.matchAll(/^def (test_\w+)\s*\(/gm)].map((m) => m[1]);
}

// prompt.md: "# Title", body, optional "## Hints" numbered list (max 3).
export function compilePrompt(src: string, where: string) {
  const tree = unified().use(remarkParse).use(remarkGfm, { singleTilde: false }).use(remarkMath).parse(src) as Root;
  const issues: CompileIssue[] = [];
  let title = '';
  const nodes = [...tree.children];
  const h1 = nodes.findIndex((n) => n.type === 'heading' && n.depth === 1);
  if (h1 >= 0) {
    title = mdToString(nodes[h1]);
    nodes.splice(h1, 1);
  } else issues.push({ message: `${where}: prompt.md missing "# Title"` });
  const hintsIdx = nodes.findIndex((n) => n.type === 'heading' && n.depth === 2 && /^hints$/i.test(mdToString(n)));
  let hints: string[] = [];
  let body = nodes;
  if (hintsIdx >= 0) {
    const list = nodes.slice(hintsIdx + 1).find((n) => n.type === 'list') as List | undefined;
    if (list) hints = list.children.map((li) => nodesToHtml((li as Parent).children as RootContent[]));
    body = nodes.slice(0, hintsIdx);
  }
  if (hints.length > 3) issues.push({ message: `${where}: more than 3 hints` });
  return { title, html: nodesToHtml(body), hints, issues };
}

export interface LoadedLesson {
  lesson: Lesson;
  yaml: LessonYaml;
  issues: CompileIssue[];
  plainText: Map<string, string[]>; // movement id -> text per top-level block
  files: string[];
  notebookSource: string | null;
}

export function loadLesson(id: string, graph: Graph): LoadedLesson {
  const dir = lessonDir(id);
  const yaml = loadLessonYaml(id);
  const meta = graph.lessons.find((l) => l.id === id)!;
  const issues: CompileIssue[] = [];
  const files: string[] = [];
  const plainText = new Map<string, string[]>();

  const movements: Movement[] = [];
  for (const m of yaml.movements) {
    const p = path.join(dir, m.file);
    if (!fs.existsSync(p)) {
      issues.push({ message: `${id}: missing movement file ${m.file}` });
      continue;
    }
    files.push(p);
    const res = compileMarkdown(read(p), `${id}/${m.file}`);
    issues.push(...res.issues);
    const mid = m.file.replace(/\.md$/, '');
    // Top-level text per block index, used to anchor retro-annotations.
    plainText.set(
      mid,
      res.blocks.map((b) => (b.t === 'html' ? b.html.replace(/<[^>]+>/g, ' ') : '')),
    );
    movements.push({
      id: mid,
      file: m.file,
      title: res.title,
      mode: m.mode,
      minutes: m.minutes,
      breakIt: /break/.test(m.file),
      blocks: res.blocks,
    });
  }

  const exercises: Record<string, Exercise> = {};
  const exDir = path.join(dir, 'exercises');
  const exIds = fs.existsSync(exDir) ? fs.readdirSync(exDir).filter((f) => fs.statSync(path.join(exDir, f)).isDirectory()).sort() : [];
  const loadEx = (exId: string, d: string, capstone: boolean) => {
    const need = ['prompt.md', 'solution.py', 'tests.py'];
    for (const f of need) {
      if (!fs.existsSync(path.join(d, f))) issues.push({ message: `${id}/${exId}: missing ${f}` });
    }
    const notebook = capstone && meta?.gpu === true;
    if (!notebook && !fs.existsSync(path.join(d, 'starter.py'))) issues.push({ message: `${id}/${exId}: missing starter.py` });
    if (need.some((f) => !fs.existsSync(path.join(d, f)))) return;
    for (const f of [...need, 'starter.py']) if (fs.existsSync(path.join(d, f))) files.push(path.join(d, f));
    const pr = compilePrompt(read(path.join(d, 'prompt.md')), `${id}/${exId}`);
    issues.push(...pr.issues);
    const tests = read(path.join(d, 'tests.py'));
    exercises[exId] = {
      id: exId,
      title: pr.title,
      promptHtml: pr.html,
      hints: pr.hints,
      starter: notebook ? '' : read(path.join(d, 'starter.py')),
      solution: notebook ? '' : read(path.join(d, 'solution.py')),
      tests,
      testNames: testNames(tests),
      capstone,
      notebook,
    };
  };
  for (const exId of exIds) loadEx(exId, path.join(exDir, exId), false);
  const capDir = path.join(dir, 'capstone');
  let notebookSource: string | null = null;
  if (fs.existsSync(capDir)) {
    loadEx('capstone', capDir, true);
    if (meta?.gpu && fs.existsSync(path.join(capDir, 'solution.py'))) notebookSource = read(path.join(capDir, 'solution.py'));
  } else issues.push({ message: `${id}: missing capstone/` });

  // Attach the expected autograder test list to colab blocks.
  for (const mv of movements) {
    for (const b of collectDirectives(mv.blocks)) {
      if (b.t === 'colab') b.tests = exercises.capstone?.testNames ?? [];
    }
  }

  const theory = yaml.movements.reduce((s, m) => s + (m.mode === 'theory' ? m.minutes : m.mode === 'both' ? m.minutes / 2 : 0), 0);
  const practice = yaml.movements.reduce((s, m) => s + (m.mode === 'practice' ? m.minutes : m.mode === 'both' ? m.minutes / 2 : 0), 0);
  const prereqs = graph.edges.filter((e) => e.to === id && e.type === 'vertical').map((e) => e.from);
  const unlocks = graph.edges.filter((e) => e.from === id && e.type === 'vertical').map((e) => e.to);

  const lesson: Lesson = {
    id,
    title: meta?.title ?? id,
    track: meta?.track ?? 'math',
    ...(meta?.strand ? { strand: meta.strand } : {}),
    stage: meta?.stage ?? 'foundations',
    gpu: meta?.gpu ?? false,
    hours: yaml.hours,
    theoryMinutes: theory,
    practiceMinutes: practice,
    capstone: yaml.capstone,
    teaser: yaml.teaser ?? '',
    movements,
    prereqs,
    unlocks,
    exercises,
    hooks: yaml.hooks ?? [],
    reuses: yaml.reuses ?? [],
    feynman: movements.flatMap((m) => collectDirectives(m.blocks)).flatMap((b) => (b.t === 'feynman' ? [b.id] : [])),
  };
  return { lesson, yaml, issues, plainText, files, notebookSource };
}

export function stripMovementBlocks(lesson: Lesson) {
  return {
    ...lesson,
    movements: lesson.movements.map((m) => ({
      id: m.id,
      file: m.file,
      title: m.title,
      mode: m.mode,
      minutes: m.minutes,
      breakIt: m.breakIt,
    })),
  };
}
