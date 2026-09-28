import {test} from 'node:test';
import assert from 'node:assert/strict';
import {activitySummary,parseSubmissionExport,mergeHistory,validateCalendars,type Submission} from './index';
const entry=(id:string,timestamp:string):Submission=>({id,slug:'two-sum',title:'Two Sum',timestamp,status:'Accepted',language:'python3'});
const packet=(calendars?:unknown,submissions:Submission[]=[])=>JSON.stringify({format:'pattern-atlas-leetcode',version:1,account:'demo',exportedAt:'2026-09-28T01:00:00.000Z',complete:false,calendars,submissions});
const calendar={year:2025,observedAt:'2026-09-28T01:00:00.000Z',days:{'2025-05-01':10,'2025-05-02':20,'2025-12-03':2}};

test('source calendars supply complete totals without inventing missing submission details or verdicts',()=>{
 const history=parseSubmissionExport(packet({'2025':calendar},[entry('1','2025-05-01T00:30:00Z')]));
 const result=activitySummary(history,2025,new Date('2026-09-28T02:00:00Z'));
 assert.equal(result.total,32);assert.equal(result.imported,1);assert.equal(result.accepted,1);
 assert.equal(result.activeDays,3);assert.equal(result.longest,2);assert.equal(result.current,0);
 assert.equal(result.counts['2025-12-03'],2);assert.equal(result.byDay['2025-12-03'],undefined);
 // UTC midnight must not become the preceding local day.
 assert.equal(result.byDay['2025-05-01'].length,1);
});
test('streaks use the selected year, newer details augment a snapshot once, and future activity is excluded',()=>{
 const history=parseSubmissionExport(packet({'2026':{year:2026,observedAt:'2026-01-02T01:00:00Z',days:{'2026-01-01':2,'2026-01-02':1}}},[
  entry('1','2025-12-31T23:59:59Z'),entry('2','2026-01-02T00:00:00Z'),entry('3','2026-01-02T02:00:00Z'),entry('4','2026-01-03T00:00:00Z'),entry('5','2026-01-04T00:00:00Z')]));
 const result=activitySummary(history,2026,new Date('2026-01-03T01:00:00Z'));
 assert.equal(result.total,5);assert.equal(result.imported,3);assert.equal(result.longest,3);assert.equal(result.current,3);
 assert.equal(result.counts['2026-01-02'],2);assert.equal(result.counts['2026-01-04'],undefined);
 assert.equal(activitySummary(history,2025,new Date('2026-01-03T01:00:00Z')).current,0);
});
test('calendar snapshots survive old clients, partial updates and backups; invalid dates fail atomically',()=>{
 const original=parseSubmissionExport(packet({'2025':calendar}));
 const legacy=parseSubmissionExport(packet(undefined,[entry('1','2025-05-01T00:00:00Z')]));
 assert.deepEqual(mergeHistory(original,legacy).calendars,original.calendars);
 const older=parseSubmissionExport(packet({'2025':{...calendar,observedAt:'2025-12-31T00:00:00Z',days:{'2025-05-01':1}}}));
 assert.deepEqual(mergeHistory(original,older).calendars,original.calendars);
 for(const days of [{'2025-02-30':1},{'2024-05-01':1},{'2025-05-01':-1},{'2025-05-01':1.5}])assert.throws(()=>validateCalendars({'2025':{...calendar,days}}));
 assert.throws(()=>validateCalendars({'2025':{...calendar,observedAt:'2025-01-01T00:00:00Z'}}));
});
