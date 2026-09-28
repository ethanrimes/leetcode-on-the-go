import {app} from '@azure/functions';
import {TableClient} from '@azure/data-tables';
import {authorize, parseExport, readHistory, saveHistory, toExport} from './history-store.mjs';

const json = (status, body) => ({status, jsonBody: body, headers: {'Cache-Control': 'private, no-store'}});
const settings = () => ({
  tokenHash: process.env.PATTERN_ATLAS_SYNC_KEY_SHA256,
  githubOwner: process.env.PATTERN_ATLAS_OWNER_GITHUB,
  leetcodeAccount: process.env.PATTERN_ATLAS_LEETCODE_ACCOUNT,
});
let client;
const table = () => {
  if (!process.env.PATTERN_ATLAS_TABLE_CONNECTION) throw new Error('Table connection is not configured.');
  return client ??= TableClient.fromConnectionString(process.env.PATTERN_ATLAS_TABLE_CONNECTION, 'PatternAtlasHistory');
};

app.http('history', {
  route: 'history', methods: ['GET', 'POST'], authLevel: 'anonymous',
  handler: async (request, context) => {
    const config = settings();
    if (!config.tokenHash || !config.githubOwner || !config.leetcodeAccount) return json(503, {error: 'Cloud history is not configured.'});
    if (!authorize(request.headers, config)) return json(401, {error: 'Sign in with the owner GitHub account or use the sync key.'});
    try {
      const store = table();
      if (request.method === 'GET') {
        const {history} = await readHistory(store);
        return history ? json(200, toExport(history)) : {status: 204, headers: {'Cache-Control': 'private, no-store'}};
      }
      const source = await request.text();
      if (Buffer.byteLength(source, 'utf8') > 10_000_000) return json(413, {error: 'History exceeds the 10 MB import limit.'});
      const incoming = parseExport(JSON.parse(source));
      if (incoming.account.toLowerCase() !== config.leetcodeAccount.toLowerCase()) return json(409, {error: 'LeetCode account mismatch.'});
      const saved = await saveHistory(store, incoming);
      return json(200, {account: saved.account, completed: saved.completions?.slugs.length ?? 0,
        submissions: Object.keys(saved.submissions).length, exportedAt: saved.exportedAt});
    } catch (error) {
      if (error instanceof SyntaxError || (error instanceof Error && /Invalid|mismatch|exceeds/.test(error.message))) {
        return json(400, {error: error instanceof Error ? error.message : 'Invalid history.'});
      }
      context.error('Cloud history request failed', error);
      return json(503, {error: 'Cloud history is temporarily unavailable.'});
    }
  },
});
