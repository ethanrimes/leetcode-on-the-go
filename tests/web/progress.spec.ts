import {choose} from './select';
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
 await expect(page.locator('.analytics-dashboard .history-connect')).toContainText('3 submissions saved');
 await page.getByLabel('LeetCode history file').setInputFiles(file);
 await expect(page.locator('.submission-history tbody tr')).toHaveCount(3);
 await expect(page.getByLabel('Submission statistics')).toContainText('1accepted problems');
 await page.getByRole('button',{name:'Stacked bars',exact:true}).click();await expect(page.locator('.stacked-chart')).toBeVisible();
 await choose(page,'Chart metric','Practice freshness');await choose(page,'Freshness window','14 days');
 await page.getByRole('button',{name:'Treemap',exact:true}).click();
 await choose(page,'Map detail','All patterns & collections');
 await page.getByLabel('Find a tile').fill('Frequency signatures');
 await expect(page.locator('.treemap-tile')).toHaveCount(1);
 await page.locator('.treemap-tile').click();await expect(page.locator('.tile-detail')).toContainText('fresh');
 await page.getByLabel('Find a tile').fill('');await choose(page,'Map detail','Overview');
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
  if(url.pathname==='/api/problems/all/')return route.fulfill({json:{user_name:'demo-test',stat_status_pairs:[{status:'ac',stat:{question__title_slug:'two-sum'}},{status:'ac',stat:{question__title_slug:'group-anagrams'}},{status:null,stat:{question__title_slug:'valid-anagram'}}]}});
  if(url.pathname==='/api/submissions/') {const offset=Number(url.searchParams.get('offset'));return route.fulfill({json:{submissions_dump:offset===0?[{id:101,title_slug:'two-sum',title:'Two Sum',timestamp:1720000000,status_display:'Accepted',lang:'python3',code:'SECRET CODE'}]:[{id:102,title_slug:'valid-anagram',title:'Valid Anagram',timestamp:1710000000,status_display:'Wrong Answer',lang:'python3'}],has_next:offset===0,last_key:'cursor'}});}
  return route.fulfill({contentType:'text/html',body:'<html><body>Signed-in fixture</body></html>'});
 });
 await page.goto('https://leetcode.com/progress/');await page.addScriptTag({path:'apps/web/public/tools/leetcode-export.user.js'});
 const download=page.waitForEvent('download');await page.getByRole('button',{name:'Export all available history'}).click();
 const file=await download;const stream=await file.createReadStream();const chunks:Buffer[]=[];for await(const c of stream!)chunks.push(c);const result=JSON.parse(Buffer.concat(chunks).toString());
 expect(result.complete).toBe(true);expect(result.submissions).toHaveLength(2);expect(result.submissions[0]).not.toHaveProperty('code');expect(JSON.stringify(result)).not.toContain('SECRET');
 expect(result.completions.slugs).toEqual(['group-anagrams','two-sum']);
 await expect(page.getByRole('status')).toContainText('oldest record');
});
test('undated completions populate all-time coverage without filling diagnostic ratings or freshness',async({page})=>{
 await page.goto('/#/progress');
 const packet={...fixture,submissions:[],complete:false,completions:{observedAt:new Date().toISOString(),slugs:['two-sum','group-anagrams']}};
 await page.getByLabel('LeetCode history file').setInputFiles({name:'history.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(packet))});
 await expect(page.getByLabel('Submission statistics')).toContainText('2accepted problems');
 await expect(page.getByLabel('Imported LeetCode progress')).toContainText('2 completed problems');
 await page.getByRole('link',{name:'View coverage & freshness ↓'}).click();
 await expect(page).toHaveURL(/#\/progress$/);
 await expect(page.locator('.completion-note')).toContainText('2 completed problems');
 await expect(page.getByLabel('Diagnostic familiarity',{exact:true})).toContainText('0 of 200 solution sets assessed');
 await expect(page.locator('.submission-history tbody tr')).toHaveCount(0);
 await choose(page,'Submission period','Last 30 days');
 await expect(page.getByLabel('Submission statistics')).toContainText('0accepted problems');
 await page.reload();await expect(page.getByLabel('Submission statistics')).toContainText('2accepted problems');
});

test('styled menus fit the viewport, support keyboard selection, and expose readable map detail names',async({page},info)=>{
 await page.goto('/#/progress');
 const trigger=page.getByRole('combobox',{name:'Pattern level',exact:true});
 await trigger.scrollIntoViewIfNeeded();const control=await trigger.boundingBox();await trigger.click();
 const menu=page.getByRole('listbox');await expect(menu).toBeVisible();
 const box=await menu.boundingBox();
 expect(box!.width).toBeLessThanOrEqual(control!.width+2);expect(box!.height).toBeLessThanOrEqual(322);
 expect(box!.x).toBeGreaterThanOrEqual(0);expect(box!.x+box!.width).toBeLessThanOrEqual(page.viewportSize()!.width);
 await page.screenshot({path:`artifacts/styled-select-${info.project.name}.png`});
 await page.keyboard.press('Escape');await expect(menu).not.toBeVisible();await expect(trigger).toBeFocused();
 await trigger.press('ArrowDown');await page.keyboard.press('End');await page.keyboard.press('Enter');
 await expect(trigger).toHaveText('Advanced');
 await choose(page,'Map detail','All patterns & collections');
 await expect(page.getByRole('combobox',{name:'Map detail'})).toHaveText('All patterns & collections');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});

test('treemap reveals details on hover or keyboard focus and remains tappable',async({page},info)=>{
 await page.goto('/#/progress');await choose(page,'Map detail','All patterns & collections');
 await page.getByLabel('Find a tile').fill('Frequency signatures');
 const tile=page.locator('.treemap-tile');await expect(tile).toHaveCount(1);
 if(info.project.name==='desktop') {
  await tile.hover();const tooltip=page.getByRole('tooltip');await expect(tooltip).toBeVisible();
  await expect(tooltip).toContainText('Frequency signatures');await expect(tooltip).toContainText('Page entries');await expect(tooltip).toContainText('No dated practice');
  const box=await page.locator('.tile-tooltip').first().boundingBox();expect(box!.x).toBeGreaterThanOrEqual(0);expect(box!.x+box!.width).toBeLessThanOrEqual(page.viewportSize()!.width);
  await page.screenshot({path:'artifacts/treemap-tooltip.png'});
  await page.keyboard.press('Escape');await expect(tooltip).not.toBeVisible();
  await page.mouse.move(0,0);await tile.focus();await expect(tooltip).toBeVisible();
 }
 await tile.click();await expect(page.locator('.tile-detail')).toContainText('Frequency signatures');
 await expect(page.getByRole('link',{name:'Open study page',exact:true})).toBeVisible();
});

test('recommended tiles explain imported evidence, honor difficulty, and open the exact worked approach',async({page},info)=>{
 await page.goto('/#/progress');
 const history={...fixture,submissions:[{...fixture.submissions[0],id:'900010',slug:'group-anagrams',title:'Group Anagrams',status:'Wrong Answer'}]};
 await page.getByLabel('LeetCode history file').setInputFiles({name:'history.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(history))});
 await choose(page,'Problem difficulty','Medium');
 const panel=page.getByRole('region',{name:'Recommended practice'});
 await expect(panel).toContainText('Latest recorded submission: Wrong Answer');
 const links=panel.locator('.practice-problem');
 const hrefs=await links.evaluateAll(elements=>elements.map(e=>e.getAttribute('href')!));
 expect(hrefs.length).toBeGreaterThan(0);expect(new Set(hrefs.map(h=>h.split('?')[0])).size).toBe(hrefs.length);
 await expect(panel.locator('.practice-problem').first()).toContainText('Group Anagrams');
 await panel.scrollIntoViewIfNeeded();await page.screenshot({path:`artifacts/recommended-practice-${info.project.name}.png`});
 await links.first().click();await expect(page.locator('h1')).toHaveText('Group Anagrams');
 await expect(page).toHaveURL(/pattern=arrays-hashing-lookup-counting-frequency-signatures/);
});
