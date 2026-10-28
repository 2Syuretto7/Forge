// Shared shapes for compiled content. Produced by scripts/build_content.ts,
// consumed by the app. Keep both sides in sync through this file only.

export type Track = 'math' | 'core' | 'arch' | 'sys' | 'llm' | 'all';
export type Stage = 'foundations' | 'learning' | 'models_gpus' | 'scale' | 'frontier';
export type EdgeType = 'vertical' | 'horizontal' | 'long_range';
export type Mode = 'theory' | 'practice' | 'both';

export interface Edge {
  from: string;
  to: string;
  type: EdgeType;
  note?: string;
}

export interface MovementSummary {
  id: string;
  file: string;
  title: string;
  mode: Mode;
  minutes: number;
  breakIt: boolean;
}

export interface LessonSummary {
  id: string;
  title: string;
  track: Track;
  stage: Stage;
  gpu: boolean;
  hours: number;
  theoryMinutes: number;
  practiceMinutes: number;
  capstone: string;
  movements: MovementSummary[];
  prereqs: string[];
  unlocks: string[];
  teaser: string;
}

export interface Annotation {
  source: string;
  target: string;
  movement: string;
  block: number;
  anchor: string;
  text: string;
}

export type ReviewKind = 'derivation' | 'kata' | 'concept' | 'prediction';

export interface ReviewItem {
  id: string;
  lesson: string;
  kind: ReviewKind;
  prompt: string;
  answer: string;
  answerKind: 'expr' | 'choice' | 'numeric' | 'text' | 'code';
  tol?: number;
  options?: { key: string; html: string }[];
  exercise?: string;
  explain?: string;
}

export interface ContentIndex {
  buildId: string;
  tracks: Track[];
  stages: Stage[];
  lessons: LessonSummary[];
  edges: Edge[];
  annotations: Annotation[];
  reviews: ReviewItem[];
  available: string[];
}

export interface DerivationStep {
  html: string;
  blanks: string[];
}

export interface ChoiceOption {
  key: string;
  html: string;
}

export type Block =
  | { t: 'html'; html: string }
  | { t: 'derivation'; id: string; title: string; steps: DerivationStep[] }
  | {
      t: 'predict';
      id: string;
      kind: 'choice' | 'numeric' | 'sketch';
      answer: string;
      tol: number;
      questionHtml: string;
      explainHtml: string;
      options: ChoiceOption[];
      xlabel: string;
      ylabel: string;
    }
  | { t: 'exercise'; ref: string }
  | { t: 'widget'; name: string; props: Record<string, string> }
  | { t: 'edge'; dir: 'to' | 'from'; lesson: string; text: string }
  | { t: 'feynman'; id: string; prompt: string; keyPoints: string[]; rubric: 'concept' | 'design' }
  | { t: 'colab'; notebook: string; tests: string[]; gpu: boolean }
  | { t: 'aside'; title: string; blocks: Block[] };

export interface Movement extends MovementSummary {
  blocks: Block[];
}

export interface Exercise {
  id: string;
  title: string;
  promptHtml: string;
  hints: string[];
  starter: string;
  solution: string;
  tests: string;
  testNames: string[];
  capstone: boolean;
  notebook: boolean;
}

export interface Hook {
  to: string;
  text: string;
}

export interface Reuse {
  from: string;
  concept: string;
}

export interface Lesson extends LessonSummary {
  movements: Movement[];
  exercises: Record<string, Exercise>;
  hooks: Hook[];
  reuses: Reuse[];
}
