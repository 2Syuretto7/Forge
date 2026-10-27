import { describe, expect, it } from 'vitest';
import { checkAnswer, parseBlank, parseExpr, evaluate, validateBlank } from '../../src/lib/expr';

const ok = (answer: string, input: string) => checkAnswer(parseBlank(answer), input).ok;

describe('expression checker', () => {
  it('accepts algebraically equivalent forms', () => {
    expect(ok('2*x', '2x')).toBe(true);
    expect(ok('2*x', 'x+x')).toBe(true);
    expect(ok('(a+b)^2', 'a^2 + 2*a*b + b**2')).toBe(true);
    expect(ok('sigmoid(z)*(1-sigmoid(z))', 'exp(-z)/(1+exp(-z))^2')).toBe(true);
    expect(ok('log(a*b)', 'log(a) + log(b)')).toBe(true);
    expect(ok('1/(n-1)', '1/(n - 1)')).toBe(true);
  });
  it('rejects non-equivalent forms and unknown symbols', () => {
    expect(ok('2*x', 'x^2')).toBe(false);
    expect(ok('n*p', 'n*q')).toBe(false);
    expect(ok('x/2', '2/x')).toBe(false);
  });
  it('uses a relative tolerance for numbers', () => {
    expect(ok('log(2)', '0.693')).toBe(true);
    expect(ok('log(2)', '0.69')).toBe(false);
    expect(ok('0.5|tol=0.1', '0.58')).toBe(true);
  });
  it('handles word answers', () => {
    expect(ok('word:orthogonal', ' Orthogonal ')).toBe(true);
    expect(ok('word:QR/qr decomposition', 'qr decomposition')).toBe(true);
    expect(ok('word:orthogonal', 'parallel')).toBe(false);
  });
  it('parses precedence correctly', () => {
    expect(evaluate(parseExpr('-x^2'), { x: 3 })).toBe(-9);
    expect(evaluate(parseExpr('2^-1'), {})).toBe(0.5);
    expect(evaluate(parseExpr('2(3+1)'), {})).toBe(8);
    expect(evaluate(parseExpr('e^0 + pi*0'), {})).toBe(1);
  });
  it('validates answer keys', () => {
    expect(validateBlank('2*x')).toBeNull();
    expect(validateBlank('2*(x')).not.toBeNull();
  });
});
