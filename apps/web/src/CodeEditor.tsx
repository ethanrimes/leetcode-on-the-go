import CodeMirror, {type ReactCodeMirrorProps} from '@uiw/react-codemirror';
import {python} from '@codemirror/lang-python';
import {oneDark} from '@codemirror/theme-one-dark';

export default function CodeEditor(props: ReactCodeMirrorProps) {
  return <CodeMirror {...props} extensions={[python()]} theme={oneDark}/>;
}
