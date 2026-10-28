import { useEffect, useRef } from 'react';
import { EditorView, basicSetup } from 'codemirror';
import { EditorState } from '@codemirror/state';
import { keymap } from '@codemirror/view';
import { indentWithTab } from '@codemirror/commands';
import { python } from '@codemirror/lang-python';
import { HighlightStyle, syntaxHighlighting } from '@codemirror/language';
import { tags as t } from '@lezer/highlight';

interface Props {
  value: string;
  onChange: (v: string) => void;
  onRun?: () => void;
  onCheck?: () => void;
  label: string;
}

// Always dark, as on Codecademy and DataCamp, whatever the page theme.
const theme = EditorView.theme(
  {
    '&': { backgroundColor: 'var(--editor-bg)', color: 'var(--editor-text)', fontSize: '14px', height: '100%' },
    '.cm-content': { fontFamily: 'var(--mono)', caretColor: '#ffffff', padding: '10px 0' },
    '.cm-cursor, .cm-dropCursor': { borderLeftColor: '#ffffff' },
    '.cm-gutters': { backgroundColor: 'var(--editor-bg)', color: 'var(--editor-muted)', border: 'none' },
    '.cm-activeLine': { backgroundColor: 'var(--editor-active)' },
    '.cm-activeLineGutter': { backgroundColor: 'var(--editor-active)', color: 'var(--editor-text)' },
    '&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': { backgroundColor: '#34437a' },
    '.cm-matchingBracket, &.cm-focused .cm-matchingBracket': { backgroundColor: '#2c3a6b', outline: '1px solid #5b6ba8' },
    '.cm-tooltip': { backgroundColor: 'var(--editor-panel)', color: 'var(--editor-text)', border: '1px solid var(--editor-border)' },
    '.cm-panels': { backgroundColor: 'var(--editor-panel)', color: 'var(--editor-text)' },
    '&.cm-focused': { outline: '2px solid var(--focus)', outlineOffset: '-2px' },
    '.cm-scroller': { overflow: 'auto', lineHeight: '1.6' },
  },
  { dark: true },
);

const highlight = HighlightStyle.define([
  { tag: [t.keyword, t.controlKeyword, t.definitionKeyword, t.moduleKeyword, t.operatorKeyword], color: '#c792ea' },
  { tag: [t.string, t.special(t.string)], color: '#c3e88d' },
  { tag: [t.number, t.bool, t.null], color: '#f9a77c' },
  { tag: t.comment, color: '#8a96bb', fontStyle: 'italic' },
  { tag: [t.function(t.variableName), t.function(t.propertyName)], color: '#82aaff' },
  { tag: [t.className, t.typeName], color: '#ffcb6b' },
  { tag: [t.operator, t.punctuation], color: '#89ddff' },
  { tag: [t.self, t.special(t.variableName)], color: '#ff8a9a' },
  { tag: [t.variableName, t.propertyName], color: '#e6ebf7' },
]);

export function Editor({ value, onChange, onRun, onCheck, label }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const view = useRef<EditorView | null>(null);
  const cbs = useRef({ onChange, onRun, onCheck });
  cbs.current = { onChange, onRun, onCheck };

  useEffect(() => {
    const v = new EditorView({
      parent: host.current!,
      state: EditorState.create({
        doc: value,
        extensions: [
          basicSetup,
          python(),
          theme,
          syntaxHighlighting(highlight),
          keymap.of([
            { key: 'Mod-Enter', run: () => (cbs.current.onCheck?.(), true) },
            { key: 'Shift-Enter', run: () => (cbs.current.onRun?.(), true) },
            indentWithTab,
          ]),
          EditorView.updateListener.of((u) => {
            if (u.docChanged) cbs.current.onChange(u.state.doc.toString());
          }),
          EditorView.contentAttributes.of({ 'aria-label': label }),
        ],
      }),
    });
    view.current = v;
    return () => v.destroy();
    // Created once per mount; value changes from outside go through the effect below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const v = view.current;
    if (v && v.state.doc.toString() !== value) {
      v.dispatch({ changes: { from: 0, to: v.state.doc.length, insert: value } });
    }
  }, [value]);

  return <div ref={host} className="editor-host" />;
}
