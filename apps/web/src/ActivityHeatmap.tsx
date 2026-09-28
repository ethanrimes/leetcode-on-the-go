import {useMemo,useState} from 'react';
import {Select} from './Select';
import {accepted,type Curriculum,type Progress,type Submission} from '@pattern-atlas/core';

const localDay=(date:Date)=>`${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
const dayDate=(key:string)=>new Date(`${key}T12:00:00`);
const dayNumber=(key:string)=>Date.parse(`${key}T12:00:00Z`)/86400000;
function streaks(days:string[]){
  const ordered=[...new Set(days)].sort(),last=ordered.at(-1),today=localDay(new Date()),yesterday=localDay(new Date(Date.now()-86400000));
  let longest=0,run=0,current=0,previous='';
  for(const day of ordered){run=previous&&dayNumber(day)-dayNumber(previous)===1?run+1:1;longest=Math.max(longest,run);previous=day;}
  if(last===today||last===yesterday){for(let i=ordered.length-1;i>=0;i--){if(i<ordered.length-1&&dayNumber(ordered[i+1])-dayNumber(ordered[i])!==1)break;current++;}}
  return {longest,current};
}
export function ActivityHeatmap({data,progress}:{data:Curriculum;progress:Progress}){
  const submissions=useMemo(()=>Object.values(progress.leetcode?.submissions??{}),[progress.leetcode]);
  const byDay=useMemo(()=>{const map=new Map<string,Submission[]>();for(const submission of submissions){const key=localDay(new Date(submission.timestamp));map.set(key,[...(map.get(key)??[]),submission]);}return map;},[submissions]);
  const years=useMemo(()=>[...new Set([new Date().getFullYear(),...byDay.keys()].map(value=>typeof value==='number'?value:Number(value.slice(0,4))))].sort((a,b)=>b-a),[byDay]);
  const [year,setYear]=useState(new Date().getFullYear()),[selected,setSelected]=useState('');
  const start=new Date(year,0,1),end=new Date(year+1,0,1),gridStart=new Date(start);gridStart.setDate(start.getDate()-(start.getDay()+6)%7);
  const cells:Date[]=[];for(let day=new Date(gridStart);day<end||day.getDay()!==1;day.setDate(day.getDate()+1))cells.push(new Date(day));
  const active=[...byDay.keys()].filter(key=>key.startsWith(String(year))),total=active.reduce((sum,key)=>sum+(byDay.get(key)?.length??0),0),acceptedCount=active.reduce((sum,key)=>sum+(byDay.get(key)?.filter(accepted).length??0),0);
  const streak=streaks([...byDay.keys()]),dayEntries=[...(byDay.get(selected)??[])].sort((a,b)=>b.timestamp.localeCompare(a.timestamp));
  const worked=new Set(data.problems.map(problem=>problem.slug));
  return <section className="activity-panel" aria-label="LeetCode activity">
    <div className="section-heading"><div><p className="eyebrow">DATED PRACTICE</p><h2>Your activity</h2></div><label>Year<Select aria-label="Activity year" value={year} onChange={event=>{setYear(Number(event.target.value));setSelected('');}}>{years.map(value=><option key={value} value={value}>{value}</option>)}</Select></label></div>
    <div className="activity-stats"><div><strong>{total}</strong><span>submissions in {year}</span></div><div><strong>{acceptedCount}</strong><span>accepted submissions</span></div><div><strong>{active.length}</strong><span>active days</span></div><div><strong>{streak.current}</strong><span>current streak</span></div><div><strong>{streak.longest}</strong><span>longest streak</span></div></div>
    <div className="activity-scroll"><div className="activity-calendar"><div className="activity-months">{cells.filter(day=>day.getDate()<=7&&day.getDay()===1).map(day=><span key={localDay(day)} style={{gridColumn:Math.floor((day.getTime()-gridStart.getTime())/604800000)+1}}>{day.toLocaleDateString('en',{month:'short'})}</span>)}</div><div className="activity-grid">{cells.map(day=>{const key=localDay(day),count=byDay.get(key)?.length??0,inYear=day.getFullYear()===year,level=count===0?0:count===1?1:count<=3?2:count<=7?3:4;return <button type="button" key={key} className={`activity-day activity-level-${level} ${selected===key?'selected':''} ${!inYear?'outside-year':''}`} disabled={!inYear} title={`${day.toDateString()}: ${count} submissions`} aria-label={`${day.toDateString()}: ${count} submissions, ${byDay.get(key)?.filter(accepted).length??0} accepted`} aria-pressed={selected===key} onClick={()=>setSelected(key)} />;})}</div></div></div>
    <div className="activity-footer"><span>Each square is a day with dated LeetCode submissions. Select one to inspect it.</span><span>Less <i className="activity-level-0"/><i className="activity-level-1"/><i className="activity-level-2"/><i className="activity-level-3"/><i className="activity-level-4"/> More</span></div>
    {selected&&<div className="activity-detail"><div><h3>{dayDate(selected).toLocaleDateString('en',{weekday:'long',month:'long',day:'numeric',year:'numeric'})}</h3><p>{dayEntries.length} submissions · {dayEntries.filter(accepted).length} accepted</p></div>{dayEntries.length?<ul>{dayEntries.map(submission=><li key={submission.id}><span className={accepted(submission)?'activity-accepted':'activity-other'}>{submission.status}</span><a href={worked.has(submission.slug)?`#/problem/${data.problems.find(p=>p.slug===submission.slug)?.id}`:`https://leetcode.com/problems/${submission.slug}/`} target={worked.has(submission.slug)?undefined:'_blank'} rel="noreferrer">{submission.title}</a><small>{new Date(submission.timestamp).toLocaleTimeString([],{hour:'numeric',minute:'2-digit'})} · {submission.language}</small><a href={`https://leetcode.com/submissions/detail/${submission.id}/`} target="_blank" rel="noreferrer">View submission ↗</a></li>)}</ul>:<p>No recorded submissions on this day.</p>}</div>}
    <p className="chart-note">Completion snapshots without submission dates are included in coverage, not activity or streaks. The importer may have only partial historical submission detail.</p>
  </section>;
}
