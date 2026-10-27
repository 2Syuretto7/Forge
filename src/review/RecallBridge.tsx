import { useMemo } from 'react';
import type { ContentIndex, Lesson } from '../content/types';
import { useStore } from '../store/store';
import { dueItems } from '../store/derive';
import { ReviewQueue } from './ReviewPage';

// Movement 0: due reviews filtered to the lesson's prerequisites (every lesson
// with an edge into this one).
export function RecallBridge({ lesson, index }: { lesson: Lesson; index: ContentIndex }) {
  const reviews = useStore((s) => s.reviews);
  const sources = useMemo(() => new Set(index.edges.filter((e) => e.to === lesson.id).map((e) => e.from)), [index, lesson.id]);
  const ids = useMemo(
    () =>
      dueItems({ reviews } as never)
        .map((r) => r.itemId)
        .filter((id) => sources.has(id.slice(0, 3)))
        .sort(),
    // Snapshot on entry.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [sources],
  );
  if (!sources.size) return null;
  return (
    <section className="card recall" aria-label="Recall bridge">
      <div className="card-kicker">Recall bridge</div>
      <p>
        Due reviews from the lessons this one builds on ({[...sources].sort().join(', ')}). Answer from memory before reading on.
      </p>
      <ReviewQueue ids={ids} onEmpty={<p className="muted">No reviews from these lessons are due today.</p>} />
    </section>
  );
}
