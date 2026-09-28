import {createHash, randomUUID, timingSafeEqual} from 'node:crypto';
import {gzipSync, gunzipSync} from 'node:zlib';
import {validateCalendars, mergeCalendars} from './activity-calendar.mjs';

const isObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const validDate = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T/.test(value) && Number.isFinite(Date.parse(value));
const validSlug = value => typeof value === 'string' && value.length <= 300 && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value);

export function parseExport(value) {
  if (!isObject(value) || value.format !== 'pattern-atlas-leetcode' || value.version !== 1 ||
      typeof value.account !== 'string' || !value.account || value.account.length > 300 ||
      !validDate(value.exportedAt) || typeof value.complete !== 'boolean' || !Array.isArray(value.submissions) ||
      (value.through !== undefined && (typeof value.through !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value.through)))) {
    throw new Error('Invalid LeetCode history export.');
  }
  const submissions = Object.create(null);
  for (const entry of value.submissions) {
    if (!isObject(entry) || typeof entry.id !== 'string' || !/^\d{1,30}$/.test(entry.id) ||
        !validSlug(entry.slug) || !validDate(entry.timestamp) ||
        !['title', 'status', 'language'].every(key => typeof entry[key] === 'string' && entry[key].length <= 500) || !entry.status) {
      throw new Error('Invalid submission in history export.');
    }
    submissions[entry.id] = {id: entry.id, slug: entry.slug, title: entry.title,
      timestamp: entry.timestamp, status: entry.status, language: entry.language};
  }
  let completions;
  if (value.completions !== undefined) {
    const snapshot = value.completions;
    if (!isObject(snapshot) || !validDate(snapshot.observedAt) || !Array.isArray(snapshot.slugs) ||
        snapshot.slugs.length > 100_000 || !snapshot.slugs.every(validSlug)) {
      throw new Error('Invalid completion snapshot.');
    }
    completions = {observedAt: snapshot.observedAt, slugs: [...new Set(snapshot.slugs)].sort()};
  }
  return {account: value.account, exportedAt: value.exportedAt, complete: value.complete, calendars: validateCalendars(value.calendars),
    ...(value.through ? {through: value.through} : {}), ...(completions ? {completions} : {}), submissions};
}

export function mergeHistory(current, incoming) {
  if (!current) return incoming;
  if (current.account.toLowerCase() !== incoming.account.toLowerCase()) throw new Error('LeetCode account mismatch.');
  const newer = Date.parse(incoming.exportedAt) >= Date.parse(current.exportedAt);
  const a = current.completions, b = incoming.completions;
  const completions = !a ? b : !b ? a : Date.parse(b.observedAt) >= Date.parse(a.observedAt) ? b : a;
  return {...(newer ? incoming : current), completions, calendars: current.calendars || incoming.calendars ? mergeCalendars(current.calendars, incoming.calendars) : undefined,
    submissions: newer ? {...current.submissions, ...incoming.submissions} : {...incoming.submissions, ...current.submissions}};
}

export function toExport(history) {
  return {...history, format: 'pattern-atlas-leetcode', version: 1,
    submissions: Object.values(history.submissions).sort((a, b) => b.timestamp.localeCompare(a.timestamp) || b.id.localeCompare(a.id))};
}

export function authorize(headers, settings) {
  const token = headers.get('x-pattern-atlas-sync-key');
  if (token && settings.tokenHash && /^[0-9a-f]{64}$/i.test(settings.tokenHash)) {
    const expected = Buffer.from(settings.tokenHash, 'hex');
    const actual = createHash('sha256').update(token).digest();
    if (timingSafeEqual(expected, actual)) return true;
  }
  const encoded = headers.get('x-ms-client-principal');
  if (!encoded || !settings.githubOwner) return false;
  try {
    const user = JSON.parse(Buffer.from(encoded, 'base64').toString('utf8'));
    return user.identityProvider === 'github' &&
      user.userDetails?.toLowerCase() === settings.githubOwner.toLowerCase() &&
      Array.isArray(user.userRoles) && user.userRoles.includes('authenticated');
  } catch { return false; }
}

const partitionKey = 'owner';
const missing = error => error?.statusCode === 404;
const race = error => error?.statusCode === 409 || error?.statusCode === 412;
const chunkSize = 24_000;

export async function readHistory(table) {
  let pointer;
  try { pointer = await table.getEntity(partitionKey, 'current'); }
  catch (error) { if (missing(error)) return {history: undefined, pointer: undefined}; throw error; }
  if (!Number.isSafeInteger(pointer.parts) || pointer.parts < 1 || pointer.parts > 100 ||
      typeof pointer.version !== 'string' || !/^[0-9a-f-]{36}$/.test(pointer.version)) {
    throw new Error('Stored history pointer is invalid.');
  }
  const parts = await Promise.all(Array.from({length: pointer.parts}, (_, index) =>
    table.getEntity(partitionKey, `${pointer.version}-${String(index).padStart(3, '0')}`)));
  const encoded = parts.map(part => part.payload).join('');
  const raw = gunzipSync(Buffer.from(encoded, 'base64'), {maxOutputLength: 10_000_000}).toString('utf8');
  return {history: parseExport(JSON.parse(raw)), pointer};
}

export async function saveHistory(table, incoming) {
  for (let attempt = 0; attempt < 4; attempt++) {
    const {history: current, pointer} = await readHistory(table);
    const merged = mergeHistory(current, incoming);
    if (current && JSON.stringify(toExport(current)) === JSON.stringify(toExport(merged))) return current;
    const encoded = gzipSync(Buffer.from(JSON.stringify(toExport(merged)))).toString('base64');
    const chunks = encoded.match(new RegExp(`.{1,${chunkSize}}`, 'g')) ?? [];
    if (!chunks.length || chunks.length > 100) throw new Error('History exceeds cloud storage limits.');
    const version = randomUUID();
    await Promise.all(chunks.map((payload, index) => table.createEntity({partitionKey,
      rowKey: `${version}-${String(index).padStart(3, '0')}`, payload})));
    const entity = {partitionKey, rowKey: 'current', version, parts: chunks.length,
      account: merged.account, exportedAt: merged.exportedAt, updatedAt: new Date().toISOString(),
      completions: merged.completions?.slugs.length ?? 0, submissions: Object.keys(merged.submissions).length};
    try {
      if (pointer) await table.updateEntity(entity, 'Replace', {etag: pointer.etag});
      else await table.createEntity(entity);
      return merged;
    } catch (error) { if (!race(error) || attempt === 3) throw error; }
  }
  throw new Error('Concurrent history update could not be merged.');
}
