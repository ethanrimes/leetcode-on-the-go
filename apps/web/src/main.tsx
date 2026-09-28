import {Select} from './Select';
import React, {useEffect, useMemo, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {CodeEditor} from './CodeEditorLoader';
import {DiagnosticPage, FamiliarityDashboard} from './Diagnostic';
import {ProgressDashboard,LeetCodeSummary} from './ProgressDashboard';
import {ProblemBrowser} from './ProblemBrowser';

import {ArrowRight, ArrowUpRight, BookOpen, Bookmark, Check, CheckCheck, ChevronDown, ChevronRight, CircleHelp, Code2, Download, ExternalLink, Eye, Flame, GitBranch, GraduationCap, Layers3, LayoutDashboard, Leaf, ListFilter, Menu, Network, Play, RotateCcw, Search, Settings2, Shuffle, Sparkles, Target, Timer, TrendingUp, Upload, X} from 'lucide-react';
import {mergeHistory, mergeProgress, parseSubmissionExport, recordVisit, breadcrumbs, cardKey, dayKey, descendants, emptyProgress, isLearned, parseProgress, problemsFor, rateCard, studyQueue, type CatalogProblem, type Curriculum, type CurriculumNode, type Problem, type Progress, type Rating, libraryEntriesFor} from '@pattern-atlas/core';
import './styles.css';

const STORAGE='pattern-atlas.progress.v1';
const SYNC_KEY='pattern-atlas.cloud-sync-key';
type CloudState='loading'|'connected'|'sign-in'|'error'|'local';
const cloudHeaders=(key:string):Record<string,string>=>key?{'x-pattern-atlas-sync-key':key}:{};
function readSyncKey(){try{return localStorage.getItem(SYNC_KEY)??'';}catch{return '';}}
function exportHistory(history:NonNullable<Progress['leetcode']>) {
  return JSON.stringify({...history,format:'pattern-atlas-leetcode',version:1,submissions:Object.values(history.submissions)});
}
function readSavedProgress():Progress {
  let raw:string|null=null;
  try {raw=localStorage.getItem(STORAGE);return raw?parseProgress(raw):emptyProgress();}
  catch {if(raw){try{localStorage.setItem(`${STORAGE}.recovery`,raw);}catch{/* Browser storage may be unavailable. */}}return emptyProgress();}
}
const navigate=(path:string)=>{window.location.hash=path; window.scrollTo({top:0,behavior:'instant'});};
const nodePath=(id:string)=>`/library/${id}`;
const problemPath=(id:string,pattern?:string)=>`/problem/${id}${pattern?`?pattern=${pattern}`:''}`;
const difficultyClass=(level:string)=>level.toLowerCase();
const icons=[Layers3,ArrowRight,Search,GitBranch,Network,Leaf,Code2,Sparkles,BookOpen,Target,ListFilter,Shuffle];
function useRoute(){
  const [route,setRoute]=useState(window.location.hash.slice(1)||'/');
  useEffect(()=>{const listener=()=>setRoute(window.location.hash.slice(1)||'/'); window.addEventListener('hashchange',listener); return()=>window.removeEventListener('hashchange',listener);},[]);
  return route;
}
function Tag({children,kind='neutral'}:{children:React.ReactNode;kind?:string}){return <span className={`tag ${difficultyClass(kind)}`}>{children}</span>;}
function App(){
  const [data,setData]=useState<Curriculum>(); const [catalog,setCatalog]=useState<CatalogProblem[]>([]); const [loadError,setLoadError]=useState('');
  const [progress,setProgress]=useState<Progress>(readSavedProgress);
  const [toast,setToast]=useState(''); const [storageError,setStorageError]=useState(''); const [mobileNav,setMobileNav]=useState(false); const [search,setSearch]=useState('');
  const [syncKey,setSyncKey]=useState(readSyncKey),[cloudState,setCloudState]=useState<CloudState>('loading');
  const [cloudMessage,setCloudMessage]=useState(''); const [syncAttempt,setSyncAttempt]=useState(0);
  const lastCloudHistory=useRef('');
  const route=useRoute(); const [path,query='']=route.split('?'); const params=new URLSearchParams(query); const parts=path.split('/').filter(Boolean);
  const lastPage=useRef('');
  useEffect(()=>{if(!data||lastPage.current===path)return;lastPage.current=path;
    let device:string;try{device=localStorage.getItem('pattern-atlas.device')||crypto.randomUUID();localStorage.setItem('pattern-atlas.device',device);}catch{device='session-'+crypto.randomUUID();}
    setProgress(p=>recordVisit(p,device,path));
  },[path,data]);
  const importRef=useRef<HTMLInputElement>(null);
  useEffect(()=>{let cancelled=false; fetch('/content/curriculum.json?v=3').then(async response=>{
    if(!response.ok) throw new Error('The curriculum could not be loaded.');
    const content:Curriculum=await response.json();
    if(!cancelled){setData(content);setCatalog(content.catalog??content.problems);}
  }).catch(e=>!cancelled&&setLoadError(e.message));return()=>{cancelled=true;};},[]);
  useEffect(()=>{try{localStorage.setItem(STORAGE,JSON.stringify(progress));setStorageError('');}catch{setStorageError('Your browser could not save this change. Export a backup to keep your work.');}},[progress]);
  useEffect(()=>{
    if(['localhost','127.0.0.1'].includes(location.hostname)){setCloudState('local');return;}
    let cancelled=false;
    lastCloudHistory.current='';
    setCloudState('loading');
    fetch('/api/history',{headers:cloudHeaders(syncKey),cache:'no-store'}).then(async response=>{
      if(cancelled)return;
      if(response.status===401){setCloudState('sign-in');setCloudMessage('Sign in with the owner GitHub account or enter your sync key.');return;}
      if(!response.ok&&response.status!==204)throw new Error(`Cloud history is unavailable (${response.status}).`);
      if(response.status===200){const incoming=parseSubmissionExport(await response.text());
        if(!cancelled){lastCloudHistory.current=exportHistory(incoming);setProgress(current=>({...current,leetcode:mergeHistory(current.leetcode,incoming)}));}}
      if(!cancelled){setCloudState('connected');setCloudMessage('Your LeetCode history is stored in Azure.');}
    }).catch(error=>{if(!cancelled){setCloudState('error');setCloudMessage(error instanceof Error?error.message:'Cloud history is unavailable.');}});
    return()=>{cancelled=true;};
  },[syncKey,syncAttempt]);
  useEffect(()=>{
    if(cloudState!=='connected'||!progress.leetcode)return;
    const serialized=exportHistory(progress.leetcode);
    if(serialized===lastCloudHistory.current)return;
    const timer=setTimeout(()=>{
      fetch('/api/history',{method:'POST',headers:{...cloudHeaders(syncKey),'Content-Type':'application/json'},
        body:serialized}).then(async response=>{
          if(!response.ok)throw new Error(`Cloud update failed (${response.status}).`);
          lastCloudHistory.current=serialized;
          setCloudMessage('Your LeetCode history is stored in Azure.');
        }).catch(error=>{setCloudState('error');setCloudMessage(error instanceof Error?error.message:'Cloud update failed.');});
    },900);
    return()=>clearTimeout(timer);
  },[progress.leetcode,cloudState,syncKey]);
  function connectWithKey(key:string){
    const value=key.trim();try{if(value)localStorage.setItem(SYNC_KEY,value);else localStorage.removeItem(SYNC_KEY);}catch{}
    setSyncKey(value);setSyncAttempt(current=>current+1);
  }
  useEffect(()=>{if(!toast)return; const timer=setTimeout(()=>setToast(''),4500);return()=>clearTimeout(timer);},[toast]);
  useEffect(()=>setMobileNav(false),[route]);
  function exportProgress(){const url=URL.createObjectURL(new Blob([JSON.stringify(progress,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`pattern-atlas-${dayKey(new Date())}.json`;a.click();URL.revokeObjectURL(url);setToast('Progress and drafts exported.');}
  async function importProgress(file?:File){if(!file)return;try{
    const incoming=parseProgress(await file.text());
    mergeProgress(progress,incoming);
    setProgress(current=>mergeProgress(current,incoming));
    setToast('Backup merged. Existing drafts were kept; newer review records were imported.');
  }catch(error){setToast(error instanceof Error?error.message:'Could not import this backup.');}finally{if(importRef.current)importRef.current.value='';}}
  if(!data)return <div className="loading"><div className="brand-mark"><Layers3/></div><h1>Pattern Atlas</h1><p>{loadError||'Opening your study library…'}</p>{loadError&&<button onClick={()=>location.reload()}>Try again</button>}</div>;
  const roots=data.nodes.filter(n=>!n.parentId); const patterns=data.nodes.filter(n=>n.kind==='pattern');
  const reviewed=Object.keys(progress.cards).length; const mastered=data.problems.filter(p=>isLearned(progress,p)).length;
  const due=Object.values(progress.cards).filter(r=>Date.parse(r.due)<=Date.now()).length;
  const active=parts[0]||'overview';
  const common={data,progress,setProgress,setToast};
  const navigation=[['overview','Overview',LayoutDashboard],['library','Pattern library',Network],['review','Practice deck',Layers3],['diagnostic','Diagnostic test',CheckCheck],['catalog','All problems',Code2],['progress','Your progress',TrendingUp]] as const;
  return <div className="app-shell">
    {mobileNav&&<button className="nav-scrim" aria-label="Close navigation" onClick={()=>setMobileNav(false)}/>}
    <aside id="workspace-navigation" onClick={e=>{if((e.target as HTMLElement).closest('a'))setMobileNav(false);}} className={`sidebar ${mobileNav?'open':''}`}>
      <a className="brand" href="#/"><span className="brand-mark"><Layers3 size={23}/></span><span>Pattern Atlas<small>ALGORITHM STUDY WORKSPACE</small></span></a>
      <div className="sidebar-label">YOUR WORKSPACE</div>
      <nav aria-label="Main navigation">{navigation.map(([key,label,Icon])=><a key={key} className={active===key?'active':''} href={key==='overview'?'#/':`#/${key}`}><Icon size={18}/>{label}{key==='review'&&due>0&&<span className="nav-count">{due}</span>}</a>)}</nav>
      <div className="sidebar-label topics-label">EXPLORE TOPICS <span>{roots.length}</span></div>
      <nav className="topic-nav" aria-label="Topics">{roots.map((n,i)=>{const Icon=icons[i%icons.length];return <a key={n.id} className={parts[1]===n.id?'selected-topic':''} href={`#${nodePath(n.id)}`}><Icon size={16}/><span>{n.title}</span></a>;})}</nav>
      <div className="sidebar-bottom"><div className="small-sprout"><Code2 size={18}/><span>PERSONAL WORKSPACE<br/><strong>Drafts saved on this device</strong></span></div><a href="#/about"><CircleHelp size={16}/> About the curriculum <ArrowUpRight size={14}/></a></div>
    </aside>
    <div className="workspace">
      <header className="topbar"><div className="topbar-title"><button className="icon-button mobile-menu" aria-label="Open navigation" aria-controls="workspace-navigation" aria-expanded={mobileNav} onClick={()=>setMobileNav(true)}><Menu size={20}/></button><span>Learning workspace</span><ChevronRight size={14}/><strong>{navigation.find(n=>n[0]===active)?.[1]??(active==='problem'?'Problem study':'Curriculum notes')}</strong></div>
        <form className="global-search" onSubmit={e=>{e.preventDefault();navigate(`/catalog?q=${encodeURIComponent(search)}`);}}><button type="button" aria-label="Open problem search" className="search-trigger" onClick={()=>navigate('/catalog')}><Search size={17}/></button><input aria-label="Search all problems" placeholder="Find a problem or pattern…" value={search} onChange={e=>setSearch(e.target.value)}/><kbd>↵</kbd></form>
        <span className="local-avatar" title="Your study workspace">You</span>
      </header>
      {storageError&&<div className="storage-warning" role="alert">{storageError}<button onClick={exportProgress}>Export backup</button></div>}
      <main id="main" key={route}>
        {active==='overview'&&<>
          <div className="page-heading"><div><p className="eyebrow">ALGORITHMS / SYSTEMATIC PRACTICE</p><h1>Algorithm practice,<br/><span>organized.</span></h1><p className="lead">A structured library of techniques, problems, and reference implementations.</p></div><a className="button secondary" href="#/catalog">Browse all problems <ArrowUpRight size={16}/></a></div>
          <section className="stats-row" aria-label="Curriculum statistics"><div><strong>{patterns.length}</strong><span>authored patterns</span></div><div><strong>{data.problems.length.toLocaleString()}</strong><span>problems with solutions</span></div><div><strong>{catalog.length.toLocaleString()}</strong><span>indexed problems</span></div><div><strong>{mastered}</strong><span>recalled twice</span></div></section>
          <div className="overview-top"><section className="daily-card"><div className="daily-content"><p className="eyebrow">RECALL SESSION</p><h2>Test your understanding.</h2><p>Draft an approach, reveal the implementation, and assess your recall.</p><button className="button primary" onClick={()=>navigate('/review')}>Start a study session <ArrowRight size={17}/></button><span className="session-meta"><Timer size={14}/> 10 problems · self-paced</span></div></section>
            <section className="progress-card"><div className="card-topline"><h3>Review activity</h3><TrendingUp size={18}/></div><div className="rhythm-value">{Object.values(progress.activity).reduce((a,b)=>a+b,0)}<span>recall attempts</span></div><div className="week-bars">{Array.from({length:7},(_,i)=>{const d=new Date();d.setDate(d.getDate()-6+i);const count=progress.activity[dayKey(d)]??0;return <div key={i} className={i===6?'today':''} title={`${dayKey(d)}: ${count} reviews`}><div className="bar-track"><i style={{height:`${Math.max(5,Math.min(100,count*10))}%`}}/></div><span>{d.toLocaleDateString('en',{weekday:'narrow'})}</span></div>;})}</div><div className="rhythm-footer"><span>{due} problems due for review</span><a href="#/progress"><ArrowUpRight size={17}/><span className="sr-only">View progress</span></a></div></section></div>
          <div className="section-heading"><div><p className="eyebrow">CURRICULUM INDEX</p><h2>Topics and techniques</h2></div><a className="text-link" href="#/library">Open full library <ArrowRight size={16}/></a></div>
          <CategoryGrid data={data} nodes={roots} progress={progress}/>
          <section className="bottom-note"><GraduationCap size={22}/><div><strong>From core patterns to extended practice.</strong><p>200 authored patterns, 313 source-guide practice sets, and attributed community implementations.</p></div><a href="#/about">How this works <ArrowUpRight size={15}/></a></section>
        </>}
        {active==='library'&&<Library {...common} nodeId={parts[1]}/>}
        {active==='problem'&&<ProblemStudy {...common} problem={data.problems.find(p=>p.id===parts[1])} requestedPattern={params.get('pattern')??undefined}/>}
        {active==='review'&&<ReviewSession {...common} nodeId={params.get('topic')??undefined}/>}
        {active==='diagnostic'&&<DiagnosticPage {...common} initialScope={params.get('topic')??''} initialMode={params.get('mode')==='uncertain'?'uncertain':'unassessed'} initialCommunity={params.get('community')==='1'}/>}
        {active==='catalog'&&<Catalog {...common} catalog={catalog} initialQuery={params.get('q')??''}/>}
        {active==='progress'&&<>
          <p className="eyebrow">PRACTICE / COVERAGE / FRESHNESS</p><h1>Your progress</h1><p className="lead">Find the patterns to revisit and the gaps to work on next.</p>
          <CloudHistoryPanel state={cloudState} message={cloudMessage} onRetry={()=>setSyncAttempt(current=>current+1)} onConnect={connectWithKey}/>
          <LeetCodeSummary progress={progress}/>
          <FamiliarityDashboard data={data} progress={progress}/>
          <ProgressDashboard {...common}/>
          <div className="section-heading"><h2>Recall practice</h2></div><section className="stats-row"><div><strong>{reviewed}</strong><span>cards reviewed</span></div><div><strong>{mastered}</strong><span>recalled twice</span></div><div><strong>{due}</strong><span>due for review</span></div></section>
          <div className="section-heading"><h2>Saved for later</h2></div><ProblemList {...common} problems={data.problems.filter(p=>progress.bookmarks.includes(p.id))}/>
          <section className="backup-panel"><div><h3>Your work travels with you</h3><p>LeetCode completions and submissions sync from Azure when connected. Drafts, ratings, and page visits are saved in this browser; export a backup to transfer them. Import preserves existing local drafts.</p></div><div className="button-row"><button className="button secondary" onClick={exportProgress}><Download size={16}/> Export backup</button><button className="button secondary" onClick={()=>importRef.current?.click()}><Upload size={16}/> Import backup</button></div></section>
        </>}
        {active==='about'&&<About data={data} catalogCount={catalog.length}/>}
        {!['overview','library','problem','review','diagnostic','catalog','progress','about'].includes(active)&&<Empty title="That page is off the map." description="Return to the library to pick your next pattern."/>}
      </main>
      <footer><span>Pattern Atlas <span className="footer-dot">·</span> Algorithm study workspace</span><a href="#/about">Sources & curriculum notes <ArrowUpRight size={13}/></a></footer>
    </div>
    <input className="sr-only" type="file" aria-label="Progress backup file" accept="application/json,.json" ref={importRef} onChange={e=>void importProgress(e.target.files?.[0])}/>
    {toast&&<div className="toast" role="status"><Check size={17}/>{toast}<button className="icon-button" aria-label="Dismiss message" onClick={()=>setToast('')}><X size={14}/></button></div>}
  </div>;
}

function CloudHistoryPanel({state,message,onRetry,onConnect}:{state:CloudState;message:string;onRetry:()=>void;onConnect:(key:string)=>void}){
  const [key,setKey]=useState('');
  if(state==='local')return null;
  return <section className={`cloud-history-status ${state}`} aria-label="Cloud history status">
    <div><p className="eyebrow">AZURE HISTORY</p><strong>{state==='connected'?'Connected to your history':state==='loading'?'Loading your history':state==='sign-in'?'Connect to your history':'Cloud history needs attention'}</strong><p>{message||'Checking the private history database…'}</p></div>
    {state==='sign-in'&&<div className="cloud-history-actions"><a className="button primary" href={`/.auth/login/github?post_login_redirect_uri=${encodeURIComponent(location.origin+'/#/progress')}`}>Sign in with GitHub</a><form onSubmit={event=>{event.preventDefault();onConnect(key);setKey('');}}><label htmlFor="cloud-sync-key">Or enter your sync key</label><input id="cloud-sync-key" type="password" autoComplete="off" value={key} onChange={event=>setKey(event.target.value)} placeholder="Sync key" required/><button className="button secondary" type="submit">Connect</button></form></div>}
    {state==='error'&&<button className="button secondary" onClick={onRetry}>Retry cloud sync</button>}
  </section>;
}

type Shared={data:Curriculum;progress:Progress;setProgress:React.Dispatch<React.SetStateAction<Progress>>;setToast:(text:string)=>void};
function CategoryGrid({data,nodes,progress}:{data:Curriculum;nodes:CurriculumNode[];progress:Progress}){
  return <div className="category-grid">{nodes.map((node,i)=>{const ids=descendants(data.nodes,node.id);const count=data.nodes.filter(n=>ids.has(n.id)&&n.kind==='pattern').length;const problems=problemsFor(data,node.id);const learned=problems.filter(p=>isLearned(progress,p)).length;const Icon=icons[i%icons.length];return <a className={`category-card color-${i%4}`} href={`#${nodePath(node.id)}`} key={node.id}><div className="category-top"><span className="category-number">{String(i+1).padStart(2,'0')}</span><Tag kind={node.level}>{node.level}</Tag></div><h3>{node.title}</h3><p>{node.description}</p><div className="category-meta"><span>{count||1} {count===1?'pattern':'patterns'}</span><span>·</span><span>{libraryEntriesFor(data,node.id).length.toLocaleString()} problems</span><ArrowUpRight size={18}/></div><div className="category-progress"><i style={{width:`${problems.length?learned/problems.length*100:0}%`}}/></div></a>;})}</div>;
}
function Tree({data,parent=null,selected,depth=0}:{data:Curriculum;parent?:string|null;selected?:string;depth?:number}){
  const [expanded,setExpanded]=useState<Set<string>>(()=>new Set(selected?breadcrumbs(data.nodes,selected).map(n=>n.id):[]));
  return <div className="tree-branch">{data.nodes.filter(n=>n.parentId===parent).map(n=>{
    const hasChildren=data.nodes.some(c=>c.parentId===n.id);const open=expanded.has(n.id);
    return <div key={n.id}><div className={`tree-row ${selected===n.id?'selected':''}`} style={{paddingLeft:depth*12+6}}>{hasChildren?<button className="tree-toggle" aria-label={`${open?'Collapse':'Expand'} ${n.title}`} aria-expanded={open} onClick={()=>setExpanded(current=>{const next=new Set(current);next.has(n.id)?next.delete(n.id):next.add(n.id);return next;})}>{open?<ChevronDown size={14}/>:<ChevronRight size={14}/>}</button>:<span className="tree-dot"/>}<button onClick={()=>navigate(nodePath(n.id))}>{n.title}</button></div>{hasChildren&&open&&<Tree data={data} parent={n.id} selected={selected} depth={depth+1}/>}</div>;
  })}</div>;
}
function Library(props:Shared&{nodeId?:string}){
  const {data,progress,nodeId}=props;const [filter,setFilter]=useState('');const [level,setLevel]=useState('All levels');const [difficulty,setDifficulty]=useState('All difficulties');
  const node=data.nodes.find(n=>n.id===nodeId);const trail=node?breadcrumbs(data.nodes,node.id):[];
  const filtered=data.nodes.filter(n=>n.kind!=='category'&&`${n.title} ${n.description} ${breadcrumbs(data.nodes,n.id).map(n=>n.title).join(' ')}`.toLowerCase().includes(filter.toLowerCase())&&(level==='All levels'||n.level===level));
  if(!nodeId)return <><p className="eyebrow">THE COMPLETE MAP</p><h1>Pattern library</h1><p className="lead">Follow a topic down to the exact decision rule. Go as deep as you need.</p><div className="filterbar"><label className="search-field"><Search size={18}/><input aria-label="Search patterns" placeholder="Search patterns, techniques, or recognition cues" value={filter} onChange={e=>setFilter(e.target.value)}/></label><Select aria-label="Pattern level" value={level} onChange={e=>setLevel(e.target.value)}>{['All levels','Foundation','Intermediate','Advanced'].map(x=><option key={x}>{x}</option>)}</Select></div>{filter||level!=='All levels'?<><p className="result-count">{filtered.length} patterns found</p><div className="pattern-results">{filtered.map(n=><a key={n.id} href={`#${nodePath(n.id)}`}><div><span className="eyebrow">{breadcrumbs(data.nodes,n.id).slice(0,-1).map(n=>n.title).join(' / ')}</span><h3>{n.title}</h3><p>{n.description}</p></div><Tag kind={n.level}>{n.level}</Tag><ArrowRight size={18}/></a>)}</div>{!filtered.length&&<Empty title="No patterns found" description="Try a broader phrase or another learning level."/>}</>:<CategoryGrid data={data} nodes={data.nodes.filter(n=>!n.parentId)} progress={progress}/>}</>;
  if(!node)return <Empty title="Pattern not found" description="This link may belong to a newer curriculum. Return to the library."/>;
  const children=data.nodes.filter(n=>n.parentId===node.id);const problems=problemsFor(data,node.id).filter(p=>difficulty==='All difficulties'||p.difficulty===difficulty);
  return <><div className="breadcrumbs"><a href="#/library">Library</a>{trail.map(n=><React.Fragment key={n.id}><ChevronRight size={13}/><a href={`#${nodePath(n.id)}`}>{n.title}</a></React.Fragment>)}</div><div className="library-layout"><aside className="tree-panel"><div className="tree-heading"><Network size={17}/> THE PATTERN MAP</div><Tree data={data} selected={node.id}/></aside><article className="node-content"><div className="button-row"><Tag kind={node.level}>{node.level}</Tag><Tag>{node.priority} learning priority</Tag><span className="muted">{node.kind==='pattern'?'Authored pattern':node.kind==='collection'?'Practice collection':`${children.length} branches`}</span></div><h1>{node.title}</h1><p className="lead">{node.description}</p><a className="button secondary diagnostic-entry" href={`#/diagnostic?topic=${node.id}`}>Assess familiarity with this topic</a><section className="technique-panel"><span className="eyebrow"><Sparkles size={14}/> THE GENERAL APPROACH</span><p>{node.approach}</p>{node.pseudocode&&<div className="approach-pseudocode"><span className="eyebrow">PSEUDOCODE</span><pre tabIndex={0} aria-label="Technique pseudocode"><code>{node.pseudocode.code}</code></pre>{node.pseudocode.example&&<><span className="eyebrow">TRACE AN EXAMPLE</span><pre className="pseudocode-example" tabIndex={0} aria-label="Pseudocode example"><code>{node.pseudocode.example}</code></pre></>}</div>}<div className="tip"><CircleHelp size={17}/><div>{node.tips.map(t=><p key={t}>{t}</p>)}</div></div></section><div className="importance"><Target size={18}/><p><strong>Why learn this?</strong> {node.why}</p></div>{children.length>0&&<><div className="section-heading"><h2>Go one level deeper</h2></div><div className="child-grid">{children.map(c=><a href={`#${nodePath(c.id)}`} key={c.id}><div><span className="eyebrow">{c.kind==='pattern'?'PATTERN':c.kind==='collection'?'PRACTICE SET':'TECHNIQUE FAMILY'}</span><h3>{c.title}</h3><p>{c.description}</p></div><ChevronRight size={18}/></a>)}</div></>}
      <div className="section-heading wrap"><div><p className="eyebrow">PROBLEM INDEX</p><h2>Practice problems</h2></div><button className="button primary" onClick={()=>navigate(`/review?topic=${node.id}`)}><Layers3 size={16}/> Study this topic</button></div>
      <ProblemBrowser data={data} progress={progress} nodeId={node.id}/>
      <div className="source-links"><span>REFERENCE READING</span>{node.sourceUrls.map((url,i)=><a key={url} href={url} target="_blank" rel="noreferrer">{url.includes('leetcode.cn')?'EndlessCheng guide':url.includes('github')?'Solution source':'LeetCode reference'} <ArrowUpRight size={13}/></a>)}</div>
    </article></div></>;
}
function ProblemList({problems,progress,patternId,data}:{problems:Problem[];progress:Progress;patternId?:string;data:Curriculum}){
  if(!problems.length)return <Empty title="No problems in this view yet" description="Try another difficulty, or save a problem with the bookmark button."/>;
  return <div className="problem-list">{problems.map(p=><a href={`#${problemPath(p.id,patternId)}`} key={p.id}><span className={`status-circle ${isLearned(progress,p)?'done':''}`}>{isLearned(progress,p)?<Check size={14}/>:<Code2 size={14}/>}</span><div className="problem-name"><strong><span className="problem-number">{p.id}.</span> {p.title}</strong><small>{data.nodes.find(n=>n.id===(patternId??p.patternIds[0]))?.title}</small></div><Tag kind={p.difficulty}>{p.difficulty}</Tag>{progress.bookmarks.includes(p.id)&&<Bookmark size={15}/>}<ChevronRight size={17}/></a>)}</div>;
}
function Empty({title,description}:{title:string;description:string}){return <div className="empty-state"><BookOpen size={30}/><h3>{title}</h3><p>{description}</p><a href="#/library" className="text-link">Explore the library <ArrowRight size={15}/></a></div>;}

function ProblemStudy(props:Shared&{problem?:Problem;requestedPattern?:string;reviewMode?:boolean;onRate?:(rating:Rating)=>void}){
  const {data,progress,setProgress,setToast,problem,requestedPattern,reviewMode,onRate}=props;
  const [revealed,setRevealed]=useState(false);const [hint,setHint]=useState(false);const [solutionIndex,setSolutionIndex]=useState(()=>Math.max(0,problem?.solutions.findIndex(s=>s.patternId===requestedPattern)??0));
  const [rated,setRated]=useState<Rating>(); const [tab,setTab]=useState<'draft'|'solution'>('draft');
  if(!problem)return <Empty title="This problem is not a worked card yet" description="Find it in the full catalog to open the original problem on LeetCode."/>;
  const solution=problem.solutions[solutionIndex];const pattern=data.nodes.find(n=>n.id===solution.patternId)!;const key=cardKey(problem.id,solution.patternId);
  const saved=progress.bookmarks.includes(problem.id);const draft=progress.drafts[problem.id]??problem.starter;
  function grade(rating:Rating){if(!revealed||rated)return;setRated(rating);if(onRate)onRate(rating);else{setProgress(p=>rateCard(p,key,rating));setToast(rating==='again'?'Added to review in 10 minutes.':`Review scheduled. ${rating==='hard'?'Keep practicing the invariant.':'Nice work recalling the approach.'}`);}}
  return <div className="problem-study">
    {!reviewMode&&<div className="breadcrumbs"><a href="#/library">Library</a><ChevronRight size={13}/><a href={`#${nodePath(pattern.id)}`}>{pattern.title}</a><ChevronRight size={13}/><span>#{problem.id}</span></div>}
    <div className="problem-heading"><div><div className="button-row"><span className="eyebrow">PROBLEM {problem.id}</span><Tag kind={problem.difficulty}>{problem.difficulty}</Tag>{problem.premium&&<Tag>Premium on LeetCode</Tag>}</div><h1>{problem.title}</h1>{(!reviewMode||revealed)&&<a className="pattern-link" href={`#${nodePath(pattern.id)}`}><GitBranch size={15}/>{pattern.title}<ArrowUpRight size={13}/></a>}</div><div className="button-row"><button className={`button secondary ${saved?'bookmarked':''}`} aria-label={saved?'Unsave problem':'Save problem'} onClick={()=>setProgress(p=>({...p,bookmarks:saved?p.bookmarks.filter(id=>id!==problem.id):[...p.bookmarks,problem.id]}))}><Bookmark size={16} fill={saved?'currentColor':'none'}/><span>{saved?'Saved':'Save'}</span></button><a className="button secondary" href={problem.sourceUrl} target="_blank" rel="noreferrer">Run on LeetCode <ExternalLink size={15}/></a></div></div>
    <div className="study-layout"><section className="prompt-panel"><div className="panel-label"><BookOpen size={16}/> THE CHALLENGE <span>{problem.origin==='community'?'Community study card':'Original study summary'}</span></div><p className="problem-description">{problem.description}</p>{problem.examples.length>0?<h3>Example</h3>:<a className="button secondary statement-link" href={problem.sourceUrl} target="_blank" rel="noreferrer">Read official problem statement <ExternalLink size={15}/></a>}{problem.examples.map((ex,i)=><div className="example" key={i}><span>ARGUMENTS</span><code>{ex.input}</code><span>RESULT</span><code>{ex.output}</code>{ex.note&&<p>{ex.note}</p>}</div>)}<details className="constraints"><summary>Input notes <ChevronDown size={14}/></summary><p>{problem.constraints}</p>{problem.origin!=='community'&&<p>Authored study implementations use a <code>solve(...)</code> function. Linked-list and tree objects follow LeetCode node interfaces.</p>}</details><div className="recall-prompt"><Sparkles size={17}/><div><strong>Before you reveal</strong><p>What state do you need? What stays true after each step? What is the time complexity?</p></div></div><button className="hint-button" onClick={()=>setHint(!hint)}><CircleHelp size={16}/>{hint?'Hide recognition cue':'Need a small hint?'}<ChevronDown size={14}/></button>{hint&&<div className="hint-content">{pattern.description}<p>{pattern.tips[0]}</p></div>}</section>
      <section className="editor-panel"><div className="editor-tabs"><button className={tab==='draft'?'active':''} onClick={()=>setTab('draft')}><Code2 size={16}/> Your draft</button><button disabled={!revealed} className={tab==='solution'?'active':''} onClick={()=>setTab('solution')}><Eye size={16}/> Canonical solution</button><span>Python 3</span></div>
        {tab==='draft'?<><div className="editor-meta"><span><span className="green-dot"/> Saved on this device</span><span>Tab to indent · Esc then Tab to leave editor</span></div><CodeEditor aria-label="Solution draft" value={draft} height="390px" basicSetup={{autocompletion:false,foldGutter:false,highlightActiveLine:true}} onChange={value=>setProgress(p=>({...p,drafts:{...p.drafts,[problem.id]:value}}))}/><div className="editor-bottom"><span>Your space to reason. Execution lives on LeetCode.</span><button className="text-link" onClick={()=>{void navigator.clipboard.writeText(draft).then(()=>setToast('Draft copied.')).catch(()=>setToast('Copy unavailable. Select the text to copy it manually.'));}}>Copy draft</button></div></>:<div className="solution-content"><div className="solution-selector"><label>Solution approach<Select aria-label="Solution approach" disabled={reviewMode} value={solutionIndex} onChange={e=>{setSolutionIndex(Number(e.target.value));setRated(undefined);}}>{problem.solutions.map((s,i)=><option key={`${s.patternId}-${i}`} value={i}>{s.title}</option>)}</Select></label></div><p>{solution.approach}</p>{solution.attribution&&<div className="attribution">By <a href={solution.attribution.url} target="_blank" rel="noreferrer">{solution.attribution.author} <ArrowUpRight size={13}/></a><a href="/licenses/walkccc-MIT.txt" target="_blank" rel="noreferrer">MIT license</a><span>Source preserved · syntax checked · not judge-verified here</span></div>}<CodeEditor aria-label="Canonical solution code" value={solution.code} editable={false} basicSetup={{autocompletion:false,foldGutter:false}}/><div className="complexity"><span><Timer size={15}/><strong>Time</strong> {solution.time}</span><span><Layers3 size={15}/><strong>Space</strong> {solution.space}</span></div><div className="solution-pitfall"><strong>Watch for this</strong><p>{pattern.tips.join(' ')}</p></div></div>}
        {!revealed?<div className="reveal-panel"><div><strong>Ready to check your reasoning?</strong><p>Compare the invariant, not just the syntax.</p></div><button className="button primary" onClick={()=>{setRevealed(true);setTab('solution');}}><Eye size={17}/> Reveal solution</button></div>:<div className="rating-panel"><div><strong>{rated?'Review saved':'How well did you recall the approach?'}</strong><span>{rated?'Your next review is scheduled.':'Be honest. This decides when you see the card again.'}</span></div><div className="rating-buttons">{(['again','hard','good','easy'] as Rating[]).map((rating,i)=><button className={rated===rating?'chosen':''} disabled={!!rated} onClick={()=>grade(rating)} key={rating}><strong>{['Again','Hard','Good','Easy'][i]}</strong><small>{['10 minutes','1+ day','3+ days','7+ days'][i]}</small></button>)}</div></div>}
      </section></div>
  </div>;
}
function ReviewSession(props:Shared&{nodeId?:string}){
  const {data,progress,setProgress,nodeId}=props;
  const [queue,setQueue]=useState(()=>studyQueue(data,progress,{nodeId,limit:10}));const [index,setIndex]=useState(0);const [complete,setComplete]=useState(false);
  const [counts,setCounts]=useState<Record<string,number>>({});
  const node=data.nodes.find(n=>n.id===nodeId);const item=queue[index];
  function grade(rating:Rating){if(!item)return;setProgress(p=>rateCard(p,item.key,rating));setCounts(p=>({...p,[rating]:(p[rating]??0)+1}));if(index+1>=queue.length)setComplete(true);else setIndex(index+1);}
  if(!queue.length||complete)return <section className="session-complete"><span className="complete-icon"><CheckCheck size={34}/></span><p className="eyebrow">{complete?'SESSION COMPLETE':'ALL CAUGHT UP'}</p><h1>{complete?'A little practice goes a long way.':'You’re right on schedule.'}</h1><p>{complete?`You reviewed ${queue.length} cards. Your next reviews are scheduled based on your recall.`:'There are no new or due cards in this topic right now. Explore another topic, or revisit your saved problems.'}</p>{complete&&<div className="session-results">{Object.entries(counts).map(([rating,count])=><div key={rating}><strong>{count}</strong><span>{rating}</span></div>)}</div>}<div className="button-row"><button className="button primary" onClick={()=>{setQueue(studyQueue(data,progress,{nodeId,limit:10}));setIndex(0);setComplete(false);setCounts({});}}>Check next cards <ArrowRight size={16}/></button><a className="button secondary" href="#/library">Explore topics</a></div></section>;
  return <><div className="session-bar"><div><Layers3 size={20}/><div><strong>{node?.title??'Daily practice deck'}</strong><small>Recall first. Reveal when you’re ready.</small></div></div><div className="session-meter"><span>{index+1} / {queue.length}</span><div className="progress-track"><i style={{width:`${index/queue.length*100}%`}}/></div></div><a href="#/" className="icon-button" aria-label="Leave study session"><X size={18}/></a></div><ProblemStudy {...props} key={item.key} problem={item.problem} requestedPattern={item.patternId} reviewMode onRate={grade}/></>;
}
function Catalog(props:Shared&{catalog:CatalogProblem[];initialQuery:string}){
  return <><p className="eyebrow">PROBLEM INDEX</p><h1>All problems</h1><p className="lead">{props.catalog.length.toLocaleString()} indexed problems. {props.data.problems.length.toLocaleString()} with revealable Python solutions, including {props.data.stats?.authoredProblems??193} authored lessons.</p><ProblemBrowser key={props.initialQuery} data={props.data} progress={props.progress} initialQuery={props.initialQuery}/></>;
}
function About({data,catalogCount}:{data:Curriculum;catalogCount:number}){
  return <article className="about-page"><p className="eyebrow">A FIELD GUIDE, BUILT FOR RECALL</p><h1>Understand the why.<br/>Remember the how.</h1><p className="lead">Pattern Atlas turns algorithms into an organized collection of ideas you can recognize, practice, and revisit.</p><div className="technique-panel"><h2>The study loop</h2><p>Read the problem. Name the invariant. Write a draft. Reveal a solution and compare the reasoning. Rate your recall so the card returns when you need it.</p><p>Pattern level describes learning complexity; problem difficulty comes from LeetCode. “Core”, “Useful”, and “Specialist” describe editorial learning priority, not measured interview frequency.</p></div><h2>Built from a deeper map</h2><p>The curriculum was audited against the 12 EndlessCheng topic-guide outlines, labuladong’s full algorithm directory and learning plans, and LeetCode’s official topic tags. The core lessons are independently authored. Additional community implementations are imported from walkccc under the MIT license, with source attribution on every solution.</p><div className="source-cards"><a href="https://github.com/EndlessCheng/codeforces-go" target="_blank" rel="noreferrer"><h3>EndlessCheng</h3><p>Fine-grained patterns, from foundational techniques to advanced DP and graph structures.</p><ArrowUpRight/></a><a href="https://labuladong.online/en/algo/intro/quick-learning-plan/" target="_blank" rel="noreferrer"><h3>labuladong</h3><p>Frameworks, traversal thinking, and connections between structures and algorithms.</p><ArrowUpRight/></a><a href="https://leetcode.com/problemset/" target="_blank" rel="noreferrer"><h3>LeetCode</h3><p>Official problem titles, difficulty labels, topic tags, and a place to execute your solution.</p><ArrowUpRight/></a></div><h2>What is covered</h2><p>This edition includes {data.nodes.filter(n=>n.kind==='pattern').length} authored patterns, {data.problems.length.toLocaleString()} solution cards, and a dated catalog of {catalogCount.toLocaleString()} algorithm problem references. The hierarchy includes 313 problem-bearing source collections from EndlessCheng’s guides and broad official-topic collections. Source collections are practice groupings, not a guarantee that each community implementation follows one exact pattern.</p><p>The map focuses on algorithmic problem solving. SQL, shell, concurrency, and language-specific tracks are separate domains. Some rare contest techniques are recorded as extension topics in the repository’s coverage audit. This is an evolving curriculum, not a claim that all possible problems or patterns have been exhausted.</p><h2>Your private notebook</h2><p>No account is required. Drafts, bookmarks, and review history stay on your device. Export and import a backup from Your progress to move your work between installations. Automatic cross-device synchronization is not enabled.</p><p>Authored lessons include original summaries and study functions. Community cards preserve upstream Python implementations and public method signatures; their full statements and examples are read on LeetCode. The complete official statement and execution environment remain on LeetCode; premium problems may require a LeetCode subscription.</p><div className="source-links"><span>CURRICULUM UPDATED {data.updatedAt}</span><a href="https://github.com/ethanrimes/leetcode-on-the-go" target="_blank" rel="noreferrer">View source and coverage audit <ArrowUpRight size={14}/></a></div></article>;
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
