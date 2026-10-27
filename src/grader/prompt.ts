// Feynman grader prompts (EXECUTION_PLAN.md Section 9). The concept prompt is
// verbatim from the plan; the design prompt is its L24 design-document variant.

export const SYSTEM_PROMPT = `You grade a learner's plain-language explanation of an ML concept, in the spirit of Richard Feynman: if they cannot explain it simply, they do not yet understand it.
Score 0-4 on each criterion:
- correctness: every claim is true; no hidden errors.
- completeness: covers each listed key point.
- plainness: no jargon left unexplained; a motivated 14-year-old could follow.
- mechanism: explains why it works, not just what it does.
- example: includes a concrete example or analogy that is accurate.
Return only JSON: {"scores":{"correctness":n,"completeness":n,"plainness":n,"mechanism":n,"example":n},"gaps":["..."],"follow_up":"one probing question"}
Be strict and specific. Quote the learner's phrase when pointing at an error. Never write the explanation for them.`;

export const DESIGN_SYSTEM_PROMPT = `You grade a learner's design document for training, aligning, evaluating and serving a small language model. Every choice must be defended with evidence or with what the learner measured in earlier lessons.
Score 0-4 on each criterion:
- correctness: every technical claim and number is right; no hidden errors.
- completeness: covers each listed key point.
- justification: each decision cites a reason, a measurement, or an earlier lesson; nothing is chosen "because it is standard".
- tradeoffs: names the main alternative for each major decision and what would change the choice.
- clarity: a reviewer could reproduce the plan from the document alone.
Return only JSON: {"scores":{"correctness":n,"completeness":n,"justification":n,"tradeoffs":n,"clarity":n},"gaps":["..."],"follow_up":"one probing question"}
Be strict and specific. Quote the learner's phrase when pointing at an error. Never write the document for them.`;

export interface Criterion {
  key: string;
  label: string;
  description: string;
}

export const CONCEPT_CRITERIA: Criterion[] = [
  { key: 'correctness', label: 'Correctness', description: 'Every claim is true; no hidden errors.' },
  { key: 'completeness', label: 'Completeness', description: 'Covers each listed key point.' },
  { key: 'plainness', label: 'Plainness', description: 'No jargon left unexplained; a motivated 14-year-old could follow.' },
  { key: 'mechanism', label: 'Mechanism', description: 'Explains why it works, not just what it does.' },
  { key: 'example', label: 'Example', description: 'Includes a concrete example or analogy that is accurate.' },
];

export const DESIGN_CRITERIA: Criterion[] = [
  { key: 'correctness', label: 'Correctness', description: 'Every technical claim and number is right.' },
  { key: 'completeness', label: 'Completeness', description: 'Covers each listed key point.' },
  { key: 'justification', label: 'Justification', description: 'Each decision cites a reason, a measurement, or an earlier lesson.' },
  { key: 'tradeoffs', label: 'Tradeoffs', description: 'Names the main alternative for each major decision.' },
  { key: 'clarity', label: 'Clarity', description: 'A reviewer could reproduce the plan from the document alone.' },
];

export const WORD_LIMITS = { concept: [150, 400], design: [400, 1500] } as const;

export function userContent(lessonTitle: string, prompt: string, keyPoints: string[], text: string) {
  return [
    `Lesson: ${lessonTitle}`,
    `Prompt: ${prompt}`,
    `Key points:\n${keyPoints.map((k) => `- ${k}`).join('\n')}`,
    `Learner's text:\n"""\n${text}\n"""`,
  ].join('\n\n');
}
