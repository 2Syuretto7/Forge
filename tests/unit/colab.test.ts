import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import { colabUrl, expectedCode, verifyCode } from '../../src/lesson/colab';

describe('completion codes', () => {
  it('match the notebook autograder formula', async () => {
    const tests = ['test_speedup', 'test_matches_reference', 'test_report'];
    const hex = createHash('sha256').update(`L07:${[...tests].sort().join(',')}:forge`).digest('hex').slice(0, 8);
    expect(await expectedCode('L07', tests)).toBe(`FORGE-L07-${hex}`);
    expect(await verifyCode('L07', tests, ` FORGE-L07-${hex} `)).toBe(true);
    expect(await verifyCode('L07', tests.slice(1), `FORGE-L07-${hex}`)).toBe(false);
  });

  it('open the committed notebook on the deployed branch', () => {
    expect(colabUrl('L04')).toBe('https://colab.research.google.com/github/2Syuretto7/Forge/blob/main/notebooks/L04.ipynb');
    expect(colabUrl('L07', 'dev')).toContain('/blob/dev/notebooks/L07.ipynb');
  });
});
