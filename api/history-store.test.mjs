import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {test} from 'node:test';
import {authorize, mergeHistory, parseExport, readHistory, saveHistory, toExport} from './history-store.mjs';

const entry = (id, status='Accepted') => ({id,slug:`problem-${id}`,title:`Problem ${id}`,timestamp:'2026-09-27T10:00:00.000Z',status,language:'python3'});
const packet = (ids, observedAt='2026-09-27T11:00:00.000Z') => ({format:'pattern-atlas-leetcode',version:1,account:'Example',exportedAt:observedAt,complete:false,
  completions:{observedAt,slugs:ids.map(id=>`problem-${id}`)},submissions:ids.map(id=>entry(id))});
class MemoryTable {
  rows=new Map(); serial=0;
  key(partition,row){return `${partition}/${row}`;}
  async getEntity(partition,row){const value=this.rows.get(this.key(partition,row));if(!value)throw {statusCode:404};return {...value};}
  async createEntity(entity){const key=this.key(entity.partitionKey,entity.rowKey);if(this.rows.has(key))throw {statusCode:409};this.rows.set(key,{...entity,etag:String(++this.serial)});}
  async updateEntity(entity,_mode,options){const key=this.key(entity.partitionKey,entity.rowKey),old=this.rows.get(key);if(old?.etag!==options.etag)throw {statusCode:412};this.rows.set(key,{...entity,etag:String(++this.serial)});}
}

test('Azure table snapshot merges IDs and keeps the newest completion list', async()=>{
  const table=new MemoryTable();
  await saveHistory(table,parseExport(packet(['1','2'])));
  await saveHistory(table,parseExport(packet(['2','3'],'2026-09-27T12:00:00.000Z')));
  const {history}=await readHistory(table);
  assert.deepEqual(new Set(Object.keys(history.submissions)),new Set(['1','2','3']));
  assert.deepEqual(history.completions.slugs,['problem-2','problem-3']);
  assert.equal(toExport(history).submissions.length,3);
});

test('older partial uploads retain a newer completion snapshot',()=>{
  const newer=parseExport(packet(['2'],'2026-09-27T12:00:00.000Z'));
  const older=parseExport(packet(['1'],'2026-09-27T11:00:00.000Z'));
  const merged=mergeHistory(newer,older);
  assert.deepEqual(merged.completions.slugs,['problem-2']);
  assert.equal(Object.keys(merged.submissions).length,2);
});

test('uploading unchanged history does not create another table snapshot',async()=>{
  const table=new MemoryTable(),exported=parseExport(packet(['1','2']));
  await saveHistory(table,exported);
  const before=table.rows.size;
  await saveHistory(table,exported);
  assert.equal(table.rows.size,before);
});

test('only the configured GitHub owner or correct sync key can read history',()=>{
  const key='private-value',settings={tokenHash:createHash('sha256').update(key).digest('hex'),githubOwner:'ethanrimes'};
  assert.equal(authorize(new Headers({'x-pattern-atlas-sync-key':key}),settings),true);
  assert.equal(authorize(new Headers({'x-pattern-atlas-sync-key':'wrong'}),settings),false);
  const principal=user=>Buffer.from(JSON.stringify(user)).toString('base64');
  assert.equal(authorize(new Headers({'x-ms-client-principal':principal({identityProvider:'github',userDetails:'ethanrimes',userRoles:['anonymous','authenticated']})}),settings),true);
  assert.equal(authorize(new Headers({'x-ms-client-principal':principal({identityProvider:'github',userDetails:'someone-else',userRoles:['authenticated']})}),settings),false);
});

test('Azure preserves source calendars across old-client sync and selects the newest snapshot per year',async()=>{
  const table=new MemoryTable(),calendar={year:2025,observedAt:'2026-09-27T12:00:00.000Z',days:{'2025-05-01':12,'2025-05-02':8}};
  await saveHistory(table,parseExport({...packet(['1']),calendars:{'2025':calendar}}));
  await saveHistory(table,parseExport(packet(['2'],'2026-09-27T13:00:00.000Z')));
  let {history}=await readHistory(table);assert.deepEqual(history.calendars['2025'],calendar);
  const older={...calendar,observedAt:'2026-09-26T12:00:00.000Z',days:{'2025-05-01':1}};
  await saveHistory(table,parseExport({...packet(['3']),calendars:{'2025':older}}));
  ({history}=await readHistory(table));assert.deepEqual(toExport(history).calendars['2025'],calendar);
  assert.equal(Object.keys(history.submissions).length,3);
  for(const days of [{'2025-02-30':1},{'2024-05-01':1},{'2025-05-01':-1}])assert.throws(()=>parseExport({...packet([]),calendars:{'2025':{...calendar,days}}}));
});
