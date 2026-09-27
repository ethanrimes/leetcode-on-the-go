import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {emptyProgress, rateCard, schedule, parseProgress, descendants, studyQueue, cardKey, type Curriculum} from './index.js';
const data: Curriculum = JSON.parse(readFileSync(new URL('../../content/curriculum.json', import.meta.url), 'utf8'));
const now=new Date('2026-09-27T12:00:00Z');
test('again resets recall streak and returns in ten minutes',()=>{
  const result=schedule({repetitions:4,lapses:0,interval:21,due:now.toISOString(),lastReviewed:now.toISOString(),rating:'good'},'again',now);
  assert.equal(result.repetitions,0); assert.equal(result.lapses,1); assert.equal(result.due,'2026-09-27T12:10:00.000Z');
});
test('review queue excludes future cards and prioritizes due cards over new cards',()=>{
  let progress=emptyProgress(); const queue=studyQueue(data,progress,{now,limit:3});
  progress=rateCard(progress,queue[0].key,'good',now);
  progress=rateCard(progress,queue[1].key,'again',new Date(now.getTime()-3600000));
  const next=studyQueue(data,progress,{now,limit:3});
  assert.equal(next[0].key,queue[1].key); assert.ok(next.every(c=>c.key!==queue[0].key));
});
test('nested category queue stays within its descendants and preserves pattern variants',()=>{
  const ids=descendants(data.nodes,'dynamic-programming-knapsack');
  assert.ok(ids.size>6);
  assert.ok(studyQueue(data,emptyProgress(),{nodeId:'dynamic-programming-knapsack',limit:100}).every(c=>ids.has(c.patternId)));
  const p=data.problems.find(p=>p.id==='307')!;
  assert.notEqual(cardKey(p.id,p.patternIds[0]),cardKey(p.id,p.patternIds[1]));
});
test('backup roundtrip preserves drafts, bookmarks, and review history',()=>{
  const progress=rateCard({...emptyProgress(),drafts:{'1':'def solve():\n    return 42'},bookmarks:['1']},'1:complement','easy',now);
  assert.deepEqual(parseProgress(JSON.stringify(progress)),progress);
});
test('invalid backups fail rather than overwriting local progress',()=>{
  assert.throws(()=>parseProgress('{"version":2}'));
  assert.throws(()=>parseProgress(JSON.stringify({...emptyProgress(),cards:{bad:{due:'never'}}})));
  assert.throws(()=>parseProgress(JSON.stringify({...emptyProgress(),drafts:{one:3}})));
});
