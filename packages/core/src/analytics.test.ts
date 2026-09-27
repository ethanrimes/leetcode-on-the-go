import {test} from 'node:test';
import assert from 'node:assert/strict';
import {analytics,emptyProgress,recordVisit,pageVisits,mergeVisits,parseProgress,parseSubmissionExport,mergeHistory,mergeProgress,treemap,type Curriculum,type SubmissionExport,type CurriculumNode} from './index';
const now=new Date('2026-09-27T12:00:00.000Z');
const packet:SubmissionExport={format:'pattern-atlas-leetcode',version:1,account:'demo',exportedAt:now.toISOString(),complete:true,submissions:[
  {id:'1',slug:'two-sum',title:'Two Sum',timestamp:'2026-08-01T00:00:00.000Z',status:'Accepted',language:'python3'},
  {id:'2',slug:'two-sum',title:'Two Sum',timestamp:'2026-09-26T00:00:00.000Z',status:'Wrong Answer',language:'python3'},
  {id:'3',slug:'valid-anagram',title:'Valid Anagram',timestamp:'2026-07-01T00:00:00.000Z',status:'Wrong Answer',language:'python3'}
]};
const history=()=>parseSubmissionExport(JSON.stringify(packet));
const node=(id:string,parentId:string|null,problemIds:string[]=[]):CurriculumNode=>({id,parentId,problemIds,title:id,kind:parentId?'pattern':'category',level:'Foundation',priority:'Core',description:'',approach:'',tips:[],why:'',sourceUrls:[],references:[]});
const data:Curriculum={version:1,updatedAt:'',language:'python',problems:[],nodes:[node('root',null),node('one','root',['1','242']),node('two','root',['1']),node('other',null,['49'])],catalog:[{id:'1',title:'Two Sum',slug:'two-sum',difficulty:'Easy',premium:false},{id:'242',title:'Valid Anagram',slug:'valid-anagram',difficulty:'Easy',premium:false},{id:'49',title:'Group Anagrams',slug:'group-anagrams',difficulty:'Medium',premium:false}]};
test('submission updates merge once, preserve accepted evidence, reject mixed accounts',()=>{
 const first=history();const updated=mergeHistory(first,first);assert.equal(Object.keys(updated.submissions).length,3);
 assert.throws(()=>mergeHistory(first,{...first,account:'someone-else'}),/belongs/);
 const stats=analytics(data,{...emptyProgress(),leetcode:updated},{depth:1,now:+now});
 assert.equal(stats.solved,1);assert.equal(stats.attempted,1);assert.equal(stats.tiles.find(s=>s.node.id==='root')?.total,2);
 assert.equal(stats.tiles.find(s=>s.node.id==='root')?.solved,1); // overlap is deduplicated at the parent
 const leaves=analytics(data,{...emptyProgress(),leetcode:updated},{depth:99,scope:'root',now:+now});
 assert.equal(leaves.tiles.reduce((sum,s)=>sum+s.solved,0),2);assert.equal(leaves.solved,1);
 assert.deepEqual(analytics(data,{...emptyProgress(),leetcode:updated},{depth:1,difficulty:'Medium',now:+now}).submissions,[]);
});
test('freshness uses practice, not page visits, and highlights stale work',()=>{
 let p=recordVisit({...emptyProgress(),leetcode:history()},'web','/library/one',now);
 const result=analytics(data,p,{depth:99,scope:'root',freshDays:30,now:+now});
 const one=result.tiles.find(s=>s.node.id==='one')!;
 assert.equal(one.fresh,1);assert.equal(one.practiced,2);assert.equal(one.visits,1);assert.equal(result.focus[0].node.id,'one');
 const recent=analytics(data,p,{depth:99,scope:'root',since:+now-30*86400000,now:+now});
 assert.equal(recent.solved,0);assert.equal(recent.attempted,1);assert.equal(recent.tiles.find(s=>s.node.id==='one')?.fresh,1);
 p={...p,cards:{'242:one':{repetitions:1,lapses:0,interval:1,rating:'good',lastReviewed:now.toISOString(),due:new Date(+now+86400000).toISOString()}}};
 assert.equal(analytics(data,p,{depth:99,scope:'root',now:+now}).tiles.find(s=>s.node.id==='one')?.fresh,2);
});
test('visit counters merge idempotently across devices and old backups still load',()=>{
 const old=parseProgress('{"version":1,"cards":{},"drafts":{"1":"local"},"bookmarks":[],"activity":{}}');
 const web=recordVisit(recordVisit(old,'web','/library/one',now),'web','/library/one?sort=number',now);
 const ios=recordVisit(old,'ios','/library/one',now);
 const merged=mergeVisits(web.visits,ios.visits);assert.equal(pageVisits(merged)['/library/one'].count,3);
 assert.deepEqual(mergeVisits(merged,merged),merged);
 const roundtrip=parseProgress(JSON.stringify({...web,leetcode:history()}));assert.equal(Object.keys(roundtrip.leetcode!.submissions).length,3);
 const combined=mergeProgress(roundtrip,{...ios,drafts:{'1':'incoming'}});assert.equal(combined.drafts['1'],'local');assert.equal(pageVisits(combined.visits)['/library/one'].count,3);
});
test('invalid analytics imports fail atomically and unrecognized problems remain in history',()=>{
 assert.throws(()=>parseSubmissionExport(JSON.stringify({...packet,submissions:[{...packet.submissions[0],id:'../x'}]})));
 assert.throws(()=>parseSubmissionExport(JSON.stringify({...packet,submissions:[{...packet.submissions[0],timestamp:'bad'}]})));
 assert.throws(()=>parseProgress(JSON.stringify({...emptyProgress(),visits:{web:{'/':{count:-1,lastVisited:now.toISOString()}}}})));
 const unmapped=history();unmapped.submissions['9']={...packet.submissions[0],id:'9',slug:'future-problem'};
 const stats=analytics(data,{...emptyProgress(),leetcode:unmapped},{depth:1,now:+now});assert.equal(stats.unmapped,1);assert.equal(stats.submissions.length,4);assert.equal(stats.solved,1);
});
test('treemap covers the canvas with proportional, non-overlapping rectangles',()=>{
 const weights=[100,50,40,10,1,0],rects=treemap(weights,800,500);assert.equal(rects.length,5);
 for(const r of rects){assert.ok(Math.abs(r.width*r.height/(800*500)-weights[r.index]/201)<1e-10);assert.ok(r.x>=0&&r.y>=0&&r.x+r.width<=800.00001&&r.y+r.height<=500.00001);}
 for(let i=0;i<rects.length;i++)for(let j=i+1;j<rects.length;j++){const a=rects[i],b=rects[j];assert.ok(Math.min(a.x+a.width,b.x+b.width)-Math.max(a.x,b.x)<1e-9||Math.min(a.y+a.height,b.y+b.height)-Math.max(a.y,b.y)<1e-9);}
 assert.deepEqual(treemap([]),[]);
});
test('a due recall is attributed to its exact pattern, not every pattern sharing a problem',()=>{
 const progress={...emptyProgress(),cards:{'1:one':{repetitions:1,lapses:0,interval:1,rating:'good' as const,lastReviewed:'2026-01-01T00:00:00.000Z',due:'2026-01-02T00:00:00.000Z'}}};
 const result=analytics(data,progress,{depth:99,scope:'root',now:+now});
 assert.equal(result.tiles.find(s=>s.node.id==='one')?.due,1);assert.equal(result.tiles.find(s=>s.node.id==='two')?.due,0);
});
