import { Link } from 'react-router-dom';
import type { Exercise } from '../../content/types';
import { useStore } from '../../store/store';
import { exerciseXp, exerciseXpAvailable } from '../../store/derive';
import { Bolt, Check, Cloud, Code, Play } from '../../app/icons';

// The first paragraph of an exercise prompt, shown (clamped) on the step card.
function firstParagraph(html: string) {
  return /<p>[\s\S]*?<\/p>/.exec(html)?.[0] ?? '';
}

export function ExerciseCard({ lessonId, ex, number }: { lessonId: string; ex: Exercise; number: number }) {
  const rec = useStore((s) => s.exercises[`${lessonId}/${ex.id}`]);
  const st = rec?.status ?? 'unseen';
  const done = st === 'passed' || st === 'passed_with_solution';
  const label = st === 'passed' ? 'Passed' : st === 'passed_with_solution' ? 'Completed with solution' : st === 'attempted' ? 'In progress' : 'Not started';
  const action = done ? 'Review' : st === 'attempted' ? 'Continue' : 'Start';
  return (
    <div className={`card exercise ex-${st}`} id={`ex-${ex.id}`}>
      <span className="ex-icon" aria-hidden="true">
        {done ? <Check size={18} /> : ex.notebook ? <Cloud size={18} /> : <Code size={18} />}
      </span>
      <div className="ex-body">
        <div className="card-kicker">
          {ex.capstone ? 'Capstone' : `Exercise ${number}`}
          <span className={`ex-status ${st}`}>{label}</span>
          {!ex.notebook && (
            <span className="ex-xp">
              <Bolt size={12} /> {done ? exerciseXp(rec) : exerciseXpAvailable(rec?.hintsUsed ?? 0)} XP
            </span>
          )}
        </div>
        <h3>{ex.title}</h3>
        {ex.notebook ? (
          <p className="muted">This capstone runs in the Colab notebook below. Paste its completion code to finish.</p>
        ) : (
          <div className="ex-excerpt" dangerouslySetInnerHTML={{ __html: firstParagraph(ex.promptHtml) }} />
        )}
      </div>
      {!ex.notebook && (
        <Link to={`/lesson/${lessonId}/ex/${ex.id}`} className={`btn ${done ? 'outline' : 'primary'}`} aria-label={`${action} ${ex.capstone ? 'capstone' : `exercise ${number}`}: ${ex.title}`}>
          {!done && <Play size={12} />} {action}
        </Link>
      )}
    </div>
  );
}
