import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {analytics,assessFamiliarity,diagnosticCards,diagnosticQueue,emptyProgress,familiarityByNode,familiaritySummary,mergeFamiliarity,mergeProgress,parseProgress,type Curriculum} from './index';
const data:Curriculum=JSON.parse(readFileSync(new URL('../../content/curriculum.json',import.meta.url),'utf8'));
const now=new Date('2026-09-27T12:00:00.000Z');
test('diagnostic samples breadth, exact approaches and usable local solutions',()=>{
 const cards=diagnosticCards(data),patternCount=data.nodes.filter(node=>node.kind==='pattern').length;assert.equal(cards.length,patternCount);assert.equal(new Set(cards.map(c=>c.key)).size,patternCount);
 const queue=diagnosticQueue(data,emptyProgress(),{mode:'unassessed',limit:12});
 const root=(id:string):string=>{const node=data.nodes.find(n=>n.id===id)!;return node.parentId?root(node.parentId):id;};
 assert.equal(new Set(queue.map(c=>root(c.node.id))).size,12);
 for(const card of cards){assert.equal(card.node.kind,'pattern');assert.ok(card.solutions.every(s=>s.patternId===card.node.id));}
 const scoped=diagnosticQueue(data,emptyProgress(),{nodeId:'dynamic-programming',difficulty:'Hard',limit:10000});assert.ok(scoped.length>0);assert.ok(scoped.every(c=>c.problem.difficulty==='Hard'&&root(c.node.id)==='dynamic-programming'));
 assert.ok(diagnosticCards(data,{includeCommunity:true}).length>2800);
});
test('flags update only familiarity, can be revised, and drive unassessed/uncertain queues',()=>{
 const card=diagnosticCards(data)[0];let p=assessFamiliarity(emptyProgress(),card.key,'probably',now);
 assert.equal(familiaritySummary([card],p).probably,1);assert.equal(Object.keys(p.cards).length,0);assert.deepEqual(p.activity,{});assert.equal(p.leetcode,undefined);
 assert.equal(analytics(data,p,{depth:99,scope:card.node.id,now:+now}).tiles[0].fresh,0);
 assert.ok(!diagnosticQueue(data,p,{mode:'unassessed',limit:10000}).some(c=>c.key===card.key));
 assert.deepEqual(diagnosticQueue(data,p,{mode:'uncertain'}).map(c=>c.key),[card.key]);
 p=assessFamiliarity(p,card.key,'definitely',new Date(+now+1000));assert.equal(familiaritySummary([card],p).definitely,1);assert.equal(diagnosticQueue(data,p,{mode:'uncertain'}).length,0);
 const leaves=familiarityByNode(data,p,{},true);assert.equal(leaves.filter(r=>r.assessed>0).length,1);assert.equal(leaves.find(r=>r.node.id===card.node.id)?.definitely,1);
});
test('community grouping ratings never leak into authored patterns for the same problem',()=>{
 const all=diagnosticCards(data,{includeCommunity:true});const community=all.find(c=>c.node.kind==='collection')!;
 const p=assessFamiliarity(emptyProgress(),community.key,'definitely',now);
 assert.equal(familiaritySummary(diagnosticCards(data),p).assessed,0);
 assert.equal(familiaritySummary(all,p).assessed,1);
 assert.ok(familiarityByNode(data,p,{includeCommunity:true},true).some(r=>r.node.id===community.node.id&&r.definitely===1));
});
test('diagnostic backups merge by date, reject bad records and preserve existing drafts',()=>{
 const key=diagnosticCards(data)[0].key;
 const local={...assessFamiliarity(emptyProgress(),key,'definitely',now),drafts:{'1':'keep'}};
 const incoming={...assessFamiliarity(emptyProgress(),key,'not-yet',new Date(+now+1000)),drafts:{'1':'replace'}};
 const merged=mergeProgress(local,parseProgress(JSON.stringify(incoming)));assert.equal(merged.familiarity?.[key].rating,'not-yet');assert.equal(merged.drafts['1'],'keep');
 assert.equal(mergeProgress(merged,local).familiarity?.[key].rating,'not-yet');
 const same=assessFamiliarity(emptyProgress(),key,'probably',now);
 assert.deepEqual(mergeFamiliarity(local.familiarity,same.familiarity),mergeFamiliarity(same.familiarity,local.familiarity));
 assert.equal(parseProgress(JSON.stringify(emptyProgress())).familiarity,undefined);
 assert.throws(()=>parseProgress(JSON.stringify({...local,familiarity:{[key]:{rating:'mastered',assessedAt:now.toISOString()}}})));
 assert.throws(()=>parseProgress(JSON.stringify({...local,familiarity:{[key]:{rating:'probably',assessedAt:'bad'}}})));
});
