import {validateHistory, validateVisits, type LeetCodeHistory, type Visits} from './analytics';
export * from './analytics';
export type Level = 'Foundation' | 'Intermediate' | 'Advanced';
export type Difficulty = 'Easy' | 'Medium' | 'Hard';
export type Rating = 'again' | 'hard' | 'good' | 'easy';
export interface ReferenceSection { title: string; url: string; problemIds: string[] }
export interface CurriculumNode {
  id: string; parentId: string | null; title: string; kind: 'category' | 'pattern' | 'collection';
  problemIds?: string[]; sourceTitle?: string;
  pseudocode?: {code: string; example?: string};
  level: Level; priority: 'Core' | 'Useful' | 'Specialist'; description: string;
  approach: string; tips: string[]; why: string; sourceUrls: string[]; references: ReferenceSection[];
}
export interface CatalogProblem {
  id: string; title: string; slug: string; difficulty: Difficulty; premium: boolean;
  tags?: {name: string; slug: string}[];
}
export interface Solution {
  attribution?: {author: string; license: string; url: string; commit: string; sha256: string};
  patternId: string; title: string; language: string; approach: string; code: string; time: string; space: string;
}
export interface Problem extends CatalogProblem {
  origin?: 'authored' | 'community'; collectionIds?: string[];
  description: string; examples: {input: string; output: string; note: string}[]; constraints: string;
  patternIds: string[]; solutions: Solution[]; starter: string; sourceUrl: string;
}
export interface Curriculum {catalog?: CatalogProblem[]; stats?: {authoredProblems:number;communityProblems:number;sourceCollections:number}; version: number; updatedAt: string; language: string; nodes: CurriculumNode[]; problems: Problem[]}
export interface Review {
  repetitions: number; lapses: number; interval: number; due: string; lastReviewed: string; rating: Rating;
}
export interface Progress {
  leetcode?: LeetCodeHistory; visits?: Visits;
  version: 1; cards: Record<string, Review>; drafts: Record<string, string>; bookmarks: string[]; activity: Record<string, number>;
}
export const emptyProgress = (): Progress => ({version: 1, cards: {}, drafts: {}, bookmarks: [], activity: {}});
export const cardKey = (problemId: string, patternId: string) => `${problemId}:${patternId}`;
export const dayKey = (date: Date) => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;

/** Small, predictable interval scheduler; not presented as FSRS or a validated memory model. */
export function schedule(previous: Review | undefined, rating: Rating, now = new Date()): Review {
  const interval = rating === 'again' ? 10 / 1440
    : rating === 'hard' ? Math.max(1, Math.round((previous?.interval ?? 0) * 1.2))
    : rating === 'good' ? Math.max(3, Math.round((previous?.interval ?? 0) * 2.3))
    : Math.max(7, Math.round((previous?.interval ?? 0) * 3.2));
  return {
    repetitions: rating === 'again' ? 0 : (previous?.repetitions ?? 0) + 1,
    lapses: (previous?.lapses ?? 0) + (rating === 'again' ? 1 : 0), interval,
    due: new Date(now.getTime() + interval * 86_400_000).toISOString(), lastReviewed: now.toISOString(), rating,
  };
}
export function rateCard(progress: Progress, key: string, rating: Rating, now = new Date()): Progress {
  const day = dayKey(now);
  return {...progress, cards: {...progress.cards, [key]: schedule(progress.cards[key], rating, now)},
    activity: {...progress.activity, [day]: (progress.activity[day] ?? 0) + 1}};
}
export function descendants(nodes: CurriculumNode[], id: string): Set<string> {
  const result = new Set([id]); const children = new Map<string, string[]>();
  for (const n of nodes) if (n.parentId) children.set(n.parentId, [...(children.get(n.parentId) ?? []), n.id]);
  const queue = [id];
  for (let i=0; i<queue.length; i++) for (const child of children.get(queue[i]) ?? []) {
    if (!result.has(child)) { result.add(child); queue.push(child); }
  }
  return result;
}
export function breadcrumbs(nodes: CurriculumNode[], id: string): CurriculumNode[] {
  const byId = new Map(nodes.map(n => [n.id, n])); const result: CurriculumNode[] = []; const seen = new Set<string>();
  let current = byId.get(id);
  while (current && !seen.has(current.id)) { result.unshift(current); seen.add(current.id); current = byId.get(current.parentId ?? ''); }
  return result;
}
export const problemsFor = (data: Curriculum, id: string) => {
  const ids = descendants(data.nodes, id); return data.problems.filter(p => [...p.patternIds,...(p.collectionIds??[])].some(pattern => ids.has(pattern)));
};
export function studyQueue(data: Curriculum, progress: Progress, options: {nodeId?: string; limit?: number; now?: Date} = {}) {
  const now = (options.now ?? new Date()).getTime();
  const ids = options.nodeId ? descendants(data.nodes, options.nodeId) : undefined;
  return data.problems.flatMap(problem => problem.patternIds.filter(id => !ids || ids.has(id) || problem.collectionIds?.some(collection=>ids.has(collection))).map(patternId => ({problem, patternId, key: cardKey(problem.id, patternId)})))
    .filter(c => !progress.cards[c.key] || Date.parse(progress.cards[c.key].due) <= now)
    .sort((a,b) => {
      const x=progress.cards[a.key], y=progress.cards[b.key];
      if (x && y) return Date.parse(x.due)-Date.parse(y.due);
      return x ? -1 : y ? 1 : 0;
    }).slice(0, options.limit ?? 20);
}
export const isLearned = (progress: Progress, problem: Problem) => problem.patternIds.some(id => (progress.cards[cardKey(problem.id,id)]?.repetitions ?? 0) >= 2);

/** Strictly validate imports so malformed or oversized backups never erase existing progress. */
export function parseProgress(raw: string): Progress {
  if (raw.length > 10_000_000) throw new Error('Backup is too large (maximum 10 MB).');
  const value = JSON.parse(raw);
  const object = (x: unknown): x is Record<string, unknown> => !!x && typeof x === 'object' && !Array.isArray(x);
  if (!object(value) || value.version !== 1 || !object(value.cards) || !object(value.drafts) || !object(value.activity) || !Array.isArray(value.bookmarks)) throw new Error('This is not a Pattern Atlas version 1 backup.');
  const result = emptyProgress();
  for (const [key,r] of Object.entries(value.cards)) {
    if (!object(r) || !['again','hard','good','easy'].includes(String(r.rating)) || !Number.isFinite(Date.parse(String(r.due))) || !Number.isFinite(Date.parse(String(r.lastReviewed))) || !['repetitions','lapses','interval'].every(k => typeof r[k] === 'number' && Number.isFinite(r[k]) && Number(r[k])>=0)) throw new Error('A review record in this backup is invalid.');
    if (['__proto__','constructor','prototype'].includes(key)) throw new Error('Invalid record key.');
    result.cards[key]=r as unknown as Review;
  }
  for (const [key,draft] of Object.entries(value.drafts)) {
    if (typeof draft !== 'string' || draft.length > 200_000 || ['__proto__','constructor','prototype'].includes(key)) throw new Error('A code draft in this backup is invalid.');
    result.drafts[key]=draft;
  }
  if (!value.bookmarks.every(x => typeof x === 'string')) throw new Error('Invalid bookmarks.');
  result.bookmarks = [...new Set(value.bookmarks as string[])];
  for (const [day,count] of Object.entries(value.activity)) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day) || typeof count !== 'number' || !Number.isInteger(count) || count<0) throw new Error('Invalid activity history.');
    result.activity[day]=count;
  }
  if(value.leetcode != null) result.leetcode=validateHistory(value.leetcode);
  if(value.visits != null) result.visits=validateVisits(value.visits);
  return result;
}

export type ProblemOrder = 'difficulty' | 'difficulty-desc' | 'number' | 'number-desc' | 'title';
export const problemOrders: {value:ProblemOrder; label:string}[] = [
  {value:'difficulty',label:'Difficulty: easy to hard'}, {value:'difficulty-desc',label:'Difficulty: hard to easy'},
  {value:'number',label:'Problem number: ascending'}, {value:'number-desc',label:'Problem number: descending'},
  {value:'title',label:'Title: A–Z'},
];
export function sortProblems<T extends CatalogProblem>(problems: readonly T[], order: ProblemOrder): T[] {
  const rank={Easy:0,Medium:1,Hard:2};
  const number=(a:T,b:T)=>a.id.localeCompare(b.id,'en',{numeric:true});
  return [...problems].sort((a,b)=>{
    if(order==='title') return a.title.localeCompare(b.title,'en')||number(a,b);
    if(order==='number'||order==='number-desc') return number(a,b)*(order==='number-desc'?-1:1);
    return (rank[a.difficulty]-rank[b.difficulty])*(order==='difficulty-desc'?-1:1)||number(a,b);
  });
}
/** Source membership is explicit. Related source sections are not exact-pattern claims. */
export function libraryEntriesFor(data: Curriculum, nodeId?: string): CatalogProblem[] {
  if(!nodeId) return data.catalog??data.problems;
  const scope=descendants(data.nodes,nodeId);
  const ids=new Set(problemsFor(data,nodeId).map(p=>p.id));
  for(const node of data.nodes) if(scope.has(node.id)) for(const id of node.problemIds??[]) ids.add(id);
  return (data.catalog??data.problems).filter(p=>ids.has(p.id));
}
