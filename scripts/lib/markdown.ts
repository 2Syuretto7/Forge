// Compiles lesson markdown (with the directives of Section 6.3) into Block[].
// KaTeX is rendered here, at build time; the app only injects HTML.
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkMath from 'remark-math';
import remarkDirective from 'remark-directive';
import rehypeKatex from 'rehype-katex';
import { toHast } from 'mdast-util-to-hast';
import { toHtml } from 'hast-util-to-html';
import { toString as mdToString } from 'mdast-util-to-string';
import type { Root, RootContent, Parent } from 'mdast';
import type { Root as HastRoot } from 'hast';
import type { Block, ChoiceOption } from '../../src/content/types';

export interface CompileIssue {
  message: string;
}

export interface CompileResult {
  title: string;
  blocks: Block[];
  issues: CompileIssue[];
  plainText: string[];
}

const KNOWN = new Set([
  'derivation',
  'step',
  'predict',
  'reveal',
  'exercise',
  'widget',
  'edge',
  'feynman',
  'colab',
  'aside',
]);

type DirectiveNode = RootContent & {
  type: 'containerDirective' | 'leafDirective' | 'textDirective';
  name: string;
  attributes?: Record<string, string | null | undefined>;
  children: RootContent[];
};

function isDirective(n: RootContent): n is DirectiveNode {
  return n.type === 'containerDirective' || n.type === 'leafDirective' || n.type === 'textDirective';
}

const katexProcessor = unified().use(rehypeKatex, { strict: 'ignore', output: 'htmlAndMathml', throwOnError: true } as never);

export function nodesToHtml(nodes: RootContent[]): string {
  if (!nodes.length) return '';
  const root: Root = { type: 'root', children: nodes };
  const hast = toHast(root, { allowDangerousHtml: false }) as HastRoot;
  const out = katexProcessor.runSync(hast) as HastRoot;
  return toHtml(out);
}

// Unknown text/leaf directives come from prose such as "ratio 3:x". Turn them
// back into literal text so they render as written.
function restoreStrayDirectives(node: Parent) {
  node.children = node.children.map((c) => {
    const child = c as RootContent;
    if ((child.type === 'textDirective' || child.type === 'leafDirective') && !KNOWN.has((child as DirectiveNode).name)) {
      const d = child as DirectiveNode;
      const label = d.children.length ? `[${mdToString(d)}]` : '';
      return { type: 'text', value: `:${d.name}${label}` } as RootContent;
    }
    if ('children' in child) restoreStrayDirectives(child as Parent);
    return child;
  }) as typeof node.children;
}

const BLANK_TOKEN = (i: number) => `FORGEBLANK${i}X`;

// Pull [[answer]] blanks out of derivation regions before markdown parsing so
// that characters such as * inside answers are not read as emphasis.
function extractBlanks(src: string): { src: string; blanks: string[] } {
  const blanks: string[] = [];
  const out = src.replace(/(^|\n)(:{4,})derivation[\s\S]*?\n\2(?=\s*(\n|$))/g, (region) =>
    region.replace(/\[\[([\s\S]+?)\]\]/g, (_m, inner: string) => {
      blanks.push(inner.trim());
      return BLANK_TOKEN(blanks.length - 1);
    }),
  );
  return { src: out, blanks };
}

function attr(d: DirectiveNode, key: string): string | undefined {
  const v = d.attributes?.[key];
  return v == null ? undefined : String(v);
}

export function compileMarkdown(source: string, where: string): CompileResult {
  const issues: CompileIssue[] = [];
  const plainText: string[] = [];
  const { src, blanks } = extractBlanks(source);
  const tree = unified().use(remarkParse).use(remarkMath).use(remarkDirective).parse(src) as Root;
  restoreStrayDirectives(tree);

  let title = '';
  const children = [...tree.children];
  const firstHeading = children.findIndex((c) => c.type === 'heading' && c.depth === 1);
  if (firstHeading >= 0) {
    title = mdToString(children[firstHeading]);
    children.splice(firstHeading, 1);
  } else {
    issues.push({ message: `${where}: missing "# Title" heading` });
  }

  const blankHtml = (html: string, stepBlanks: string[]) =>
    html.replace(/FORGEBLANK(\d+)X/g, (_m, i: string) => {
      stepBlanks.push(blanks[Number(i)]);
      return `<span class="blank" data-blank="${stepBlanks.length - 1}">[ ${stepBlanks.length} ]</span>`;
    });

  function compileNodes(nodes: RootContent[]): Block[] {
    const blocks: Block[] = [];
    let run: RootContent[] = [];
    const flush = () => {
      if (run.length) {
        const html = nodesToHtml(run);
        if (/FORGEBLANK\d+X/.test(html)) issues.push({ message: `${where}: blank [[...]] outside a derivation step` });
        blocks.push({ t: 'html', html });
        plainText.push(run.map((n) => mdToString(n)).join('\n'));
        run = [];
      }
    };
    for (const n of nodes) {
      if (isDirective(n) && n.type !== 'textDirective' && KNOWN.has(n.name)) {
        flush();
        const b = compileDirective(n);
        if (b) blocks.push(b);
      } else {
        run.push(n);
      }
    }
    flush();
    return blocks;
  }

  function compileDirective(d: DirectiveNode): Block | null {
    switch (d.name) {
      case 'derivation': {
        const id = attr(d, 'id');
        if (!id) issues.push({ message: `${where}: derivation without id` });
        const steps = d.children.filter((c) => isDirective(c) && c.name === 'step') as DirectiveNode[];
        if (!steps.length) issues.push({ message: `${where}: derivation ${id} has no :::step children` });
        const intro = d.children.filter((c) => !(isDirective(c) && c.name === 'step'));
        return {
          t: 'derivation',
          id: id ?? 'missing',
          title: attr(d, 'title') ?? (intro.length ? mdToString({ type: 'root', children: intro } as Root) : ''),
          steps: steps.map((s) => {
            const stepBlanks: string[] = [];
            const html = blankHtml(nodesToHtml(s.children), stepBlanks);
            plainText.push(mdToString(s));
            return { html, blanks: stepBlanks };
          }),
        };
      }
      case 'predict': {
        const id = attr(d, 'id');
        const kind = attr(d, 'kind') as 'choice' | 'numeric' | 'sketch' | undefined;
        const answer = attr(d, 'answer');
        if (!id || !kind || answer == null) issues.push({ message: `${where}: predict needs id, kind and answer` });
        if (kind && !['choice', 'numeric', 'sketch'].includes(kind))
          issues.push({ message: `${where}: predict ${id} has unknown kind ${kind}` });
        const reveal = d.children.find((c) => isDirective(c) && c.name === 'reveal') as DirectiveNode | undefined;
        if (!reveal) issues.push({ message: `${where}: predict ${id} needs a :::reveal explanation` });
        const question = d.children.filter((c) => c !== reveal);
        let options: ChoiceOption[] = [];
        let qNodes = question;
        if (kind === 'choice') {
          const listIdx = question.findIndex((c) => c.type === 'list');
          if (listIdx < 0) issues.push({ message: `${where}: choice predict ${id} needs a list of options` });
          else {
            const list = question[listIdx] as Parent;
            options = list.children.map((li, i) => ({
              key: String.fromCharCode(97 + i),
              html: nodesToHtml((li as Parent).children as RootContent[]),
            }));
            qNodes = question.filter((_, i) => i !== listIdx);
            if (answer && !options.some((o) => o.key === answer))
              issues.push({ message: `${where}: predict ${id} answer ${answer} is not an option key` });
          }
        }
        if (kind === 'numeric' && answer != null && !Number.isFinite(parseFloat(answer)))
          issues.push({ message: `${where}: numeric predict ${id} answer is not a number` });
        if (kind === 'sketch' && answer != null) {
          const ys = answer.split(',').map(Number);
          if (ys.length < 3 || ys.some((y) => !Number.isFinite(y) || y < 0 || y > 1))
            issues.push({ message: `${where}: sketch predict ${id} answer must be 3+ values in [0,1]` });
        }
        plainText.push(mdToString(d));
        return {
          t: 'predict',
          id: id ?? 'missing',
          kind: kind ?? 'choice',
          answer: answer ?? '',
          tol: parseFloat(attr(d, 'tol') ?? (kind === 'sketch' ? '0.15' : '0')),
          questionHtml: nodesToHtml(qNodes),
          explainHtml: reveal ? nodesToHtml(reveal.children) : '',
          options,
          xlabel: attr(d, 'xlabel') ?? 'x',
          ylabel: attr(d, 'ylabel') ?? 'y',
        };
      }
      case 'exercise': {
        const ref = attr(d, 'ref');
        if (!ref) issues.push({ message: `${where}: exercise without ref` });
        return { t: 'exercise', ref: ref ?? 'missing' };
      }
      case 'widget': {
        const name = attr(d, 'name');
        if (!name) issues.push({ message: `${where}: widget without name` });
        const props: Record<string, string> = {};
        for (const [k, v] of Object.entries(d.attributes ?? {})) if (k !== 'name' && v != null) props[k] = String(v);
        return { t: 'widget', name: name ?? 'missing', props };
      }
      case 'edge': {
        const to = attr(d, 'to');
        const from = attr(d, 'from');
        const text = attr(d, 'text');
        if ((!to && !from) || !text) issues.push({ message: `${where}: edge needs to|from and text` });
        return { t: 'edge', dir: to ? 'to' : 'from', lesson: (to ?? from ?? '').toUpperCase(), text: text ?? '' };
      }
      case 'feynman': {
        const id = attr(d, 'id');
        const prompt = attr(d, 'prompt');
        const kp = attr(d, 'key_points');
        if (!id || !prompt || !kp) issues.push({ message: `${where}: feynman needs id, prompt and key_points` });
        return {
          t: 'feynman',
          id: id ?? 'missing',
          prompt: prompt ?? '',
          keyPoints: (kp ?? '').split('|').map((s) => s.trim()).filter(Boolean),
          rubric: attr(d, 'rubric') === 'design' ? 'design' : 'concept',
        };
      }
      case 'colab': {
        const nb = attr(d, 'notebook');
        if (!nb) issues.push({ message: `${where}: colab without notebook` });
        return { t: 'colab', notebook: (nb ?? '').toUpperCase(), tests: [] };
      }
      case 'aside': {
        const labelIdx = d.children.findIndex(
          (c) => c.type === 'paragraph' && (c as { data?: { directiveLabel?: boolean } }).data?.directiveLabel,
        );
        const label = labelIdx >= 0 ? mdToString(d.children[labelIdx]) : 'Going deeper';
        const rest = d.children.filter((_, i) => i !== labelIdx);
        return { t: 'aside', title: label, blocks: compileNodes(rest) };
      }
      case 'step':
      case 'reveal':
        issues.push({ message: `${where}: :::${d.name} outside its parent directive` });
        return null;
      default:
        return null;
    }
  }

  const blocks = compileNodes(children);
  return { title, blocks, issues, plainText };
}

export function collectDirectives(blocks: Block[], acc: Block[] = []): Block[] {
  for (const b of blocks) {
    acc.push(b);
    if (b.t === 'aside') collectDirectives(b.blocks, acc);
  }
  return acc;
}
