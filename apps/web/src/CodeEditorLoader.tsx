import {lazy, Suspense} from 'react';
import type {ReactCodeMirrorProps} from '@uiw/react-codemirror';
const Editor = lazy(()=>import('./CodeEditor'));
export function CodeEditor(props: ReactCodeMirrorProps) {
  return <Suspense fallback={<div className="editor-loading">Opening your notebook…</div>}><Editor {...props}/></Suspense>;
}
