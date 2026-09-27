import {test,expect} from '@playwright/test';

test('browse a four-level taxonomy and reveal the right solution',async({page})=>{
  await page.goto('/#/library/dynamic-programming');
  await page.getByRole('link',{name:'Knapsack',exact:false}).filter({has:page.locator('h3')}).click();
  await page.getByRole('link',{name:'Zero-one choices',exact:false}).filter({has:page.locator('h3')}).click();
  await page.getByRole('link',{name:'Subset-sum feasibility',exact:false}).filter({has:page.locator('h3')}).click();
  await expect(page.locator('h1')).toHaveText('Subset-sum feasibility');
  await page.getByRole('link',{name:/416\. Partition Equal Subset Sum/}).click();
  await expect(page.getByRole('button',{name:'Canonical solution'})).toBeDisabled();
  await page.getByRole('button',{name:'Reveal solution'}).click();
  await expect(page.getByLabel('Canonical solution code')).toContainText('def solve(nums)');
  await expect(page.getByText('Descending sums preserve the previous layer.',{exact:false})).toBeVisible();
});
test('drafts, bookmarks, and recall survive reload without executing user code',async({page})=>{
  const errors:string[]=[]; page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/#/problem/1');
  const editor=page.getByLabel('Solution draft').locator('.cm-content');
  await editor.fill('def solve(nums, target):\n    return "my saved draft"');
  await page.getByRole('button',{name:'Save problem',exact:true}).click();
  await page.reload();
  await expect(editor).toContainText('my saved draft');
  await expect(page.getByRole('button',{name:'Unsave problem'})).toBeVisible();
  await page.getByRole('button',{name:'Reveal solution'}).click();
  await page.getByRole('button',{name:'Good 3+ days'}).click();
  await expect(page.getByText('Review saved',{exact:true})).toBeVisible();
  const progress=await page.evaluate(()=>JSON.parse(localStorage.getItem('pattern-atlas.progress.v1')!));
  expect(Object.values(progress.cards)).toHaveLength(1); expect(progress.bookmarks).toContain('1'); expect(errors).toEqual([]);
});
test('review session hides the pattern, advances cards, and records recall',async({page})=>{
  await page.goto('/#/review');
  await expect(page.getByText('1 / 10',{exact:true})).toBeVisible();
  await expect(page.locator('.pattern-link')).toHaveCount(0);
  await page.getByRole('button',{name:'Reveal solution'}).click();
  await page.getByRole('button',{name:'Again 10 minutes'}).click();
  await expect(page.getByText('2 / 10',{exact:true})).toBeVisible();
  await expect(page.getByRole('button',{name:'Reveal solution'})).toBeVisible();
});
test('catalog filters by official topic and exact number, with honest reference links',async({page})=>{
  await page.goto('/#/catalog?q=1');
  await expect(page.locator('.problem-list>a')).toHaveCount(1);
  await expect(page.locator('.problem-list')).toContainText('Two Sum');
  await page.getByLabel('Filter problems').fill('');
  await page.getByLabel('Official LeetCode topic').selectOption('Dynamic Programming');
  await page.getByLabel('Filter by difficulty').selectOption('Hard');
  await expect(page.locator('.problem-list>a').first()).toContainText('Hard');
  const external=page.locator('.problem-list>a[target="_blank"]').first();
  await expect(external).toHaveAttribute('href',/^https:\/\/leetcode.com\/problems\//);
});
test('backup import validates and merges without replacing an existing draft',async({page})=>{
  await page.goto('/#/problem/1');
  await page.getByLabel('Solution draft').locator('.cm-content').fill('local draft');
  await page.goto('/#/progress');
  const backup={version:1,cards:{},drafts:{'1':'incoming draft','2':'imported new draft'},bookmarks:['2'],activity:{}};
  await page.locator('input[type=file]').setInputFiles({name:'backup.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});
  await expect(page.getByRole('status')).toContainText('Backup merged');
  const progress=await page.evaluate(()=>JSON.parse(localStorage.getItem('pattern-atlas.progress.v1')!));
  expect(progress.drafts['1']).toBe('local draft');expect(progress.drafts['2']).toBe('imported new draft');
  await page.locator('input[type=file]').setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{"version":2}')});
  await expect(page.getByRole('status')).toContainText('not a Pattern Atlas');
});
test('layout stays within the viewport and navigation is accessible',async({page},testInfo)=>{
  await page.goto('/');await expect(page.locator('h1')).toContainText('Build intuition');
  if(testInfo.project.name==='mobile') {await page.getByRole('button',{name:'Open navigation'}).click();await page.getByRole('link',{name:'Pattern library',exact:true}).click();await expect(page.locator('h1')).toHaveText('Pattern library');}
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  await page.screenshot({path:`artifacts/web-${testInfo.project.name}.png`,fullPage:true});
});
