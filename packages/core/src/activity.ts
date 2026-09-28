import {accepted, type LeetCodeHistory, type Submission} from './analytics';

/** LeetCode's userCalendar uses UTC date buckets, independent of the viewer's timezone. */
export interface ActivityCalendar {year:number; observedAt:string; days:Record<string,number>}
export type ActivityCalendars = Record<string,ActivityCalendar>;
export const utcDay=(date:Date)=>date.toISOString().slice(0,10);
const dayNumber=(day:string)=>Date.parse(`${day}T00:00:00Z`)/86400000;
export function validateCalendars(value:unknown):ActivityCalendars|undefined {
  if(value===undefined)return undefined;
  if(!value||typeof value!=='object'||Array.isArray(value)||Object.keys(value).length>200)throw new Error('Invalid activity calendars.');
  const result:ActivityCalendars={};
  for(const [key,item] of Object.entries(value)){
    const c=item as ActivityCalendar;
    if(!/^\d{4}$/.test(key)||!c||typeof c!=='object'||c.year!==Number(key)||typeof c.observedAt!=='string'||!/^\d{4}-\d{2}-\d{2}T/.test(c.observedAt)||!Number.isFinite(Date.parse(c.observedAt))||!c.days||typeof c.days!=='object'||Array.isArray(c.days)||Object.keys(c.days).length>366)throw new Error('Invalid activity calendar.');
    const days:Record<string,number>={};
    for(const [day,count]of Object.entries(c.days)){
      if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||!day.startsWith(key+'-')||!Number.isFinite(dayNumber(day))||utcDay(new Date(dayNumber(day)*86400000))!==day||day>c.observedAt.slice(0,10)||!Number.isSafeInteger(count)||count<=0||count>1_000_000)throw new Error('Invalid activity calendar day.');
      days[day]=count;
    }
    result[key]={year:c.year,observedAt:c.observedAt,days};
  }
  return result;
}
export function mergeCalendars(a:ActivityCalendars={},b:ActivityCalendars={}):ActivityCalendars {
  const result={...a};for(const [year,calendar]of Object.entries(b))if(!result[year]||Date.parse(calendar.observedAt)>=Date.parse(result[year].observedAt))result[year]=calendar;
  return result;
}
export function activitySummary(history:LeetCodeHistory|undefined,year:number,now=new Date()){
  const today=utcDay(now),snapshot=history?.calendars?.[String(year)];
  const byDay:Record<string,Submission[]>={},counts:Record<string,number>={};
  if(snapshot)for(const [day,count]of Object.entries(snapshot.days))if(day<=today)counts[day]=count;
  for(const submission of Object.values(history?.submissions??{})){
    const timestamp=new Date(submission.timestamp),day=utcDay(timestamp);
    if(timestamp>now||timestamp.getUTCFullYear()!==year)continue;
    (byDay[day]??=[]).push(submission);
    if(!snapshot||timestamp.getTime()>Date.parse(snapshot.observedAt))counts[day]=(counts[day]??0)+1;
  }
  const days=Object.keys(counts).filter(day=>counts[day]>0).sort();
  let longest=0,run=0,previous='';
  for(const day of days){run=previous&&dayNumber(day)-dayNumber(previous)===1?run+1:1;longest=Math.max(longest,run);previous=day;}
  let current=0;
  if(year===now.getUTCFullYear()){
    let cursor=counts[today]?dayNumber(today):dayNumber(today)-1;
    while(cursor>=dayNumber(`${year}-01-01`)&&counts[utcDay(new Date(cursor*86400000))]){current++;cursor--;}
  }
  const entries=Object.values(byDay).flat();
  return {byDay,counts,total:Object.values(counts).reduce((a,b)=>a+b,0),imported:entries.length,accepted:entries.filter(accepted).length,activeDays:days.length,longest,current,source:!!snapshot,observedAt:snapshot?.observedAt};
}
