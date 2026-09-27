import {cloneElement,useEffect,useId,useLayoutEffect,useRef,useState,type ButtonHTMLAttributes,type ReactElement} from 'react';
import {createPortal} from 'react-dom';
import {breadcrumbs,type Curriculum,type NodeStats} from '@pattern-atlas/core';

export function TileTooltip({stats:s,data,children}:{stats:NodeStats;data:Curriculum;children:ReactElement<ButtonHTMLAttributes<HTMLButtonElement>>}) {
 const id=useId(),popup=useRef<HTMLDivElement>(null),timer=useRef<ReturnType<typeof setTimeout>|undefined>(undefined);
 const [anchor,setAnchor]=useState<{x:number;y:number}|null>(null),[position,setPosition]=useState({left:14,top:14});
 const cancel=()=>clearTimeout(timer.current);
 const close=()=>{cancel();setAnchor(null);};
 const leave=()=>{cancel();timer.current=setTimeout(()=>setAnchor(null),120);};
 useEffect(()=>()=>clearTimeout(timer.current),[]);
 useEffect(()=>{
  if(!anchor)return;
  const key=(event:KeyboardEvent)=>{if(['Escape','PageDown','PageUp'].includes(event.key))close();};
  const scroll=(event:Event)=>{if(!popup.current?.contains(event.target as Node))close();};
  window.addEventListener('keydown',key);window.addEventListener('resize',close);window.addEventListener('wheel',scroll,true);window.addEventListener('touchmove',scroll,true);
  return()=>{window.removeEventListener('keydown',key);window.removeEventListener('resize',close);window.removeEventListener('wheel',scroll,true);window.removeEventListener('touchmove',scroll,true);};
 },[anchor]);
 useLayoutEffect(()=>{
  if(!anchor||!popup.current)return;
  const {width,height}=popup.current.getBoundingClientRect();
  const left=Math.max(14,Math.min(anchor.x+16,window.innerWidth-width-14));
  const preferred=anchor.y+16+height<=window.innerHeight-14?anchor.y+16:anchor.y-height-16;
  setPosition({left,top:Math.max(14,Math.min(preferred,window.innerHeight-height-14))});
 },[anchor]);
 const trigger=cloneElement(children,{
  'aria-describedby':anchor?id:undefined,
  onPointerEnter:event=>{cancel();if(event.pointerType!=='touch')setAnchor({x:event.clientX,y:event.clientY});},
  onPointerLeave:leave,
  onPointerDown:close,
  onFocus:event=>{if(!event.currentTarget.matches(':focus-visible'))return;cancel();const rect=event.currentTarget.getBoundingClientRect();setAnchor({x:rect.left+Math.min(rect.width/2,180),y:Math.max(14,Math.min(rect.top+rect.height/2,window.innerHeight-14))});},
  onBlur:close,
  onClick:event=>{close();children.props.onClick?.(event);}
 });
 const path=breadcrumbs(data.nodes,s.node.id).slice(0,-1).map(n=>n.title).join(' / ');
 return <>{trigger}{anchor&&createPortal(<div ref={popup} id={id} role="tooltip" className="tile-tooltip" style={position} onPointerEnter={cancel} onPointerLeave={leave}>
   {path&&<p className="tooltip-path">{path}</p>}
   <div className="tooltip-heading"><strong>{s.node.title}</strong><span>{s.node.level}</span></div>
   <p className="tooltip-description">{s.node.description}</p>
   <div className="tooltip-coverage"><strong>{s.solved} / {s.total}</strong><span>accepted · {Math.round(s.solved/s.total*100)}% coverage</span></div>
   <div className="tooltip-track"><span style={{width:`${s.solved/s.total*100}%`}}/></div>
   <dl><div><dt>Attempted, not accepted</dt><dd>{s.attempted}</dd></div><div><dt>No recorded attempt</dt><dd>{s.unseen}</dd></div><div><dt>Fresh practice</dt><dd>{s.fresh}</dd></div><div><dt>Needs refresh</dt><dd>{s.practiced-s.fresh}</dd></div><div><dt>No dated practice</dt><dd>{s.total-s.practiced}</dd></div><div><dt>Page entries</dt><dd>{s.visits}</dd></div></dl>
   <p className="tooltip-footer">{s.lastPracticed?`Last practiced ${new Date(s.lastPracticed).toLocaleDateString()}`:'Practice date unknown'}<span>Click for study links</span></p>
  </div>,document.body)}</>;
}
