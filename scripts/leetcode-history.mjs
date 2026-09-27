#!/usr/bin/env node
/** Isolated LeetCode browser session. Never reads the user's Chrome/Comet profile. */
import {chromium} from '@playwright/test';
import {mkdir, chmod, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const args=process.argv.slice(2);
const option=(key,fallback)=>{const i=args.indexOf(key);return i>=0?args[i+1]:fallback;};
if(args.includes('--help')) {
 console.log('Usage: npm run history:login (one-time sign-in)\n       npm run history:export -- [--through YYYY-MM-DD] [--days 30] [--out path.json]\nHistory exports and the isolated browser session default to git-ignored .local/. No passwords, tokens, cookies, or solution code are exported.');
 process.exit(0);
}
const login=args.includes('--login');
const today=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,10);
const through=option('--through',today),days=Number(option('--days','0'));
if(!/^\d{4}-\d{2}-\d{2}$/.test(through)||through>today||!Number.isFinite(days)||days<0)throw new Error('Use a valid --through date no later than today and a nonnegative --days value.');
const until=new Date(through+'T23:59:59.999').getTime()/1000,cutoff=days?until-days*86400:0;
if(!Number.isFinite(until))throw new Error('Invalid date.');
const profile=path.join(root,'.local','leetcode-browser');
const output=path.resolve(option('--out',path.join(root,'.local',`leetcode-history-${through}.json`)));
await mkdir(profile,{recursive:true,mode:0o700});await chmod(profile,0o700);
const context=await chromium.launchPersistentContext(profile,{headless:!login,viewport:{width:1100,height:800},acceptDownloads:false});
const page=context.pages()[0]??await context.newPage();
const pause=ms=>new Promise(r=>setTimeout(r,ms));
let cancelled=false;process.on('SIGINT',()=>{cancelled=true;console.log('Stopping after the current request; collected records will be saved as partial.');});
async function readJSON(url) {
 for(let attempt=0;attempt<4;attempt++) {
  const result=await page.evaluate(async url=>{
   const response=await fetch(url,{credentials:'same-origin',cache:'no-store',signal:AbortSignal.timeout(30000)});
   if(!response.ok)return {status:response.status};
   try { return {status:response.status,data:await response.json()}; } catch { return {status:response.status}; }
  },url);
  if((result.status===429||result.status>=500)&&attempt<3){await pause(2000*2**attempt);continue;}
  if(!result.data)throw new Error(`LeetCode returned HTTP ${result.status} or a sign-in/challenge page. Run npm run history:login, then retry.`);
  return result.data;
 }
}
try {
 await page.goto('https://leetcode.com/progress/',{waitUntil:'domcontentloaded',timeout:60000});
 if(login) {
  console.log('Sign in to LeetCode in the separate browser window. This setup never changes Comet. Waiting up to 10 minutes…');
  const deadline=Date.now()+600000;let signedIn=false;
  while(Date.now()<deadline&&!cancelled){
   try{const p=await readJSON('/api/problems/all/');if(typeof p.user_name==='string'&&p.user_name.trim()){signedIn=true;break;}}catch{/* The user may still be signing in. */}
   await pause(5000);
  }
  if(!signedIn)throw new Error('Sign-in was not completed. Rerun npm run history:login when ready.');
  console.log('LeetCode session saved locally. Future exports can run headlessly.');
 } else {
  const profileData=await readJSON('/api/problems/all/');const account=profileData.user_name;
  if(typeof account!=='string'||!account.trim())throw new Error('No signed-in LeetCode session. Run npm run history:login once, then rerun this command.');
  const exportedAt=new Date().toISOString(),records=new Map(),seen=new Set();let complete=false,offset=0,lastkey='',failure='';
  try{
   for(let pageNumber=0;pageNumber<10000;pageNumber++) {
    if(cancelled)break;
    const params=new URLSearchParams({offset:String(offset),limit:'20',lastkey});const result=await readJSON(`/api/submissions/?${params}`);
    if(!Array.isArray(result.submissions_dump)||typeof result.has_next!=='boolean')throw new Error('The LeetCode response format changed. Export marked partial.');
    const before=seen.size;let crossed=false;
    for(const s of result.submissions_dump){
     const id=String(s.id),slug=s.title_slug,timestamp=Number(s.timestamp);
     if(!/^\d+$/.test(id)||typeof slug!=='string'||!Number.isFinite(timestamp)||timestamp<=0||typeof s.status_display!=='string')throw new Error('A submission record is invalid. Export marked partial.');
     seen.add(id);if(timestamp>until)continue;if(cutoff&&timestamp<cutoff){crossed=true;continue;}
     records.set(id,{id,slug,title:String(s.title??slug),timestamp:new Date(timestamp*1000).toISOString(),status:s.status_display,language:String(s.lang??'')});
    }
    if(pageNumber%10===0)console.log(`Read ${records.size} submissions…`);
    if(!result.has_next){complete=!cutoff;break;}if(crossed)break;
    if(seen.size===before)throw new Error('Pagination stopped advancing. Export marked partial.');
    offset+=result.submissions_dump.length;lastkey=String(result.last_key??'');
    if(pageNumber===9999)throw new Error('Page limit reached. Export marked partial.');
    await pause(700);
   }
  }catch(error){failure=error.message;}
  if(!records.size&&!complete)throw new Error(failure||'Stopped before any records were read.');
  await mkdir(path.dirname(output),{recursive:true,mode:0o700});
  await writeFile(output,JSON.stringify({format:'pattern-atlas-leetcode',version:1,account,exportedAt,complete,through,submissions:[...records.values()].sort((a,b)=>b.timestamp.localeCompare(a.timestamp))},null,2),{mode:0o600});
  console.log(`Saved ${records.size} submissions through ${through} to ${output}. ${complete?'Reached the oldest available record.':'Partial update; import preserves older history.'}`);
  if(failure){console.error(failure);process.exitCode=1;}
 }
}catch(error){console.error(error.message);process.exitCode=1;}
finally{await context.close();}
