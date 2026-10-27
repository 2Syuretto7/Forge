// Builds spaced-review items from lesson content: re-derivation blanks,
// predictions, concept checks and code katas. Output: content/reviews/<ID>.json
import fs from 'node:fs';
import path from 'node:path';
import { loadGraph, hasLesson, loadLesson, CONTENT, type LoadedLesson } from './lib/content';
import { collectDirectives } from './lib/markdown';
import { parseBlank } from '../src/lib/expr';
import type { ReviewItem } from '../src/content/types';

export function reviewItemsFor(l: LoadedLesson): ReviewItem[] {
  const { lesson, yaml } = l;
  const items: ReviewItem[] = [];
  for (const mv of lesson.movements) {
    for (const b of collectDirectives(mv.blocks)) {
      if (b.t === 'derivation') {
        b.steps.forEach((s, si) => {
          if (s.blanks.length !== 1) return;
          const spec = parseBlank(s.blanks[0]);
          items.push({
            id: `${lesson.id}/${b.id}/s${si + 1}`,
            lesson: lesson.id,
            kind: 'derivation',
            prompt: `<p class="review-context">${b.title}</p>${s.html}`,
            answer: s.blanks[0],
            answerKind: spec.kind === 'word' ? 'text' : 'expr',
          });
        });
      }
      if (b.t === 'predict' && b.kind !== 'sketch') {
        items.push({
          id: `${lesson.id}/${b.id}`,
          lesson: lesson.id,
          kind: 'prediction',
          prompt: b.questionHtml,
          answer: b.answer,
          answerKind: b.kind === 'choice' ? 'choice' : 'numeric',
          tol: b.tol,
          options: b.options,
          explain: b.explainHtml,
        });
      }
    }
  }
  (yaml.concepts ?? []).forEach((c, i) =>
    items.push({
      id: `${lesson.id}/concept${i + 1}`,
      lesson: lesson.id,
      kind: 'concept',
      prompt: c.q,
      answer: c.a,
      answerKind: 'text',
    }),
  );
  for (const k of yaml.katas ?? []) {
    const ex = lesson.exercises[k];
    if (!ex) continue;
    items.push({
      id: `${lesson.id}/kata/${k}`,
      lesson: lesson.id,
      kind: 'kata',
      prompt: ex.title,
      answer: '',
      answerKind: 'code',
      exercise: k,
    });
  }
  return items;
}

function main() {
  const graph = loadGraph();
  const dir = path.join(CONTENT, 'reviews');
  fs.mkdirSync(dir, { recursive: true });
  let n = 0;
  for (const g of graph.lessons) {
    if (!hasLesson(g.id)) continue;
    const items = reviewItemsFor(loadLesson(g.id, graph));
    n += items.length;
    fs.writeFileSync(path.join(dir, `${g.id}.json`), JSON.stringify(items, null, 1) + '\n');
  }
  console.log(`gen_reviews: ${n} items`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) main();
