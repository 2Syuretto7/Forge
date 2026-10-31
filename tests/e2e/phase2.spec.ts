import { test, expect } from '@playwright/test';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

// Reviews, Colab completion codes and retro-annotations, end to end: finish L08
// through its Colab block, see its review items come due the next day (in the
// review screen and in L09's reviews-first queue), and see L08's note appear in L07.

const lessonDir = (id: string) => path.resolve('content/lessons', id);
const movements = (id: string) =>
  [...fs.readFileSync(path.join(lessonDir(id), 'lesson.yaml'), 'utf8').matchAll(/file: (m\d-[a-z]+)\.md/g)].map((m) => m[1]);
const capstoneTests = (id: string) =>
  [...fs.readFileSync(path.join(lessonDir(id), 'capstone', 'tests.py'), 'utf8').matchAll(/^def (test_\w+)/gm)].map((m) => m[1]);
const completionCode = (id: string) =>
  `FORGE-${id}-${crypto.createHash('sha256').update(`${id}:${capstoneTests(id).sort().join(',')}:forge`).digest('hex').slice(0, 8)}`;
const reviewCount = (id: string) => JSON.parse(fs.readFileSync(path.resolve('content/reviews', `${id}.json`), 'utf8')).length;

function progressFile() {
  const done = (id: string, ms: string[], complete: boolean) => ({
    lessonId: id,
    status: complete ? 'complete' : 'in_progress',
    movementsDone: ms,
    startedAt: 1,
    completedAt: complete ? 2 : null,
    hoursLogged: 0,
  });
  const l08 = movements('L08');
  // A lesson unlocks once each published prerequisite is complete with its Feynman blocks
  // passed. Complete those of L08, and those of L09 other than L08, so that finishing L08
  // opens L09.
  const graph = fs.readFileSync(path.resolve('content/graph.yaml'), 'utf8');
  const prereqsOf = (to: string) =>
    [...graph.matchAll(new RegExp(`^\\s+- \\{from: ([LM]\\d\\d), to: ${to}, type: vertical`, 'gm'))]
      .map((m) => m[1])
      .filter((id) => fs.existsSync(path.join(lessonDir(id), 'lesson.yaml')));
  const prereqs = [...new Set([...prereqsOf('L08'), ...prereqsOf('L09')])].filter((id) => id !== 'L08');
  const feynmanIds = (id: string) =>
    fs
      .readdirSync(lessonDir(id))
      .filter((f) => f.endsWith('.md'))
      .flatMap((f) => [...fs.readFileSync(path.join(lessonDir(id), f), 'utf8').matchAll(/:::feynman\{id=(\w+)/g)].map((m) => m[1]));
  const passed = (id: string, f: string) => ({
    id: `${id}/${f}`,
    text: 'x',
    scores: {},
    gaps: [],
    followUp: '',
    bestTotal: 20,
    submissions: 0,
    selfAssessed: true,
    at: 1,
  });
  return {
    schemaVersion: 1,
    app: 'forge',
    exportedAt: new Date(0).toISOString(),
    stores: {
      progress: [...prereqs.map((id) => done(id, movements(id), true)), done('L08', l08.slice(0, -1), false)],
      exercises: [],
      predictions: [],
      feynman: prereqs.flatMap((id) => feynmanIds(id).map((f) => passed(id, f))),
      reviews: [],
      colab: [],
      settings: [],
    },
  };
}

test('Colab code completes L08, reviews come due the next day, annotations appear', async ({ page }, info) => {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  const day0 = new Date('2026-03-02T10:00:00');
  await page.clock.setSystemTime(day0);

  const file = info.outputPath('progress.json');
  fs.writeFileSync(file, JSON.stringify(progressFile()));
  await page.goto('./#/settings');
  await page.getByLabel('Choose a progress file to import').setInputFiles(file);
  await expect(page.getByText(/Progress imported/)).toBeVisible();

  // The annotation from L08 is hidden until L08 is complete.
  const note = /L08 automates exactly this/;
  await page.goto('./#/lesson/L07/m2-derivation');
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  await expect(page.getByText(note)).toHaveCount(0);

  // Colab block: a wrong code is rejected, the autograder's code is accepted.
  await page.goto('./#/lesson/L08/m7-capstone');
  const colab = page.locator('.colab');
  await expect(colab.getByText('the default CPU runtime is enough')).toBeVisible();
  await colab.getByRole('textbox').fill('FORGE-L08-00000000');
  await colab.getByRole('button', { name: 'Verify' }).click();
  await expect(colab.getByRole('alert')).toBeVisible();
  await colab.getByRole('textbox').fill(completionCode('L08').toLowerCase());
  await colab.getByRole('button', { name: 'Verify' }).click();
  await expect(colab.getByText(/Verified:/)).toBeVisible();
  await page.getByRole('button', { name: 'Complete movement and lesson' }).click();
  await expect(page.getByText('Movement complete.')).toBeVisible();

  // Completing the lesson schedules its items for tomorrow, not today.
  const n = reviewCount('L08');
  await page.goto('./#/review');
  await expect(page.getByText('No reviews due today.')).toBeVisible();
  await expect(page.getByText(`${n} items scheduled for later days`)).toBeVisible();

  await page.goto('./#/lesson/L07/m2-derivation');
  await expect(page.getByText(note)).toBeVisible();

  // One day later the items are due: in the review screen and in L09's reviews-first queue.
  await page.clock.setSystemTime(new Date(day0.getTime() + 24 * 3600 * 1000));
  await page.goto('./#/review');
  await page.reload();
  await expect(page.getByText(`${n} items left in this session`)).toBeVisible();
  await expect(page.getByRole('link', { name: `Reviews (${n} due)` })).toBeVisible();

  // L09 is open (its prerequisites are complete) and its first step not yet opened, so
  // the due items come first, in the reviews-first queue that replaces the recall bridge.
  await page.goto('./#/lesson/L09/m0-recall');
  const bridge = page.getByRole('region', { name: 'Reviews first' });
  await expect(bridge.getByText(`${n} items left in this session`)).toBeVisible();
  const card = bridge.locator('.review-card');
  await expect(card).toHaveAttribute('aria-label', /from L08$/);

  // Grading one item reschedules it and removes it from today's queue.
  const reveal = card.getByRole('button', { name: /Show answer|Check/ });
  if (await card.getByRole('textbox').count()) await card.getByRole('textbox').first().fill('1');
  if (await card.getByRole('radio').count()) await card.getByRole('radio').first().check();
  if (await reveal.count()) await reveal.click();
  await card.getByRole('button', { name: /^5:/ }).click();
  await expect(bridge.getByText(`${n - 1} items left in this session`)).toBeVisible();
  await expect(page.getByRole('link', { name: `Reviews (${n - 1} due)` })).toBeVisible();
  expect(errors).toEqual([]);
});
