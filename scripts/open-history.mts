#!/usr/bin/env node
// Keep this browser's study data private and separate from the LeetCode login.
import {chmod,mkdir,readFile,stat} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium,expect} from '@playwright/test';
import {parseSubmissionExport} from '../packages/core/src/index';

const args=process.argv.slice(2);
if(args.includes('--help')) {
 console.log('Usage: npm run history:open -- [--headless]\nImports .local/leetcode-history.json into a dedicated persistent Pattern Atlas browser. The visible browser stays open until you close it. Close it before running this command again. --headless imports and verifies without opening a window.');
 process.exit(0);
}
if(args.some(arg=>arg!=='--headless'))throw new Error('Unknown argument. Use --help.');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const directory=path.join(root,'.local'),profile=path.join(directory,'atlas-browser');
const file=path.join(directory,'leetcode-history.json');
if((await stat(file)).size>10_000_000)throw new Error('History exceeds the app’s 10 MB import limit.');
const history=parseSubmissionExport(await readFile(file,'utf8'));
await mkdir(profile,{recursive:true,mode:0o700});
await chmod(directory,0o700);await chmod(profile,0o700);
const headless=args.includes('--headless');
const context=await chromium.launchPersistentContext(profile,{headless,viewport:{width:1440,height:1000}});
try {
 const page=context.pages()[0]??await context.newPage();
 await page.goto('https://blue-sea-0c03ac51e.3.azurestaticapps.net/#/progress',{waitUntil:'networkidle',timeout:60000});
 await page.getByLabel('LeetCode history file',{exact:true}).setInputFiles(file);
 await expect(page.getByRole('status')).toContainText('Merged');
 const summary=page.getByLabel('Imported LeetCode progress',{exact:true});
 await expect(summary).toContainText(history.account,{timeout:15000});
 // Verify durable app storage, not merely the in-memory result of the import.
 const imported=await summary.innerText();
 await page.reload({waitUntil:'networkidle'});
 await expect(summary).toHaveText(imported,{useInnerText:true});
 console.log((await summary.innerText()).replace(/\n+/g,' · '));
 console.log('Saved in the private study-browser profile. Comet/Chrome profiles and iPhone storage are separate.');
 if(headless)await context.close();
 else {
  console.log('The study browser will stay open. Close it when finished; npm run history:open reopens it and merges your latest export.');
  process.once('SIGINT',()=>void context.close());
  process.once('SIGTERM',()=>void context.close());
  await new Promise<void>(resolve=>context.once('close',()=>resolve()));
 }
} catch(error) {
 await context.close();console.error(error instanceof Error?error.message:String(error));process.exitCode=1;
}
