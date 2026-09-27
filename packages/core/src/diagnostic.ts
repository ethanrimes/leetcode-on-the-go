import {cardKey, descendants, type Curriculum, type CurriculumNode, type Problem, type Progress, type Solution} from './index';

export type FamiliarityRating = 'definitely' | 'probably' | 'not-yet';
export const familiarityRatings: {value:FamiliarityRating;label:string;description:string}[] = [
  {value:'definitely',label:'Definitely got it',description:'I understand the approach and could explain it.'},
  {value:'probably',label:'Probably got it',description:'The idea makes sense, but I am unsure of some steps.'},
  {value:'not-yet',label:'Did not get it',description:'I need to study this approach again.'},
];
export interface FamiliarityAssessment {rating:FamiliarityRating;assessedAt:string}
export type Familiarity = Record<string,FamiliarityAssessment>;
export interface DiagnosticCard {key:string;problem:Problem;node:CurriculumNode;solutions:Solution[]}
export interface DiagnosticOptions {nodeId?:string;difficulty?:string;includeCommunity?:boolean;mode?:'unassessed'|'uncertain'|'all';limit?:number}
export function validateFamiliarity(value:unknown):Familiarity {
  if(!value||typeof value!=='object'||Array.isArray(value))throw new Error('Invalid diagnostic ratings.');
  const result:Familiarity={};
  for(const [key,item]of Object.entries(value)) {
    if(!/^[A-Za-z0-9_-]+:[A-Za-z0-9_-]+$/.test(key)||key.length>500||!item||typeof item!=='object'||Array.isArray(item)||!familiarityRatings.some(r=>r.value===item.rating)||typeof item.assessedAt!=='string'||!/^\d{4}-\d{2}-\d{2}T/.test(item.assessedAt)||!Number.isFinite(Date.parse(item.assessedAt)))throw new Error('A diagnostic rating is invalid. Nothing was imported.');
    result[key]={rating:item.rating,assessedAt:new Date(item.assessedAt).toISOString()};
  }
  return result;
}
const rank:Record<FamiliarityRating,number>={'not-yet':0,probably:1,definitely:2};
/** Newest assessment wins; equal timestamps conservatively choose the weaker rating. */
export function mergeFamiliarity(current:Familiarity={},incoming:Familiarity={}):Familiarity {
  const result={...current};
  for(const [key,item]of Object.entries(incoming)) {
    const old=result[key];
    if(!old||Date.parse(item.assessedAt)>Date.parse(old.assessedAt)||(Date.parse(item.assessedAt)===Date.parse(old.assessedAt)&&rank[item.rating]<rank[old.rating]))result[key]=item;
  }
  return result;
}
export function assessFamiliarity(progress:Progress,key:string,rating:FamiliarityRating,now=new Date()):Progress {
  return {...progress,familiarity:{...progress.familiarity,[key]:{rating,assessedAt:now.toISOString()}}};
}
/** A card groups only implementations for the same problem and explicitly mapped approach. */
export function diagnosticCards(data:Curriculum,options:DiagnosticOptions={}):DiagnosticCard[] {
  const nodes=new Map(data.nodes.map(n=>[n.id,n]));const scope=options.nodeId?descendants(data.nodes,options.nodeId):undefined;
  return data.problems.flatMap(problem=>{
    if(options.difficulty&&problem.difficulty!==options.difficulty)return [];
    return [...new Set(problem.solutions.map(s=>s.patternId))].flatMap(id=>{
      const node=nodes.get(id);
      if(!node||(!options.includeCommunity&&node.kind!=='pattern')||(scope&&!scope.has(id)))return [];
      return [{key:cardKey(problem.id,id),problem,node,solutions:problem.solutions.filter(s=>s.patternId===id)}];
    });
  });
}
/** Breadth-first sampling across roots, then patterns; unseen cards precede previous assessments. */
export function diagnosticQueue(data:Curriculum,progress:Progress,options:DiagnosticOptions={}):DiagnosticCard[] {
  const nodes=new Map(data.nodes.map(n=>[n.id,n]));
  const root=(node:CurriculumNode)=>{const seen=new Set<string>();while(node.parentId&&nodes.has(node.parentId)&&!seen.has(node.id)){seen.add(node.id);node=nodes.get(node.parentId)!;}return node.id;};
  const eligible=diagnosticCards(data,options).filter(c=>{
    const r=progress.familiarity?.[c.key];return options.mode==='uncertain'?!!r&&r.rating!=='definitely':options.mode==='unassessed'?!r:true;
  });
  const compare=(a:DiagnosticCard,b:DiagnosticCard)=>{
    const x=progress.familiarity?.[a.key],y=progress.familiarity?.[b.key];
    return Number(!!x)-Number(!!y)||(x&&y?rank[x.rating]-rank[y.rating]||Date.parse(x.assessedAt)-Date.parse(y.assessedAt):0)||({Easy:0,Medium:1,Hard:2}[a.problem.difficulty]-{Easy:0,Medium:1,Hard:2}[b.problem.difficulty])||a.problem.id.localeCompare(b.problem.id,'en',{numeric:true})||a.key.localeCompare(b.key);
  };
  const groups=new Map<string,Map<string,DiagnosticCard[]>>();
  for(const card of eligible){const id=root(card.node);if(!groups.has(id))groups.set(id,new Map());const patterns=groups.get(id)!;patterns.set(card.node.id,[...(patterns.get(card.node.id)??[]),card]);}
  const buckets=[...groups.values()].map(patterns=>{
    const queues=[...patterns.values()].map(cards=>cards.sort(compare)).sort((a,b)=>compare(a[0],b[0]));const result:DiagnosticCard[]=[];
    while(queues.some(q=>q.length))for(const q of queues){const card=q.shift();if(card)result.push(card);}return result;
  });
  const result:DiagnosticCard[]=[];const limit=options.limit??20;
  while(result.length<limit&&buckets.some(q=>q.length))for(const q of buckets){const card=q.shift();if(card)result.push(card);if(result.length>=limit)break;}
  return result;
}
export interface FamiliaritySummary {total:number;definitely:number;probably:number;notYet:number;unassessed:number;assessed:number;lastAssessed?:string}
export function familiaritySummary(cards:DiagnosticCard[],progress:Progress):FamiliaritySummary {
  const result:FamiliaritySummary={total:cards.length,definitely:0,probably:0,notYet:0,unassessed:0,assessed:0};
  for(const card of cards){const record=progress.familiarity?.[card.key];if(!record){result.unassessed++;continue;}result.assessed++;if(record.rating==='not-yet')result.notYet++;else result[record.rating]++;if(!result.lastAssessed||Date.parse(record.assessedAt)>Date.parse(result.lastAssessed))result.lastAssessed=record.assessedAt;}
  return result;
}
export function familiarityByNode(data:Curriculum,progress:Progress,options:DiagnosticOptions={},leaves=false) {
  const cards=diagnosticCards(data,options);const scope=options.nodeId?descendants(data.nodes,options.nodeId):undefined;
  let nodes=data.nodes.filter(n=>leaves?n.kind==='pattern'||(!!options.includeCommunity&&n.kind==='collection'):n.parentId===(options.nodeId??null));
  if(!leaves&&!nodes.length&&options.nodeId)nodes=data.nodes.filter(n=>n.id===options.nodeId);
  return nodes.filter(n=>!scope||scope.has(n.id)).map(node=>{const branch=descendants(data.nodes,node.id);return {node,...familiaritySummary(cards.filter(c=>branch.has(c.node.id)),progress)};}).filter(s=>s.total>0);
}
