import type { Lesson } from '../content/types';

// Theory/practice meter: planned split, plus how much of each is done.
export function Meter({ lesson, done }: { lesson: Lesson; done: string[] }) {
  let tDone = 0;
  let pDone = 0;
  for (const m of lesson.movements) {
    if (!done.includes(m.id)) continue;
    const t = m.mode === 'theory' ? m.minutes : m.mode === 'both' ? m.minutes / 2 : 0;
    tDone += t;
    pDone += m.minutes - t;
  }
  const total = lesson.theoryMinutes + lesson.practiceMinutes;
  const tPct = (lesson.theoryMinutes / total) * 100;
  const pct = (x: number) => `${Math.round(x)}%`;
  return (
    <div className="meter" aria-label="Theory and practice balance">
      <div className="meter-bar" role="img" aria-label={`Planned: ${pct(tPct)} theory, ${pct(100 - tPct)} practice`}>
        <div className="meter-theory" style={{ width: `${tPct}%` }}>
          <div className="meter-fill" style={{ width: `${lesson.theoryMinutes ? (tDone / lesson.theoryMinutes) * 100 : 0}%` }} />
        </div>
        <div className="meter-practice" style={{ width: `${100 - tPct}%` }}>
          <div className="meter-fill" style={{ width: `${lesson.practiceMinutes ? (pDone / lesson.practiceMinutes) * 100 : 0}%` }} />
        </div>
      </div>
      <div className="meter-legend">
        <span>
          Theory {Math.round(tDone / 6) / 10} / {Math.round(lesson.theoryMinutes / 6) / 10} h
        </span>
        <span>
          Practice {Math.round(pDone / 6) / 10} / {Math.round(lesson.practiceMinutes / 6) / 10} h
        </span>
      </div>
    </div>
  );
}
