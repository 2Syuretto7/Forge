import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useIndex } from '../content/load';
import { gradeReview, useStore } from '../store/store';
import { dueReviewIds } from '../store/derive';
import { localDate } from './sm2';
import { ReviewCard, resolveItem } from './ReviewCard';

export function ReviewQueue({ ids, onEmpty }: { ids: string[]; onEmpty?: React.ReactNode }) {
  const { data: index } = useIndex();
  const [done, setDone] = useState<string[]>([]);
  const remaining = ids.filter((id) => !done.includes(id));
  if (!index) return <p className="muted">Loading</p>;
  const current = remaining.map((id) => resolveItem(id, index.reviews)).find(Boolean);
  if (!current) return <>{onEmpty}</>;
  return (
    <div>
      <p className="muted" aria-live="polite">
        {remaining.length} item{remaining.length === 1 ? '' : 's'} left in this session
      </p>
      <ReviewCard
        key={current.id}
        item={current}
        onGrade={(q) => {
          void gradeReview(current.id, q);
          setDone((d) => [...d, current.id]);
        }}
      />
    </div>
  );
}

export function ReviewPage() {
  const reviews = useStore((s) => s.reviews);
  const { data: index } = useIndex();
  const today = localDate();
  // Snapshot the queue when the page opens (and the index has loaded) so graded items leave it cleanly.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const ids = useMemo(() => (index ? dueReviewIds({ reviews } as never, index, today) : []), [index]);
  const upcoming = Object.values(reviews).filter((r) => r.due > today).length;
  return (
    <main className="page narrow" id="main">
      <h1>Reviews</h1>
      <p className="muted">
        Spaced review (SM-2). Grade each item 0 to 5; items you find hard come back sooner. {upcoming} item{upcoming === 1 ? '' : 's'} scheduled for
        later days.
      </p>
      <ReviewQueue
        ids={ids}
        onEmpty={
          <div className="card">
            <p>No reviews due today.</p>
            <p className="muted">
              Completing a lesson schedules its review items for tomorrow. <Link to="/">Back to the map</Link>
            </p>
          </div>
        }
      />
    </main>
  );
}
