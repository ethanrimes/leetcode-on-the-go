import {useState} from 'react';
import * as Popover from '@radix-ui/react-popover';
import {Check,ChevronDown,Search,X} from 'lucide-react';

export interface MultiOption {value:string;label:string}
export function MultiSelect({label,allLabel,options,value,onChange,searchable=false}:{
  label:string;allLabel:string;options:MultiOption[];value:string[];onChange:(value:string[])=>void;searchable?:boolean;
}) {
  const [query,setQuery]=useState('');
  const chosen=new Set(value),visible=options.filter(option=>option.label.toLowerCase().includes(query.toLowerCase()));
  const summary=value.length===0?allLabel:value.length===1?options.find(option=>option.value===value[0])?.label??allLabel:`${value.length} selected`;
  return <Popover.Root onOpenChange={open=>{if(!open)setQuery('');}}>
    <Popover.Trigger className="atlas-select atlas-multiselect" aria-label={label} aria-haspopup="listbox">
      <span>{summary}</span><ChevronDown size={15}/>
    </Popover.Trigger>
    <Popover.Portal><Popover.Content className="atlas-multiselect-menu" align="start" sideOffset={6} collisionPadding={12}>
      <div className="multi-menu-head"><strong>{label}</strong><Popover.Close aria-label={`Close ${label}`}><X size={15}/></Popover.Close></div>
      {searchable&&<label className="multi-search"><Search size={15}/><input aria-label={`Search ${label}`} value={query} onChange={event=>setQuery(event.target.value)} placeholder="Find a category"/></label>}
      <div className="multi-options" role="listbox" aria-label={label} aria-multiselectable="true">
        {visible.map(option=><button key={option.value} type="button" role="option" aria-selected={chosen.has(option.value)} className="multi-option" onClick={()=>onChange(chosen.has(option.value)?value.filter(item=>item!==option.value):[...value,option.value])}><span className="multi-check">{chosen.has(option.value)&&<Check size={13}/>}</span><span>{option.label}</span></button>)}
        {!visible.length&&<p className="multi-empty">No matching categories</p>}
      </div>
      <div className="multi-menu-foot"><button type="button" onClick={()=>onChange([])} disabled={!value.length}>Clear selection</button><Popover.Close>Done</Popover.Close></div>
    </Popover.Content></Popover.Portal>
  </Popover.Root>;
}
