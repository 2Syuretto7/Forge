import type { Exercise } from '../../content/types';
import { useStore } from '../../store/store';
import { Html } from './Html';

export function ExerciseCard({
  lessonId,
  ex,
  active,
  onOpen,
}: {
  lessonId: string;
  ex: Exercise;
  active: boolean;
  onOpen: () => void;
}) {
  const st = useStore((s) => s.exercises[`${lessonId}/${ex.id}`]?.status ?? 'unseen');
  const label =
    st === 'passed' ? 'Passed' : st === 'passed_with_solution' ? 'Completed with solution' : st === 'attempted' ? 'In progress' : 'Not started';
  return (
    <div className={`card exercise ${active ? 'active' : ''}`} id={`ex-${ex.id}`}>
      <div className="card-kicker">
        {ex.capstone ? 'Capstone' : `Exercise ${ex.id.replace(/^e0?/, '')}`}
        <span className={`ex-status ${st}`}>{label}</span>
      </div>
      <h3>{ex.title}</h3>
      <Html html={ex.promptHtml} />
      {ex.notebook ? (
        <p className="muted">This capstone runs in the Colab notebook below. Paste its completion code to finish.</p>
      ) : (
        <button className="btn primary" onClick={onOpen} aria-pressed={active}>
          {active ? 'Open in editor' : 'Open in editor'}
        </button>
      )}
    </div>
  );
}
