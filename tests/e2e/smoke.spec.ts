import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const solution = (lesson: string, ex: string) =>
  fs.readFileSync(path.resolve('content/lessons', lesson, 'exercises', ex, 'solution.py'), 'utf8');

async function replaceEditorText(page: Page, text: string) {
  const editor = page.locator('.cm-content').first();
  await editor.click();
  await page.keyboard.press('ControlOrMeta+a');
  await page.keyboard.press('Delete');
  await page.keyboard.insertText(text);
}

test('dashboard, map, lesson, pass an exercise in the workspace, progress survives reload', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));

  await page.goto('./');
  await expect(page.getByRole('heading', { name: 'Welcome to Forge' })).toBeVisible();
  await expect(page.getByRole('link', { name: /Start learning/ })).toBeVisible();

  await page.goto('./#/map');
  await expect(page.locator('[aria-label^="L01 "]')).toBeVisible();
  const lessons = (fs.readFileSync(path.resolve('content/graph.yaml'), 'utf8').match(/^\s+- \{id: /gm) ?? []).length;
  await expect(page.locator('g[role="link"]')).toHaveCount(lessons);
  await page.locator('[aria-label^="L01 "]').click();
  await expect(page).toHaveURL(/#\/lesson\/L01/);

  await page.getByRole('button', { name: 'Syllabus' }).click();
  await page.getByRole('dialog').getByRole('link', { name: /Build: the toolkit from scratch/ }).click();
  const card = page.locator('#ex-e01');
  await card.getByRole('link', { name: /^Start exercise 1/ }).click();
  await expect(page).toHaveURL(/#\/lesson\/L01\/ex\/e01$/);
  await replaceEditorText(page, solution('L01', 'e01'));
  await page.getByRole('button', { name: 'Submit answer' }).click();
  await expect(page.getByText(/5\/5 tests passed/)).toBeVisible({ timeout: 120_000 });
  await expect(page.getByText('Passed', { exact: true })).toBeVisible();
  await expect(page.locator('.pill-xp')).toHaveText('100 XP');

  await page.reload();
  await expect(page.getByText('Passed', { exact: true })).toBeVisible();
  await page.goto('./#/lesson/L01/m3-build');
  await expect(page.locator('#ex-e01').getByText('Passed')).toBeVisible();
  await page.goto('./#/map');
  await expect(page.locator('[aria-label^="L01 "]')).toHaveAttribute('aria-label', /In progress/);
  await page.goto('./');
  await expect(page.getByRole('link', { name: /Resume/ })).toHaveAttribute('href', '#/lesson/L01/m3-build');
  expect(errors).toEqual([]);
});

test('export and import round-trip through the Settings screen', async ({ page }) => {
  await page.goto('./#/lesson/L01/m1-puzzle');
  await page.getByRole('textbox').first().fill('0');
  await page.getByRole('button', { name: 'Commit prediction' }).first().click();
  await page.goto('./#/settings');
  const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Export progress JSON' }).click()]);
  const file = await download.path();
  const exported = JSON.parse(fs.readFileSync(file!, 'utf8'));
  expect(exported.stores.predictions.length).toBe(1);

  await page.getByLabel('Type RESET to confirm').fill('RESET');
  await page.getByRole('button', { name: 'Reset progress' }).click();
  await expect(page.getByText('Progress reset.')).toBeVisible();

  await page.getByLabel('Choose a progress file to import').setInputFiles(file!);
  await expect(page.getByText(/Progress imported/)).toBeVisible();
  const [download2] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Export progress JSON' }).click()]);
  const again = JSON.parse(fs.readFileSync((await download2.path())!, 'utf8'));
  expect(again.stores).toEqual(exported.stores);
});
