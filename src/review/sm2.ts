// SM-2 variant. Grades 0..5; grades below 3 reset the repetition count.
import type { ReviewRec } from '../store/db';

export function localDate(d: Date = new Date()): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

export function addDays(date: string, days: number): string {
  const [y, m, d] = date.split('-').map(Number);
  return localDate(new Date(y, m - 1, d + days));
}

export function newReview(itemId: string, today: string): ReviewRec {
  return { itemId, ease: 2.5, interval: 0, due: addDays(today, 1), reps: 0, lapses: 0, history: [] };
}

export function grade(rec: ReviewRec, q: number, today: string, now = Date.now()): ReviewRec {
  const quality = Math.max(0, Math.min(5, Math.round(q)));
  let { ease, interval, reps, lapses } = rec;
  if (quality < 3) {
    reps = 0;
    interval = 1;
    lapses += 1;
  } else {
    if (reps === 0) interval = 1;
    else if (reps === 1) interval = 6;
    else interval = Math.round(interval * ease);
    reps += 1;
  }
  ease = Math.max(1.3, ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
  ease = Math.round(ease * 1000) / 1000;
  return {
    ...rec,
    ease,
    interval,
    reps,
    lapses,
    due: addDays(today, interval),
    history: [...rec.history, { at: now, grade: quality }],
  };
}

export function isDue(rec: ReviewRec, today: string) {
  return rec.due <= today;
}
