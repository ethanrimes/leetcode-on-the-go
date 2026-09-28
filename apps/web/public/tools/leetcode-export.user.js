// ==UserScript==
// @name         Pattern Atlas · LeetCode history export
// @namespace    https://github.com/ethanrimes/leetcode-on-the-go
// @version      1.2.0
// @description  Download your submission metadata for Pattern Atlas. No code, cookies, or tokens are exported.
// @match        https://leetcode.com/progress/*
// @match        https://leetcode.com/submissions/*
// @grant        none
// ==/UserScript==
(() => {
  'use strict';
  if (location.origin !== 'https://leetcode.com') { alert('Run this script on https://leetcode.com/progress/ while signed in.'); return; }
  if (document.getElementById('pattern-atlas-export')) return;
  const box = document.createElement('section'); box.id = 'pattern-atlas-export';
  Object.assign(box.style, {position:'fixed',right:'20px',bottom:'20px',zIndex:'2147483647',width:'320px',padding:'20px',border:'1px solid #64748b',borderRadius:'8px',background:'#171b24',color:'#f8fafc',font:'14px/1.5 system-ui',boxShadow:'0 8px 30px #0005'});
  const title = document.createElement('strong'); title.textContent = 'Pattern Atlas · Submission export';
  const status = document.createElement('p'); status.setAttribute('role','status'); status.textContent = 'Reads your signed-in history. The JSON stays on your computer. Import it in either Pattern Atlas app.';
  const through = document.createElement('input'); through.type='date'; through.setAttribute('aria-label','Include submissions through'); through.value=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,10); through.max=through.value;
  const dateLabel=document.createElement('label'); dateLabel.textContent='Include submissions through '; dateLabel.append(through);
  const full = document.createElement('button'); full.textContent = 'Export all available history';
  const recent = document.createElement('button'); recent.textContent = 'Update · last 30 days';
  const stop = document.createElement('button'); stop.textContent = 'Close';
  for (const b of [full,recent,stop]) Object.assign(b.style,{display:'block',width:'100%',marginTop:'8px',padding:'9px',cursor:'pointer',borderRadius:'4px',border:'1px solid #64748b',background:'#315ed3',color:'white'});
  box.append(title,status,dateLabel,full,recent,stop); document.body.append(box);
  let running = false, cancelled = false;
  stop.onclick = () => { if(running) {cancelled = true; status.textContent = 'Stopping after the current request…';} else box.remove(); };
  const delay = ms => new Promise(resolve => setTimeout(resolve,ms));
  async function readJSON(url,body) {
    for(let attempt=0;attempt<4;attempt++) {
      const response = await fetch(url,{credentials:'same-origin',cache:'no-store',signal:AbortSignal.timeout(30000),...(body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{})});
      if((response.status===429||response.status>=500)&&attempt<3) {status.textContent='LeetCode requested a pause. Retrying shortly…';await delay(2000*2**attempt);continue;}
      if(!response.ok) throw new Error(`LeetCode returned HTTP ${response.status}. Sign in or try again later.`);
      try { return await response.json(); } catch { throw new Error('LeetCode did not return JSON. Check your sign-in and any browser challenge, then retry.'); }
    }
  }
  const calendarQuery='query userProfileCalendar($username: String!, $year: Int) { matchedUser(username: $username) { userCalendar(year: $year) { activeYears streak totalActiveDays submissionCalendar } } }';
  const submissionQuery='query submissionList($offset: Int!, $limit: Int!, $lastKey: String) { submissionList(offset: $offset, limit: $limit, lastKey: $lastKey) { lastKey hasNext submissions { id title titleSlug statusDisplay lang timestamp } } }';
  async function graphql(query,variables){const response=await readJSON('/graphql/',{query,variables});if(response.errors?.length)throw new Error(response.errors.map(e=>e.message).join('; '));return response.data;}
  async function run(days) {
    if(running)return;if(!/^\d{4}-\d{2}-\d{2}$/.test(through.value)||through.value>through.max){status.textContent='Choose a date no later than today.';return;}const throughDate=new Date(through.value+'T23:59:59.999');const until=throughDate.getTime()/1000;running=true;cancelled=false;full.disabled=true;recent.disabled=true;stop.textContent='Stop & save partial history';
    const records=new Map(),calendars={};let account='',complete=false,failure='',offset=0,lastkey='',completions,calendarWarning='';
    const cutoff=days?until-days*86400:0;const seen=new Set();
    const exportedAt=new Date().toISOString();
    try {
      status.textContent='Checking your signed-in account…';
      const profile=await readJSON('/api/problems/all/');account=profile.user_name;
      if(typeof account!=='string'||!account.trim())throw new Error('Sign in to LeetCode before exporting.');
      if(through.value===through.max&&Array.isArray(profile.stat_status_pairs))completions={observedAt:exportedAt,slugs:[...new Set(profile.stat_status_pairs.filter(p=>p.status==='ac').map(p=>p.stat.question__title_slug))].sort()};
      if(through.value===through.max)try{
        const year=new Date().getUTCFullYear(),current=(await graphql(calendarQuery,{username:account,year}))?.matchedUser?.userCalendar;
        if(!current||!Array.isArray(current.activeYears))throw new Error('Calendar response is missing.');
        for(const activeYear of [...new Set([...current.activeYears,year])]){
          const calendar=activeYear===year?current:(await graphql(calendarQuery,{username:account,year:activeYear}))?.matchedUser?.userCalendar;
          if(!calendar||typeof calendar.submissionCalendar!=='string')throw new Error('Invalid calendar response.');
          const observedAt=new Date().toISOString(),dates={};
          for(const [epoch,count]of Object.entries(JSON.parse(calendar.submissionCalendar))){
            const timestamp=Number(epoch)*1000;
            if(!Number.isFinite(timestamp)||!Number.isSafeInteger(count)||count<0)throw new Error('Invalid calendar day.');
            const day=new Date(timestamp).toISOString().slice(0,10);
            if(day.startsWith(String(activeYear))&&timestamp<=Date.parse(observedAt)&&count>0)dates[day]=count;
          }
          calendars[String(activeYear)]={year:activeYear,observedAt,days:dates};
        }
      }catch(error){calendarWarning=`Calendar update incomplete: ${error.message}`;}
      for(let page=0;page<10000;page++) {
        if(cancelled)break;
        const data=(await graphql(submissionQuery,{offset,limit:20,lastKey:lastkey})).submissionList;
        if(!Array.isArray(data?.submissions)||typeof data.hasNext!=='boolean')throw new Error('The LeetCode response format changed. No completeness claim was made.');
        const before=seen.size;let crossedCutoff=false;
        for(const s of data.submissions) {
          const id=String(s.id),slug=s.titleSlug,timestamp=Number(s.timestamp);
          if(!/^\d+$/.test(id)||typeof slug!=='string'||!Number.isFinite(timestamp)||timestamp<=0||typeof s.statusDisplay!=='string')throw new Error('A submission could not be read. Update the exporter before retrying.');
          seen.add(id);if(timestamp>until)continue;
          if(cutoff&&timestamp<cutoff) {crossedCutoff=true;continue;}
          records.set(id,{id,slug,title:String(s.title??slug),timestamp:new Date(timestamp*1000).toISOString(),status:s.statusDisplay,language:String(s.lang??'')});
        }
        status.textContent=`Read ${records.size.toLocaleString()} submissions from ${account}…`;
        if(!data.hasNext) {complete=!cutoff;break;}
        if(crossedCutoff)break;
        if(seen.size===before)throw new Error('Pagination stopped advancing. Saved only the records read so far.');
        offset+=data.submissions.length;lastkey=String(data.lastKey??'');
        if(page===9999)throw new Error('Safety page limit reached. This export is partial.');
        await delay(1500);
      }
    } catch(error) {failure=error instanceof Error?error.message:String(error);}
    finally {running=false;full.disabled=false;recent.disabled=false;stop.textContent='Close';}
    const detailDays={};for(const record of records.values()){const day=record.timestamp.slice(0,10);detailDays[day]=(detailDays[day]??0)+1;}
    const missingDays=Object.values(calendars).flatMap(calendar=>Object.entries(calendar.days)).filter(([day,count])=>(detailDays[day]??0)<count);
    if(complete&&missingDays.length){complete=false;failure=`Detailed history is short of the source calendar on ${missingDays.length} days. Saved as partial.`;}
    if(!account||(!records.size&&!complete&&!completions&&!Object.keys(calendars).length)) {status.textContent=failure||'Stopped before any submissions were read.';return;}
    const result={format:'pattern-atlas-leetcode',version:1,account,exportedAt,complete,through:through.value,completions,calendars,submissions:[...records.values()].sort((a,b)=>b.timestamp.localeCompare(a.timestamp))};
    const url=URL.createObjectURL(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}));
    const download=document.createElement('a');download.href=url;download.download=`leetcode-history-${exportedAt.slice(0,10)}${complete?'':'-partial'}.json`;download.textContent='Download JSON again';download.style.color='#a8c5ff';box.append(download);download.click();
    // Keep the object URL valid for the visible retry-download link.
    status.textContent=`Saved ${records.size.toLocaleString()} submissions and ${Object.keys(calendars).length} yearly calendars. ${complete?'Reached the oldest record available from LeetCode.':'Partial update: earlier records are preserved when you import.'} ${failure} ${calendarWarning}`;
  }
  full.onclick=()=>run(0);recent.onclick=()=>run(30);
})();
