#!/usr/bin/env node
// Upload the private cumulative LeetCode export and confirm it is durable in Azure.
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const config = JSON.parse(await readFile(path.join(root, 'infrastructure/azure.json'), 'utf8'));
const history = JSON.parse(await readFile(path.join(root, '.local/leetcode-history.json'), 'utf8'));
const key = (await readFile(path.join(root, '.local/cloud-sync-key'), 'utf8')).trim();
const address = `https://${config.siteHostname ?? 'blue-sea-0c03ac51e.3.azurestaticapps.net'}/api/history`;
const headers = {'Content-Type': 'application/json', 'x-pattern-atlas-sync-key': key};
const saved = await fetch(address, {method: 'POST', headers, body: JSON.stringify(history), signal: AbortSignal.timeout(90_000)});
if (!saved.ok) throw new Error(`Azure history upload failed (${saved.status}): ${(await saved.text()).slice(0, 200)}`);
const result = await saved.json();
const fetched = await fetch(address, {headers, cache: 'no-store', signal: AbortSignal.timeout(90_000)});
if (!fetched.ok) throw new Error(`Azure history verification failed (${fetched.status}).`);
const remote = await fetched.json();
const remoteIds = new Set(remote.submissions.map(record => record.id));
const localIds = new Set(history.submissions.map(record => record.id));
const localSlugs = new Set(history.completions?.slugs ?? []);
const remoteSlugs = new Set(remote.completions?.slugs ?? []);
if (remote.account.toLowerCase() !== history.account.toLowerCase() ||
    [...localIds].some(id => !remoteIds.has(id)) || [...localSlugs].some(slug => !remoteSlugs.has(slug))) {
  throw new Error('Azure verification did not contain every local submission and completion.');
}
console.log(`Azure verified: ${remoteSlugs.size} completion snapshot slugs, ${remoteIds.size} dated submissions for ${result.account}.`);
