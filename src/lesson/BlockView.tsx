import { Suspense } from 'react';
import type { Annotation, Block, ContentIndex, Lesson } from '../content/types';
import { getWidget } from '../widgets';
import { Html } from './blocks/Html';
import { Predict } from './blocks/Predict';
import { Derivation } from './blocks/Derivation';
import { EdgeChip } from './blocks/EdgeChip';
import { ExerciseCard } from './blocks/ExerciseCard';
import { Colab } from './blocks/Colab';
import { Feynman } from '../grader/Feynman';
import { Link } from 'react-router-dom';

export interface BlockCtx {
  lesson: Lesson;
  index: ContentIndex;
  // Exercise numbers in lesson order (capstones are not numbered).
  exerciseNumber: (ref: string) => number;
}

function WidgetBlock({ name, props }: { name: string; props: Record<string, string> }) {
  const W = getWidget(name);
  if (!W) return <p className="reveal bad">Unknown widget {name}</p>;
  return (
    <Suspense fallback={<div className="widget loading">Loading figure</div>}>
      <W props={props} />
    </Suspense>
  );
}

export function BlockView({ b, ctx }: { b: Block; ctx: BlockCtx }) {
  const { lesson } = ctx;
  switch (b.t) {
    case 'html':
      return <Html html={b.html} />;
    case 'derivation':
      return <Derivation b={b} />;
    case 'predict':
      return <Predict b={b} lessonId={lesson.id} />;
    case 'exercise': {
      const ex = lesson.exercises[b.ref];
      if (!ex) return null;
      return <ExerciseCard lessonId={lesson.id} ex={ex} number={ctx.exerciseNumber(b.ref)} />;
    }
    case 'widget':
      return <WidgetBlock name={b.name} props={b.props} />;
    case 'edge':
      return <EdgeChip b={b} index={ctx.index} />;
    case 'feynman':
      return <Feynman b={b} lessonId={lesson.id} lessonTitle={lesson.title} />;
    case 'colab':
      return <Colab b={b} />;
    case 'aside':
      return (
        <details className="aside">
          <summary>{b.title}</summary>
          {b.blocks.map((c, i) => (
            <BlockView key={i} b={c} ctx={ctx} />
          ))}
        </details>
      );
  }
}

export function AnnotatedBlock({ b, ctx, notes }: { b: Block; ctx: BlockCtx; notes: Annotation[] }) {
  if (!notes.length) return <BlockView b={b} ctx={ctx} />;
  return (
    <div className="annotated">
      <BlockView b={b} ctx={ctx} />
      <aside className="margin-notes" aria-label="Notes from later lessons">
        {notes.map((n, i) => (
          <div key={i} className="margin-note">
            <Link to={`/lesson/${n.source}`} className="note-src">
              From {n.source}
            </Link>
            <p>{n.text}</p>
          </div>
        ))}
      </aside>
    </div>
  );
}
