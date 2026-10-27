import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import { expectedCode, verifyCode } from '../../src/lesson/colab';

describe('completion codes', () => {
  it('match the notebook autograder formula', async () => {
    const tests = ['test_speedup', 'test_matches_reference', 'test_report'];
    const hex = createHash('sha256').update(`L11:${[...tests].sort().join(',')}:forge`).digest('hex').slice(0, 8);
    expect(await expectedCode('L11', tests)).toBe(`FORGE-L11-${hex}`);
    expect(await verifyCode('L11', tests, ` FORGE-L11-${hex} `)).toBe(true);
    expect(await verifyCode('L11', tests.slice(1), `FORGE-L11-${hex}`)).toBe(false);
  });
});
