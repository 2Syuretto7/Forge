export interface TestResult {
  name: string;
  status: 'pass' | 'fail' | 'skip' | 'error';
  message: string;
  seconds: number;
}

export type WorkerRequest =
  | { type: 'init'; base: string }
  | { type: 'run'; id: number; code: string }
  | { type: 'check'; id: number; code: string; tests: string };

export type WorkerResponse =
  | { type: 'ready' }
  | { type: 'status'; text: string }
  | { type: 'init-error'; message: string }
  | { type: 'run-result'; id: number; output: string; error: string | null }
  | { type: 'check-result'; id: number; output: string; results: TestResult[] };
