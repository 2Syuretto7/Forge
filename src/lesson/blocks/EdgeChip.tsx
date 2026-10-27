import { Link } from 'react-router-dom';
import type { Block, ContentIndex } from '../../content/types';
import { useStore } from '../../store/store';
import { nodeState } from '../../store/derive';

type E = Extract<Block, { t: 'edge' }>;

export function EdgeChip({ b, index }: { b: E; index: ContentIndex }) {
  const target = index.lessons.find((l) => l.id === b.lesson);
  const st = useStore((s) => (target ? nodeState(s, index, target) : 'unpublished'));
  if (b.dir === 'from') {
    return (
      <div className="edge-chip back">
        <Link to={`/lesson/${b.lesson}`}>
          Reuses {b.lesson}: {b.text}
        </Link>
      </div>
    );
  }
  const reachable = st !== 'locked' && st !== 'unpublished';
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
