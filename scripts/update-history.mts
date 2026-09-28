#!/usr/bin/env node
// Private cumulative export. Nothing is copied into the public web/iOS bundles.
import {spawnSync} from 'node:child_process';
import {mkdir,readFile,writeFile,copyFile,chmod,rename,access} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {mergeHistory,parseSubmissionExport} from '../packages/core/src/index';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const args=process.argv.slice(2);
const option=(key:string,fallback?:string)=>{const i=args.indexOf(key);if(i<0)return fallback;if(!args[i+1]||args[i+1].startsWith('--'))throw new Error(`Missing value for ${key}`);return args[i+1];};
if(args.includes('--help')) {
 console.log('Usage: npm run history:update -- [--days 30] [--through YYYY-MM-DD] [--from existing-export.json] [--simulator UDID]\nExports headlessly (30-day updates by default), merges into .local/leetcode-history.json, and optionally imports into an installed iOS Simulator app. Import that JSON in your regular web browser or send it to iPhone. Use --days 0 for all available submissions.');
 process.exit(0);
}
const directory=path.join(root,'.local'),output=path.join(directory,'leetcode-history.json');
await mkdir(directory,{recursive:true,mode:0o700});await chmod(directory,0o700);
let input=option('--from');let partial=false;
if(!input) {
 input=path.join(directory,`update-${Date.now()}.json`);
 const command=[path.join(root,'scripts/leetcode-history.mjs'),'--days',option('--days','30')!,'--out',input];
 const through=option('--through');if(through)command.push('--through',through);
 const run=spawnSync(process.execPath,command,{cwd:root,stdio:'inherit'});
 if(run.error)throw run.error;
 partial=run.status!==0;
 // A failed export may still contain valid partial history and the completion snapshot.
}
const incoming=parseSubmissionExport(await readFile(path.resolve(input),'utf8'));
let current;
try {current=parseSubmissionExport(await readFile(output,'utf8'));}catch(error){if((error as NodeJS.ErrnoException).code!=='ENOENT')throw error;}
const merged=mergeHistory(current,incoming);
if(current)await copyFile(output,path.join(directory,'leetcode-history.previous.json'));
const packet={...merged,format:'pattern-atlas-leetcode',version:1,submissions:Object.values(merged.submissions).sort((a,b)=>b.timestamp.localeCompare(a.timestamp))};
const temporary=output+'.tmp';
await writeFile(temporary,JSON.stringify(packet,null,2),{mode:0o600});await chmod(temporary,0o600);await rename(temporary,output);
console.log(`Ready: ${Object.keys(merged.submissions).length} dated submissions, ${merged.completions?.slugs.length??0} snapshot completions.\nImport ${output} in Pattern Atlas.`);
console.log(`${Object.keys(merged.calendars??{}).length} source calendars retained for activity reconciliation.`);
if(partial)console.log('LeetCode stopped the detailed export early. Available records were merged; history remains partial.');
const simulator=option('--simulator');
if(simulator) {
 if(!/^[A-Fa-f0-9-]{36}$/.test(simulator))throw new Error('Use an explicit Simulator UDID.');
 const result=spawnSync('xcrun',['simctl','get_app_container',simulator,'com.ethanrimes.patternatlas','data'],{encoding:'utf8'});
 if(result.status!==0)throw new Error('Pattern Atlas must already be installed on the selected simulator.');
 const documents=path.join(result.stdout.trim(),'Documents');await mkdir(documents,{recursive:true});
 const destination=path.join(documents,'LeetCode History.json');await copyFile(output,destination);await chmod(destination,0o600);
 try {const key=path.join(directory,'cloud-sync-key');await access(key);const staged=path.join(documents,'Cloud Sync Key.txt');await copyFile(key,staged);await chmod(staged,0o600);} catch(error) {if((error as NodeJS.ErrnoException).code!=='ENOENT')throw error;}
 const opened=spawnSync('xcrun',['simctl','openurl',simulator,'patternatlas://import-history'],{encoding:'utf8'});
 if(opened.status!==0)throw new Error('Could not open the import link. Install the latest native app, then retry.');
 console.log('Opened the native import. Verify its confirmation and account counts in Progress.');
}
// A configured private cloud store receives each cumulative update automatically.
try {
 await access(path.join(directory,'cloud-sync-key'));
 const uploaded=spawnSync(process.execPath,[path.join(root,'scripts/sync-cloud.mjs')],{cwd:root,stdio:'inherit'});
 if(uploaded.error)throw uploaded.error;
 if(uploaded.status!==0)throw new Error('The local history was saved, but the Azure update failed. Retry with npm run history:sync.');
} catch(error) {
 if((error as NodeJS.ErrnoException).code!=='ENOENT')throw error;
}
