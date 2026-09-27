import {useMemo, useState} from 'react';
import {ArrowUpRight, Bookmark, ChevronRight, Code2, Search} from 'lucide-react';
import {libraryEntriesFor, problemOrders, sortProblems, type Curriculum, type Progress, type ProblemOrder} from '@pattern-atlas/core';

export function ProblemBrowser({data,progress,nodeId,initialQuery=''}:{data:Curriculum;progress:Progress;nodeId?:string;initialQuery?:string}) {
  const [query,setQuery]=useState(initialQuery);
  const [difficulty,setDifficulty]=useState('All difficulties');
  const [availability,setAvailability]=useState('All problems');
  const [topic,setTopic]=useState('All topics');
  const storageKey=`pattern-atlas.sort.${nodeId??'all'}`;
  const [order,setOrder]=useState<ProblemOrder>(()=>{try{const value=localStorage.getItem(storageKey);return problemOrders.some(o=>o.value===value)?value as ProblemOrder:'difficulty';}catch{return 'difficulty';}});
  const [limit,setLimit]=useState(50);
  const worked=useMemo(()=>new Map(data.problems.map(p=>[p.id,p])),[data]);
  const entries=useMemo(()=>libraryEntriesFor(data,nodeId),[data,nodeId]);
  const tags=useMemo(()=>[...new Set(entries.flatMap(p=>p.tags?.map(t=>t.name)??[]))].sort(),[entries]);
  const results=useMemo(()=>sortProblems(entries.filter(p=>{
    const card=worked.get(p.id);const q=query.trim().toLowerCase();
    return (difficulty==='All difficulties'||p.difficulty===difficulty)
      &&(availability==='All problems'||(availability==='With solutions'?!!card:availability==='Authored lessons'?card?.origin!=='community'&&!!card:!card))
      &&(topic==='All topics'||p.tags?.some(t=>t.name===topic))
      &&(!q||(/^\d+$/.test(q)?p.id===q:`${p.title} ${p.tags?.map(t=>t.name).join(' ')} ${card?.solutions.map(s=>s.title).join(' ')}`.toLowerCase().includes(q)));
  }),order),[entries,query,difficulty,availability,topic,order,worked]);
  const node=data.nodes.find(n=>n.id===nodeId);
  function changeOrder(value:ProblemOrder){setOrder(value);setLimit(50);try{localStorage.setItem(storageKey,value);}catch{/* Sorting remains available when storage is blocked. */}}
  return <section className="problem-browser">
    <div className="filterbar">
      <label className="search-field"><Search size={17}/><input aria-label="Filter problems" placeholder="Search title, number, or topic" value={query} onChange={e=>{setQuery(e.target.value);setLimit(50);}}/></label>
      <select aria-label="Problem difficulty" value={difficulty} onChange={e=>{setDifficulty(e.target.value);setLimit(50);}}>{['All difficulties','Easy','Medium','Hard'].map(v=><option key={v}>{v}</option>)}</select>
      <select aria-label="Solution availability" value={availability} onChange={e=>{setAvailability(e.target.value);setLimit(50);}}>{['All problems','With solutions','Authored lessons','Reference only'].map(v=><option key={v}>{v}</option>)}</select>
    </div>
    <div className="list-toolbar">
      <span role="status">{results.length.toLocaleString()} problems <span className="muted">/ {results.filter(p=>worked.has(p.id)).length.toLocaleString()} with solutions</span></span>
      <div><select aria-label="Official LeetCode topic" value={topic} onChange={e=>{setTopic(e.target.value);setLimit(50);}}>{['All topics',...tags].map(v=><option key={v}>{v}</option>)}</select>
      <select aria-label="Sort problems" value={order} onChange={e=>changeOrder(e.target.value as ProblemOrder)}>{problemOrders.map(o=><option key={o.value} value={o.value}>{o.label}</option>)}</select></div>
    </div>
    {node?.kind==='pattern'&&<p className="collection-note">Authored lessons demonstrate this pattern. Related practice comes from the source guide’s surrounding sections and may use neighboring techniques.</p>}
    <div className="problem-table-head"><span>PROBLEM</span><span>DIFFICULTY</span><span>CONTENT</span></div>
    <div className="problem-list catalog-list">{results.slice(0,limit).map(p=>{
      const card=worked.get(p.id);const authored=card&&card.origin!=='community';
      return <a key={p.id} data-problem-id={p.id} href={card?`#/problem/${p.id}${node?.kind==='pattern'&&card.patternIds.includes(node.id)?`?pattern=${node.id}`:''}`:`https://leetcode.com/problems/${p.slug}/`} target={card?undefined:'_blank'} rel={card?undefined:'noreferrer'}>
        <span className="status-circle"><Code2 size={15}/></span><div className="problem-name"><strong><span className="problem-number">{p.id}.</span> {p.title}</strong><small>{p.tags?.slice(0,4).map(t=>t.name).join(' · ')||'Official topic metadata unavailable'}</small></div>
        <span className={`tag ${p.difficulty.toLowerCase()}`}>{p.difficulty}</span><span className="content-kind">{authored?'Authored lesson':card?'Community solution':p.premium?'Premium reference':'Reference only'}</span>
        {progress.bookmarks.includes(p.id)&&<Bookmark size={13}/>}{card?<ChevronRight size={16}/>:<ArrowUpRight size={16}/>}
      </a>;
    })}</div>
    {!results.length&&<div className="empty-state"><h3>No matching problems</h3><p>Try a different difficulty, topic, or search.</p></div>}
    {results.length>limit&&<button className="button secondary load-more" onClick={()=>setLimit(n=>n+50)}>Show 50 more · {Math.min(limit,results.length)} of {results.length}</button>}
  </section>;
}
