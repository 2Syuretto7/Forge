import { Link } from 'react-router-dom';
import type { Block, ContentIndex } from '../../content/types';
import { useStore } from '../../store/store';
import { nodeState } from '../../store/derive';

type E = Extract<Block, { t: 'edge' }>;

export function EdgeChip({ b, index, lessonId }: { b: E; index: ContentIndex; lessonId: string }) {
  const target = index.lessons.find((l) => l.id === b.lesson);
  const st = useStore((s) => (target ? nodeState(s, index, target) : 'unpublished'));
  const reachable = st !== 'locked' && st !== 'unpublished';
  // A horizontal edge links two lessons of one stage both ways: the chip reads "Across".
  const across = !index.edges.some(
    (e) => e.type !== 'horizontal' && ((e.from === lessonId && e.to === b.lesson) || (e.to === lessonId && e.from === b.lesson)),
  );
  if (across && index.edges.some((e) => e.type === 'horizontal' && [e.from, e.to].includes(b.lesson) && [e.from, e.to].includes(lessonId))) {
    return (
      <div className="edge-chip across">
        {reachable ? (
          <Link to={`/lesson/${b.lesson}`}>Across in {b.lesson}</Link>
        ) : (
          <span aria-disabled="true" className="disabled">
            Across in {b.lesson}
          </span>
        )}
        <span className="teaser">{b.text}</span>
      </div>
    );
  }
  if (b.dir === 'from') {
    return (
      <div className="edge-chip back">
        <Link to={`/lesson/${b.lesson}`}>
          Reuses {b.lesson}: {b.text}
        </Link>
      </div>
    );
  }
  return (
    <div className="edge-chip forward">
      {reachable ? (
        <Link to={`/lesson/${b.lesson}`}>Returns in {b.lesson}</Link>
      ) : (
        <span aria-disabled="true" className="disabled">
          Returns in {b.lesson}
        </span>
      )}
      <span className="teaser">{b.text}</span>
    </div>
  );
}
