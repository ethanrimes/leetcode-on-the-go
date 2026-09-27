import {Children,isValidElement,type ReactNode} from 'react';
import * as Menu from '@radix-ui/react-select';
import {Check,ChevronDown,ChevronUp} from 'lucide-react';

// Existing option declarations stay readable; the popup is styled and keyboard accessible.
export function Select({value,onChange,children,disabled,'aria-label':label}: {
 value:string|number|undefined; onChange:(event:{target:{value:string}})=>void;
 children:ReactNode; disabled?:boolean; 'aria-label':string;
}) {
 const options=Children.toArray(children).flatMap(child=>isValidElement<{value?:string|number;children:ReactNode}>(child)?[child.props]:[]);
 const encode=(value:string)=>value===''?'__atlas_all__':value;
 return <Menu.Root value={encode(String(value??options[0]?.value??options[0]?.children??''))} disabled={disabled} onValueChange={v=>onChange({target:{value:v==='__atlas_all__'?'':v}})}>
  <Menu.Trigger className="atlas-select" aria-label={label}><Menu.Value/><Menu.Icon><ChevronDown size={15}/></Menu.Icon></Menu.Trigger>
  <Menu.Portal><Menu.Content className="atlas-select-menu" position="popper" sideOffset={6} collisionPadding={12}>
   <Menu.ScrollUpButton className="atlas-select-scroll"><ChevronUp size={14}/></Menu.ScrollUpButton>
   <Menu.Viewport>{options.map(option=>{const v=String(option.value??option.children);return <Menu.Item className="atlas-select-item" key={v} value={encode(v)}>
    <Menu.ItemText>{option.children}</Menu.ItemText><Menu.ItemIndicator><Check size={14}/></Menu.ItemIndicator>
   </Menu.Item>;})}</Menu.Viewport>
   <Menu.ScrollDownButton className="atlas-select-scroll"><ChevronDown size={14}/></Menu.ScrollDownButton>
  </Menu.Content></Menu.Portal>
 </Menu.Root>;
}
