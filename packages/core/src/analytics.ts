import {mergeFamiliarity} from './diagnostic';
import {descendants, type Curriculum, type CurriculumNode, type Progress} from './index';

export interface Submission {id:string; slug:string; title:string; timestamp:string; status:string; language:string}
export interface LeetCodeHistory {through?:string; account:string; exportedAt:string; complete:boolean; submissions:Record<string,Submission>}
export interface SubmissionExport {through?:string; format:'pattern-atlas-leetcode'; version:1; account:string; exportedAt:string; complete:boolean; submissions:Submission[]}
export interface Visit {count:number; lastVisited:string}
export type Visits = Record<string,Record<string,Visit>>;
const object=(v:unknown):v is Record<string,unknown>=>!!v&&typeof v==='object'&&!Array.isArray(v);
const safe=(s:string)=>s.length>0&&s.length<=300&&!['__proto__','prototype','constructor'].includes(s);
const date=(v:unknown):v is string=>typeof v==='string'&&/^\d{4}-\d{2}-\d{2}T/.test(v)&&Number.isFinite(Date.parse(v));
export function validateHistory(value:unknown):LeetCodeHistory {
  if(!object(value)||typeof value.account!=='string'||!safe(value.account)||!date(value.exportedAt)||typeof value.complete!=='boolean'||!object(value.submissions)) throw new Error('Invalid LeetCode history.');
  if(value.through!==undefined&&(typeof value.through!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(value.through)))throw new Error('Invalid export cutoff date.');
  const submissions:Record<string,Submission>={};
  for(const [key,s] of Object.entries(value.submissions)) {
    if(!object(s)||!/^\d{1,30}$/.test(key)||s.id!==key||typeof s.slug!=='string'||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(s.slug)||s.slug.length>300||!date(s.timestamp)||!['title','status','language'].every(k=>typeof s[k]==='string'&&(s[k] as string).length<=500)||(s.status as string).length===0) throw new Error('A submission record is invalid. Nothing was imported.');
    submissions[key]={id:key,slug:s.slug,title:s.title as string,timestamp:s.timestamp,status:s.status as string,language:s.language as string};
  }
  return {through:value.through as string|undefined,account:value.account,exportedAt:value.exportedAt,complete:value.complete,submissions};
}
export function parseSubmissionExport(raw:string):LeetCodeHistory {
  if(raw.length>10_000_000)throw new Error('Submission file is too large (maximum 10 MB).');
  const value=JSON.parse(raw);
  if(!object(value)||value.format!=='pattern-atlas-leetcode'||value.version!==1||!Array.isArray(value.submissions))throw new Error('Choose a JSON file downloaded by the LeetCode exporter.');
  const records:Record<string,unknown>={};
  for(const s of value.submissions) {
    if(!object(s)||typeof s.id!=='string'||!/^\d{1,30}$/.test(s.id))throw new Error('Invalid submission ID.');
    records[s.id]=s;
  }
  return validateHistory({...value,submissions:records});
}
export function mergeHistory(current:LeetCodeHistory|undefined,incoming:LeetCodeHistory):LeetCodeHistory {
  if(current&&current.account.toLowerCase()!==incoming.account.toLowerCase())throw new Error(`This file belongs to ${incoming.account}. Your history belongs to ${current.account}. Use a separate workspace for another account.`);
  if(!current)return incoming;
  const incomingNewer=Date.parse(incoming.exportedAt)>=Date.parse(current.exportedAt);
  return {...(incomingNewer?incoming:current),submissions:incomingNewer?{...current.submissions,...incoming.submissions}:{...incoming.submissions,...current.submissions}};
}
export function validateVisits(value:unknown):Visits {
  if(!object(value))throw new Error('Invalid visit history.');
  const result:Visits={};
  for(const [device,pages] of Object.entries(value)) {
    if(!safe(device)||!object(pages))throw new Error('Invalid visit device.');
    result[device]={};
    for(const [page,v] of Object.entries(pages)) {
      if(!/^\/[a-zA-Z0-9/_-]*$/.test(page)||page.length>500||!object(v)||typeof v.count!=='number'||!Number.isSafeInteger(v.count)||v.count<0||!date(v.lastVisited))throw new Error('Invalid page visit.');
      result[device][page]={count:v.count,lastVisited:v.lastVisited};
    }
  }
  return result;
}
export function mergeVisits(a:Visits={},b:Visits={}):Visits {
  const result:Visits=structuredClone(a);
  for(const [device,pages] of Object.entries(b))for(const [page,v] of Object.entries(pages)) {
    result[device]??={}; const old=result[device][page];
    result[device][page]={count:Math.max(old?.count??0,v.count),lastVisited:old&&Date.parse(old.lastVisited)>Date.parse(v.lastVisited)?old.lastVisited:v.lastVisited};
  }
  return result;
}
export function recordVisit(progress:Progress,device:string,page:string,now=new Date()):Progress {
  const path=page.split('?')[0];
  if(!safe(device)||!/^\/[a-zA-Z0-9/_-]*$/.test(path))return progress;
  const pages=progress.visits?.[device]??{};
  return {...progress,visits:{...progress.visits,[device]:{...pages,[path]:{count:(pages[path]?.count??0)+1,lastVisited:now.toISOString()}}}};
}
export function pageVisits(visits:Visits={}):Record<string,Visit> {
  const result:Record<string,Visit>={};
  for(const pages of Object.values(visits))for(const [page,v]of Object.entries(pages)) {
    const old=result[page]; result[page]={count:(old?.count??0)+v.count,lastVisited:old&&old.lastVisited>v.lastVisited?old.lastVisited:v.lastVisited};
  }
  return result;
}
export function mergeProgress(current:Progress,incoming:Progress):Progress {
  // Check account before making any changes.
  const leetcode=incoming.leetcode?mergeHistory(current.leetcode,incoming.leetcode):current.leetcode;
  const cards={...current.cards};for(const [key,review]of Object.entries(incoming.cards))if(!cards[key]||Date.parse(review.lastReviewed)>Date.parse(cards[key].lastReviewed))cards[key]=review;
  const activity={...current.activity};for(const [day,count]of Object.entries(incoming.activity))activity[day]=Math.max(activity[day]??0,count);
  return {version:1,cards,drafts:{...incoming.drafts,...current.drafts},bookmarks:[...new Set([...current.bookmarks,...incoming.bookmarks])],activity,leetcode,familiarity:mergeFamiliarity(current.familiarity,incoming.familiarity),visits:mergeVisits(current.visits,incoming.visits)};
}
export const accepted=(s:Submission)=>s.status.toLowerCase()==='accepted';
export interface NodeStats {node:CurriculumNode;total:number;solved:number;attempted:number;unseen:number;visits:number;fresh:number;practiced:number;lastPracticed?:string;due:number}
export interface AnalyticsFilter {scope?:string;depth:number;difficulty?:string;query?:string;level?:string;since?:number;freshDays?:number;now?:number}
export function membershipIndex(data:Curriculum):Map<string,Set<string>> {
  const direct=new Map(data.nodes.map(n=>[n.id,new Set(n.problemIds??[])]));
  for(const p of data.problems)for(const id of [...p.patternIds,...(p.collectionIds??[])])direct.get(id)?.add(p.id);
  const children=new Map<string,string[]>();for(const n of data.nodes)if(n.parentId)children.set(n.parentId,[...(children.get(n.parentId)??[]),n.id]);
  const visited=new Set<string>();
  const collect=(id:string,trail=new Set<string>()):Set<string>=>{
    const ids=direct.get(id)??new Set<string>();if(visited.has(id)||trail.has(id))return ids;
    const next=new Set([...trail,id]);for(const child of children.get(id)??[])for(const p of collect(child,next))ids.add(p);
    visited.add(id);return ids;
  };
  for(const n of data.nodes)collect(n.id);return direct;
}
export function analytics(data:Curriculum,progress:Progress,filter:AnalyticsFilter,index=membershipIndex(data)) {
  const catalog=data.catalog??data.problems; const pages=pageVisits(progress.visits);
  const all=Object.values(progress.leetcode?.submissions??{});
  const now=filter.now??Date.now(),freshAfter=now-(filter.freshDays??30)*86400000;
  const lastPractice=new Map<string,string>(),dueIds=new Set<string>();
  const bySlug=new Map(catalog.map(p=>[p.slug,p.id]));
  const note=(id:string,date:string)=>{if(Date.parse(date)>Date.parse(lastPractice.get(id)??'1970-01-01'))lastPractice.set(id,date);};
  for(const s of all){const id=bySlug.get(s.slug);if(id)note(id,s.timestamp);}
  for(const [key,review] of Object.entries(progress.cards)){const id=key.split(':')[0];note(id,review.lastReviewed);if(Date.parse(review.due)<=now)dueIds.add(id);}

  const submissions=all.filter(s=>!filter.since||Date.parse(s.timestamp)>=filter.since);
  const solved=new Set(submissions.filter(accepted).map(s=>s.slug));const attempted=new Set(submissions.map(s=>s.slug));
  const eligible=new Map(catalog.filter(p=>!filter.difficulty||p.difficulty===filter.difficulty).map(p=>[p.id,p]));
  const children=(id?:string)=>data.nodes.filter(n=>(n.parentId??undefined)===id);
  const stats=(node:CurriculumNode):NodeStats=>{
    const problems=[...(index.get(node.id)??[])].flatMap(id=>eligible.get(id)?[eligible.get(id)!]:[]);
    const success=problems.filter(p=>solved.has(p.slug)).length;
    const tried=problems.filter(p=>attempted.has(p.slug)&&!solved.has(p.slug)).length;
    let visits=0;const queue=[node.id],seen=new Set<string>();
    for(let i=0;i<queue.length;i++){const id=queue[i];if(seen.has(id))continue;seen.add(id);visits+=pages[`/library/${id}`]?.count??0;queue.push(...children(id).map(n=>n.id));}
    const dates=problems.flatMap(p=>lastPractice.get(p.id)?[lastPractice.get(p.id)!]:[]).sort();
    return {node,total:problems.length,solved:success,attempted:tried,unseen:problems.length-success-tried,visits,fresh:dates.filter(d=>Date.parse(d)>=freshAfter).length,practiced:dates.length,lastPracticed:dates.at(-1),due:problems.filter(p=>node.kind==='pattern'?!!progress.cards[`${p.id}:${node.id}`]&&Date.parse(progress.cards[`${p.id}:${node.id}`].due)<=now:dueIds.has(p.id)).length};
  };
  const frontier=(id:string|undefined,depth:number):CurriculumNode[]=>children(id).flatMap(n=>depth>1&&children(n.id).length?frontier(n.id,depth-1):[n]);
  let nodes=frontier(filter.scope,filter.depth);if(!nodes.length&&filter.scope)nodes=data.nodes.filter(n=>n.id===filter.scope);
  const tiles=nodes.filter(n=>(!filter.level||n.level===filter.level)&&(!filter.query||n.title.toLowerCase().includes(filter.query.toLowerCase()))).map(stats).filter(s=>s.total>0).sort((a,b)=>b.total-a.total||a.node.id.localeCompare(b.node.id));
  const scopeIds=filter.scope?index.get(filter.scope):new Set(catalog.map(p=>p.id));
  const scopeProblems=[...eligible.values()].filter(p=>scopeIds?.has(p.id));
  const scopeSlugs=new Set(scopeProblems.map(p=>p.slug));
  const mappedSlugs=new Set(catalog.map(p=>p.slug));
  const branch=filter.scope?descendants(data.nodes,filter.scope):new Set(data.nodes.map(n=>n.id));
  const focus=data.nodes.filter(n=>n.kind==='pattern'&&branch.has(n.id)).map(stats).filter(s=>s.total>0&&(s.fresh<s.total||s.due>0)).sort((a,b)=>b.due-a.due||(b.practiced-b.fresh)-(a.practiced-a.fresh)||Number(b.practiced>0)-Number(a.practiced>0)||(a.node.priority==='Core'?-1:1)-(b.node.priority==='Core'?-1:1)||a.solved/a.total-b.solved/b.total).slice(0,6);
  return {tiles,focus,scopeProblems,solved:scopeProblems.filter(p=>solved.has(p.slug)).length,attempted:scopeProblems.filter(p=>attempted.has(p.slug)&&!solved.has(p.slug)).length,submissions:submissions.filter(s=>!filter.scope&&!filter.difficulty||scopeSlugs.has(s.slug)).sort((a,b)=>Date.parse(b.timestamp)-Date.parse(a.timestamp)||b.id.localeCompare(a.id,'en',{numeric:true})),unmapped:all.filter(s=>!mappedSlugs.has(s.slug)).length,pages};
}
export interface TileRect {index:number;x:number;y:number;width:number;height:number}
/** Balanced binary treemap: area is proportional to memberships, never to mastery. */
export function treemap(weights:number[],width=1000,height=560):TileRect[] {
  const result:TileRect[]=[];
  function split(items:{index:number;weight:number}[],x:number,y:number,w:number,h:number){
    if(!items.length)return;if(items.length===1){result.push({index:items[0].index,x,y,width:w,height:h});return;}
    const total=items.reduce((s,i)=>s+i.weight,0);let sum=items[0].weight,k=1;
    while(k<items.length-1&&Math.abs(total/2-(sum+items[k].weight))<Math.abs(total/2-sum)){sum+=items[k].weight;k++;}
    const ratio=sum/total;
    if(w>=h){split(items.slice(0,k),x,y,w*ratio,h);split(items.slice(k),x+w*ratio,y,w*(1-ratio),h);}
    else{split(items.slice(0,k),x,y,w,h*ratio);split(items.slice(k),x,y+h*ratio,w,h*(1-ratio));}
  }
  split(weights.map((weight,index)=>({weight,index})).filter(x=>x.weight>0),0,0,width,height);return result;
}
