import {accepted,breadcrumbs,descendants,type AnalyticsFilter,type Curriculum,type CurriculumNode,type Problem,type Progress,type Submission} from './index';

export interface PracticeRecommendation {
 node:CurriculumNode; problem:Problem; rootId:string; topic:string;
 kind:string; reason:string; score:number;
}
/** Explainable practice priorities, based only on exact worked-solution mappings. */
export function practiceRecommendations(data:Curriculum,progress:Progress,filter:Pick<AnalyticsFilter,'scope'|'difficulty'|'level'|'freshDays'|'now'>):PracticeRecommendation[] {
 const now=filter.now??Date.now(),days=filter.freshDays??30;
 const branch=filter.scope?descendants(data.nodes,filter.scope):undefined;
 const latest=new Map<string,Submission>(),completed=new Set(progress.leetcode?.completions?.slugs??[]);
 for(const s of Object.values(progress.leetcode?.submissions??{})) {
  if(Date.parse(s.timestamp)>now)continue;
  if(accepted(s))completed.add(s.slug);
  const previous=latest.get(s.slug);
  if(!previous||s.timestamp>previous.timestamp||(s.timestamp===previous.timestamp&&BigInt(s.id)>BigInt(previous.id)))latest.set(s.slug,s);
 }
 const candidates:PracticeRecommendation[]=[];
 for(const node of data.nodes) {
  if(node.kind!=='pattern'||(branch&&!branch.has(node.id))||(filter.level&&node.level!==filter.level))continue;
  const root=breadcrumbs(data.nodes,node.id)[0]??node;
  for(const problem of data.problems) {
   if(!problem.solutions.some(s=>s.patternId===node.id)||(filter.difficulty&&problem.difficulty!==filter.difficulty))continue;
   const key=`${problem.id}:${node.id}`,review=progress.cards[key],rating=progress.familiarity?.[key]?.rating,submission=latest.get(problem.slug);
   const last=Math.max(submission?Date.parse(submission.timestamp):0,review?Date.parse(review.lastReviewed):0);
   const age=last?Math.max(0,Math.floor((now-last)/86400000)):undefined;
   let kind='',reason='',score=0;
   if(review&&Date.parse(review.due)<=now){kind='Review due';reason='Your saved recall review is due.';score=500;}
   else if(submission&&!accepted(submission)&&(!review||Date.parse(review.lastReviewed)<Date.parse(submission.timestamp))){kind='Retry a problem';reason=`Latest recorded submission: ${submission.status}. Revisit the approach.`;score=450;}
   else if(rating==='not-yet'||rating==='probably'){kind='Revisit the solution';reason=rating==='not-yet'?'You marked this approach “Did not get it.”':'You marked this approach “Probably got it.”';score=rating==='not-yet'?420:380;}
   else if(age!==undefined&&age>=days){kind='Refresh recall';reason=`Last practiced ${age} days ago. Try recalling the pattern first.`;score=250+Math.min(age,120)/4;}
   else if(age===undefined&&completed.has(problem.slug)){kind='Check your recall';reason='Completed on LeetCode; its practice date is unavailable.';score=160;}
   else if(age===undefined&&!completed.has(problem.slug)){kind='Build coverage';reason='No completion or practice recorded for this worked example.';score=100;}
   else continue;
   score+=node.priority==='Core'?20:node.priority==='Useful'?10:0;
   if(node.level==='Foundation')score+=3;
   candidates.push({node,problem,rootId:root.id,topic:root.title,kind,reason,score});
  }
 }
 const chosen:PracticeRecommendation[]=[],usedProblems=new Set<string>(),usedNodes=new Set<string>(),topics=new Map<string,number>();
 while(chosen.length<6) {
  const ranked=candidates.filter(c=>!usedProblems.has(c.problem.id)&&!usedNodes.has(c.node.id)).sort((a,b)=>
   (b.score-(topics.get(b.rootId)??0)*120)-(a.score-(topics.get(a.rootId)??0)*120)||a.node.id.localeCompare(b.node.id)||a.problem.id.localeCompare(b.problem.id,'en',{numeric:true}));
  const next=ranked[0];if(!next)break;
  chosen.push(next);usedProblems.add(next.problem.id);usedNodes.add(next.node.id);topics.set(next.rootId,(topics.get(next.rootId)??0)+1);
 }
 return chosen;
}
