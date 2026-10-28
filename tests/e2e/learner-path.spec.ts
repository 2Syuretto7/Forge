import { test, expect, type Page } from '@playwright/test';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

// A simulated learner takes the whole curriculum, L01 to L24 in order: every
// prediction committed, every exercise and browser capstone passed with its
// solution, every Feynman block self-assessed, every Colab capstone verified
// with the code its autograder prints, every movement completed. After each
// lesson the map shows it complete and every lesson whose prerequisites are
// now complete as unlocked. Run with `npm run e2e:path` (about 20 minutes).

const root = path.resolve('content/lessons');
const graph = fs.readFileSync(path.resolve('content/graph.yaml'), 'utf8');
const ids = [...graph.matchAll(/^\s+- \{id: (L\d\d),/gm)].map((m) => m[1]);
const prereqs = (id: string) =>
  [...graph.matchAll(/^\s+- \{from: (L\d\d), to: (L\d\d), type: vertical/gm)].filter((m) => m[2] === id).map((m) => m[1]);
// Lesson order: the lowest-numbered lesson whose prerequisites are all done (L13 comes before L12).
const lessonIds: string[] = [];
while (lessonIds.length < ids.length) {
  lessonIds.push(ids.find((l) => !lessonIds.includes(l) && prereqs(l).every((p) => lessonIds.includes(p)))!);
}
const movements = (id: string) =>
  [...fs.readFileSync(path.join(root, id, 'lesson.yaml'), 'utf8').matchAll(/file: (m\d-[a-z]+)\.md/g)].map((m) => m[1]);
const solution = (id: string, ref: string) =>
  fs.readFileSync(ref === 'capstone' ? path.join(root, id, 'capstone', 'solution.py') : path.join(root, id, 'exercises', ref, 'solution.py'), 'utf8');
const completionCode = (id: string) => {
  const tests = [...fs.readFileSync(path.join(root, id, 'capstone', 'tests.py'), 'utf8').matchAll(/^def (test_\w+)/gm)].map((m) => m[1]);
  return `FORGE-${id}-${crypto.createHash('sha256').update(`${id}:${tests.sort().join(',')}:forge`).digest('hex').slice(0, 8)}`;
};

const EXPLANATION = Array.from({ length: 8 }, (_, i) =>
  `Point ${i + 1}: the idea holds because each step follows from the one before, and a small worked example makes it concrete.`,
).join(' ');

async function replaceEditorText(page: Page, text: string) {
  const editor = page.locator('.cm-content').first();
  await editor.click();
  await page.keyboard.press('ControlOrMeta+a');
  await page.keyboard.press('Delete');
  await page.keyboard.insertText(text);
}

async function completeMovement(page: Page, id: string, m: string, next?: string) {
  await page.goto(`./#/lesson/${id}/${m}`);
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();

  for (const card of await page.locator('.card.predict').all()) {
    if (await card.getByRole('button', { name: 'Commit prediction' }).count() === 0) continue;
    const radios = card.getByRole('radio');
    if (await radios.count()) await radios.first().check();
    const box = card.getByRole('textbox');
    if (await box.count()) await box.fill('1');
    await card.getByRole('button', { name: 'Commit prediction' }).click();
    await expect(card.getByRole('status')).toBeVisible();
  }

  for (const card of await page.locator('.card.exercise').all()) {
    const ref = (await card.getAttribute('id'))!.replace(/^ex-/, '');
    const open = card.getByRole('button', { name: 'Open in editor' });
    if (await open.count() === 0) continue; // a notebook capstone, completed through its Colab block
    if (await card.locator('.ex-status.passed').count()) continue;
    await open.click();
    await replaceEditorText(page, solution(id, ref));
    await page.getByRole('button', { name: 'Check', exact: true }).click();
    await expect(card.locator('.ex-status.passed')).toBeVisible({ timeout: 120_000 });
  }

  for (const card of await page.locator('.card.feynman').all()) {
    await card.locator('textarea').fill(EXPLANATION);
    for (const set of await card.locator('fieldset.selfrow').all()) await set.getByRole('radio').last().check();
    await card.getByRole('button', { name: 'Save self-assessment' }).click();
    await expect(card.getByText('This explanation counts toward completing the movement.')).toBeVisible();
  }

  const colab = page.locator('.colab');
  if (await colab.count()) {
    await colab.getByRole('textbox').fill(completionCode(id));
    await colab.getByRole('button', { name: 'Verify' }).click();
    await expect(colab.getByText(/Verified:/)).toBeVisible();
  }

  const done = page.getByRole('button', { name: /^Complete movement/ });
  await expect(done).toBeEnabled();
  await done.click();
  // Completing a movement moves on to the next one; the last shows the completion row.
  if (next) await expect(page).toHaveURL(new RegExp(`#/lesson/${id}/${next}$`));
  else await expect(page.getByText('Movement complete.')).toBeVisible();
}

test.describe.configure({ mode: 'serial' });

let page: Page;
const errors: string[] = [];

test.beforeAll(async ({ browser }) => {
  page = await browser.newPage();
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
});

test.afterAll(async () => {
  await page.close();
});

for (const id of lessonIds) {
  test(`learner completes ${id}`, async () => {
    test.setTimeout(1_800_000);
    await page.goto('./');
    const node = page.locator(`[aria-label^="${id} "]`);
    await expect(node).not.toHaveAttribute('aria-label', /\. Locked/);
    const ms = movements(id);
    for (const [i, m] of ms.entries()) await completeMovement(page, id, m, ms[i + 1]);

    await page.goto('./');
    await expect(page.locator(`[aria-label^="${id} "]`)).toHaveAttribute('aria-label', /\. Complete$/);
    const done = new Set(lessonIds.slice(0, lessonIds.indexOf(id) + 1));
    for (const next of lessonIds.filter((l) => !done.has(l) && prereqs(l).every((p) => done.has(p)))) {
      await expect(page.locator(`[aria-label^="${next} "]`)).not.toHaveAttribute('aria-label', /\. Locked/);
    }
    expect(errors).toEqual([]);
  });
}
