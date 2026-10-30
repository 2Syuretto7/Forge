export const TRACK_LABEL: Record<string, string> = {
  math: 'Math',
  core: 'Core ML',
  arch: 'Architectures',
  sys: 'Systems (MLE)',
  llm: 'LLM science',
  all: 'All tracks',
};

export const STAGE_LABEL: Record<string, string> = {
  prelude: 'Prelude',
  foundations: 'Foundations',
  learning: 'Learning',
  models_gpus: 'Models + GPUs',
  scale: 'Scale',
  frontier: 'Frontier',
};

export const STATE_LABEL: Record<string, string> = {
  locked: 'Locked (preview available)',
  available: 'Available',
  in_progress: 'In progress',
  complete: 'Complete',
  optional: 'Optional review',
  unpublished: 'Not yet published',
};

export const STRAND_LABEL: Record<string, string> = {
  NUM: 'Number and information',
  ALG: 'Algebra and proof',
  LIN: 'Linear algebra',
  CAL: 'Calculus',
  PRB: 'Probability',
  OPT: 'Optimization',
  ALL: 'All strands',
};

// Short strand names for map column heads.
export const STRAND_SHORT: Record<string, string> = {
  NUM: 'Number',
  ALG: 'Algebra',
  LIN: 'Linear alg.',
  CAL: 'Calculus',
  PRB: 'Probability',
  OPT: 'Optimization',
};

// Stages are numbered from 0 when the curriculum opens with the Prelude (docs/math-track.md).
export function stageNumber(stages: string[], stage: string) {
  return stages.indexOf(stage) + (stages[0] === 'prelude' ? 0 : 1);
}

export function trackLabel(l: { track: string; strand?: string }) {
  return l.track === 'math' && l.strand ? `Math: ${STRAND_LABEL[l.strand]}` : TRACK_LABEL[l.track];
}
