import {test,expect} from '@playwright/test';
const fixture={format:'pattern-atlas-leetcode',version:1,account:'demo-test',exportedAt:new Date().toISOString(),complete:true,submissions:[
 {id:'900001',slug:'two-sum',title:'Two Sum',timestamp:new Date().toISOString(),status:'Accepted',language:'python3'},
 {id:'900002',slug:'two-sum',title:'Two Sum',timestamp:new Date().toISOString(),status:'Wrong Answer',language:'python3'},
 {id:'900003',slug:'valid-anagram',title:'Valid Anagram',timestamp:'2025-01-01T00:00:00.000Z',status:'Wrong Answer',language:'python3'}
]};
test('history imports deduplicate and power both chart views and freshness',async({page},info)=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/#/progress');await expect(page.locator('h1')).toHaveText('Your progress');
 const file={name:'history.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(fixture))};
 await page.getByLabel('LeetCode history file').setInputFiles(file);
 await expect(page.locator('.history-connect')).toContainText('3 submissions saved');
 await page.getByLabel('LeetCode history file').setInputFiles(file);
 await expect(page.locator('.submission-history tbody tr')).toHaveCount(3);
 await expect(page.getByLabel('Submission statistics')).toContainText('1accepted problems');
 await page.getByRole('button',{name:'Stacked bars',exact:true}).click();await expect(page.locator('.stacked-chart')).toBeVisible();
 await page.getByLabel('Chart metric').selectOption('freshness');await page.getByLabel('Freshness window').selectOption('14');
 await page.getByRole('button',{name:'Treemap',exact:true}).click();
 await page.getByLabel('Aggregation',{exact:true}).selectOption('99');
 await page.getByLabel('Find a tile').fill('Frequency signatures');
 await expect(page.locator('.treemap-tile')).toHaveCount(1);
 await page.locator('.treemap-tile').click();await expect(page.locator('.tile-detail')).toContainText('fresh');
 await page.getByLabel('Find a tile').fill('');await page.getByLabel('Aggregation',{exact:true}).selectOption('1');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.screenshot({path:`artifacts/progress-${info.project.name}.png`,fullPage:true});
 await page.getByLabel('LeetCode history file').setInputFiles({...file,buffer:Buffer.from(JSON.stringify({...fixture,account:'other'}))});await expect(page.getByRole('alert')).toContainText('belongs to');
 expect(errors).toEqual([]);
});
test('entries increase only on navigation, persist on reload, and preserve old backups',async({page})=>{
 await page.goto('/#/problem/1');await expect(page.locator('h1')).toContainText('Two Sum');
 const count=()=>page.evaluate(()=>{const p=JSON.parse(localStorage.getItem('pattern-atlas.progress.v1')!);return Object.values(p.visits as Record<string,Record<string,{count:number}>>).reduce((n,d)=>n+(d['/problem/1']?.count??0),0);});
 await expect.poll(count).toBe(1);
 await page.getByRole('button',{name:'Reveal solution'}).click();expect(await count()).toBe(1);
 await page.goto('/#/progress');await expect(page.locator('h1')).toHaveText('Your progress');
 await page.goBack();await expect(page.locator('h1')).toContainText('Two Sum');await expect.poll(count).toBe(2);
 await page.reload();await expect.poll(count).toBe(3);
});
test('exporter paginates and downloads metadata without credentials or source code',async({page})=>{
 await page.route('https://leetcode.com/**',async route=>{
  const url=new URL(route.request().url());
  if(url.pathname==='/api/problems/all/')return route.fulfill({json:{user_name:'demo-test'}});
  if(url.pathname==='/api/submissions/') {const offset=Number(url.searchParams.get('offset'));return route.fulfill({json:{submissions_dump:offset===0?[{id:101,title_slug:'two-sum',title:'Two Sum',timestamp:1720000000,status_display:'Accepted',lang:'python3',code:'SECRET CODE'}]:[{id:102,title_slug:'valid-anagram',title:'Valid Anagram',timestamp:1710000000,status_display:'Wrong Answer',lang:'python3'}],has_next:offset===0,last_key:'cursor'}});}
  return route.fulfill({contentType:'text/html',body:'<html><body>Signed-in fixture</body></html>'});
 });
 await page.goto('https://leetcode.com/progress/');await page.addScriptTag({path:'apps/web/public/tools/leetcode-export.user.js'});
 const download=page.waitForEvent('download');await page.getByRole('button',{name:'Export all available history'}).click();
 const file=await download;const stream=await file.createReadStream();const chunks:Buffer[]=[];for await(const c of stream!)chunks.push(c);const result=JSON.parse(Buffer.concat(chunks).toString());
 expect(result.complete).toBe(true);expect(result.submissions).toHaveLength(2);expect(result.submissions[0]).not.toHaveProperty('code');expect(JSON.stringify(result)).not.toContain('SECRET');
 await expect(page.getByRole('status')).toContainText('oldest record');
});
