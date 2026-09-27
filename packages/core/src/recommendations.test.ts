import {test} from 'node:test';
import assert from 'node:assert/strict';
import {practiceRecommendations,emptyProgress,type Curriculum,type CurriculumNode,type Problem,type Progress,type Submission} from './index';
const now=Date.parse('2026-09-27T12:00:00Z');
const node=(id:string,parentId:string|null,level:'Foundation'|'Advanced'='Foundation'):CurriculumNode=>({id,parentId,kind:parentId?'pattern':'category',title:id,level,priority:'Core',description:'',approach:'',tips:[],why:'',sourceUrls:[],references:[]});
const problem=(id:string,patterns:string[]):Problem=>({id,slug:`problem-${id}`,title:`Problem ${id}`,difficulty:'Medium',premium:false,description:'',examples:[],constraints:'',starter:'',sourceUrl:'',patternIds:patterns,solutions:patterns.map(patternId=>({patternId,title:'',language:'python',code:'',approach:'',time:'',space:''}))});
const data:Curriculum={version:1,updatedAt:'',language:'python',nodes:[node('a',null),node('a1','a'),node('a2','a'),node('b',null),node('b1','b'),node('c',null),node('c1','c','Advanced')],problems:[problem('1',['a1','a2']),problem('2',['a2']),problem('3',['b1']),problem('4',['c1'])]};
const submission=(id:string,slug:string,status='Accepted',timestamp='2026-08-01T00:00:00Z'):Submission=>({id,slug,title:slug,status,timestamp,language:'python3'});
const withHistory=(submissions:Submission[],slugs:string[]=[]):Progress=>({...emptyProgress(),leetcode:{account:'test',exportedAt:new Date(now).toISOString(),complete:false,submissions:Object.fromEntries(submissions.map(s=>[s.id,s])),completions:{observedAt:new Date(now).toISOString(),slugs}}});
test('recommendations prioritize due recall and unresolved latest attempts with distinct worked problems',()=>{
 const p=withHistory([submission('1','problem-1'),submission('2','problem-1','Wrong Answer','2026-09-26T00:00:00Z'),submission('3','problem-3')]);
 p.cards['4:c1']={rating:'good',repetitions:1,lapses:0,interval:3,lastReviewed:'2026-09-20T00:00:00Z',due:'2026-09-23T00:00:00Z'};
 const result=practiceRecommendations(data,p,{now});
 assert.equal(result[0].problem.id,'4');assert.equal(result[0].kind,'Review due');
 assert.equal(result[1].problem.id,'1');assert.equal(result[1].kind,'Retry a problem');
 assert.equal(new Set(result.map(r=>r.problem.id)).size,result.length);
 assert.ok(result.every(r=>r.problem.solutions.some(s=>s.patternId===r.node.id)));
 p.leetcode!.submissions['4']=submission('4','problem-1','Accepted','2026-09-27T01:00:00Z');
 assert.ok(!practiceRecommendations(data,p,{now}).some(r=>r.problem.id==='1'));
});
test('recommendations respect filters, diversify concepts and keep unknown dates unknown',()=>{
 const all=data.problems.map((p,i)=>submission(String(i+1),p.slug));
 const result=practiceRecommendations(data,withHistory(all),{now});
 assert.equal(new Set(result.slice(0,3).map(r=>r.rootId)).size,3);
 const unknown=practiceRecommendations(data,withHistory([],['problem-1']),{now,scope:'a1'});
 assert.equal(unknown.length,1);assert.equal(unknown[0].kind,'Check your recall');assert.match(unknown[0].reason,/unavailable/);
 assert.ok(practiceRecommendations(data,withHistory(all),{now,scope:'a'}).every(r=>r.rootId==='a'));
 assert.ok(practiceRecommendations(data,withHistory(all),{now,level:'Advanced'}).every(r=>r.node.level==='Advanced'));
 assert.deepEqual(practiceRecommendations(data,withHistory(all),{now,difficulty:'Easy'}),[]);
 const future=practiceRecommendations(data,withHistory([submission('1','problem-1','Wrong Answer','2026-10-01T00:00:00Z')]),{now,scope:'a1'});
 assert.equal(future[0].kind,'Build coverage');
});
test('diagnostic uncertainty is approach-specific and recent recall resolves old failed attempts',()=>{
 const p=withHistory([submission('1','problem-1','Wrong Answer')]);
 p.cards['1:a1']={rating:'good',repetitions:1,lapses:0,interval:3,lastReviewed:'2026-09-27T01:00:00Z',due:'2026-09-30T01:00:00Z'};
 assert.deepEqual(practiceRecommendations(data,p,{now,scope:'a1'}),[]);
 p.familiarity={'1:a1':{rating:'not-yet',assessedAt:new Date(now).toISOString()}};
 assert.equal(practiceRecommendations(data,p,{now,scope:'a1'})[0].kind,'Revisit the solution');
});
