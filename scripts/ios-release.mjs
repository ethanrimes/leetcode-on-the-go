#!/usr/bin/env node
// Local credential inspection / GitHub signing setup. Never execute the secrets file.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createPrivateKey, createPublicKey, sign, X509Certificate } from 'node:crypto';
import { spawnSync } from 'node:child_process';

export const release = {
  repo: 'ethanrimes/leetcode-on-the-go', appId: '6816836452',
  bundleId: 'com.ethanrimes.leetcode-on-the-go', teamId: 'XKXCB8B22L',
};
const apiOrigin = 'https://api.appstoreconnect.apple.com';

export function parseSecrets(text) {
  const entries = [...text.matchAll(/^\s*([A-Z][A-Z0-9_]*)\s*[:=][ \t]*/gm)];
  return Object.fromEntries(entries.map((entry, index) => {
    let value = text.slice(entry.index + entry[0].length, entries[index + 1]?.index ?? text.length).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
    return [entry[1], value];
  }));
}

function command(executable, args, input) {
  const result = spawnSync(executable, args, { input, maxBuffer: 4 * 1024 * 1024 });
  if (result.status !== 0) throw new Error(`${executable} failed; check its installation, authentication, and file permissions.`);
  return result.stdout;
}

function p12Certificate(path, password) {
  const args = ['pkcs12', '-in', path, '-passin', 'stdin', '-info', '-clcerts', '-nokeys'];
  let result = spawnSync('openssl', args, { input: `${password}\n` });
  // Older Apple exports use RC2 encryption, which OpenSSL 3 decodes via its legacy provider.
  if (result.status !== 0 && /unsupported/i.test(result.stderr?.toString() ?? '')) {
    result = spawnSync('openssl', ['pkcs12', '-legacy', ...args.slice(1)], { input: `${password}\n` });
  }
  if (result.status !== 0) throw new Error('Cannot open the signing certificate with P12_PASSWORD.');
  if (!/shrouded keybag|key bag|keybag/i.test(result.stderr.toString())) throw new Error('The P12 must include the signing private key.');
  return new X509Certificate(result.stdout);
}

function decodeProfile(bytes) {
  const xml = command('openssl', ['smime', '-verify', '-inform', 'DER', '-noverify'], bytes);
  // Parse Apple's CMS payload; certificate and app identity are validated below.
  const json = command('python3', ['-c', `import sys,plistlib,json,base64
p=plistlib.loads(sys.stdin.buffer.read())
print(json.dumps({'uuid':p['UUID'],'name':p['Name'],'team':p.get('TeamIdentifier',[]),
'appId':p.get('Entitlements',{}).get('application-identifier'),
'debug':p.get('Entitlements',{}).get('get-task-allow',False),
'beta':p.get('Entitlements',{}).get('beta-reports-active',False),
'devices':'ProvisionedDevices' in p,'allDevices':p.get('ProvisionsAllDevices',False),
'expires':p['ExpirationDate'].isoformat()+'Z',
'certificates':[base64.b64encode(c).decode() for c in p.get('DeveloperCertificates',[])]}))`], xml);
  return JSON.parse(json);
}

export function validateProfile(profile, certificate, now = Date.now()) {
  if (profile.appId !== `${release.teamId}.${release.bundleId}` || !profile.team.includes(release.teamId)) throw new Error('Provisioning profile belongs to a different app or team.');
  if (profile.debug || profile.devices || profile.allDevices || !profile.beta) throw new Error('An App Store distribution profile is required.');
  if (!Number.isFinite(Date.parse(profile.expires)) || Date.parse(profile.expires) <= now) throw new Error('Provisioning profile has expired or has an invalid expiry date.');
  if (!profile.certificates.some(value => Buffer.from(value, 'base64').equals(certificate))) throw new Error('Profile does not include the supplied signing certificate.');
  if (!/^[A-F0-9-]{36}$/i.test(profile.uuid)) throw new Error('Invalid provisioning profile UUID.');
  return profile;
}

function loadCredentials(folder) {
  const fields = parseSecrets(readFileSync(resolve(folder, 'secrets'), 'utf8'));
  for (const key of ['APPSTORE_API_KEY_ID', 'APPSTORE_API_ISSUER_ID', 'APPSTORE_API_PRIVATE_KEY', 'P12_PASSWORD']) {
    if (!fields[key]) throw new Error(`Missing ${key} in the credentials file.`);
  }
  if (!/^[A-Z0-9]{10}$/.test(fields.APPSTORE_API_KEY_ID) || !/^[a-f0-9-]{36}$/i.test(fields.APPSTORE_API_ISSUER_ID)) throw new Error('Invalid App Store Connect key or issuer ID.');
  const privateKey = readFileSync(resolve(folder, `AuthKey_${fields.APPSTORE_API_KEY_ID}.p8`));
  const parsedKey = createPrivateKey(privateKey);
  if (parsedKey.asymmetricKeyType !== 'ec' || parsedKey.asymmetricKeyDetails?.namedCurve !== 'prime256v1') throw new Error('The App Store Connect key must use P-256.');
  const publicKey = value => createPublicKey(value).export({ type: 'spki', format: 'der' });
  const embedded = fields.APPSTORE_API_PRIVATE_KEY.includes('-----BEGIN')
    ? Buffer.from(fields.APPSTORE_API_PRIVATE_KEY)
    : Buffer.from(fields.APPSTORE_API_PRIVATE_KEY.replace(/\s/g, ''), 'base64');
  const embeddedKey = embedded.includes('-----BEGIN') ? createPrivateKey(embedded)
    : createPrivateKey({ key: embedded, format: 'der', type: 'pkcs8' });
  if (!publicKey(parsedKey).equals(publicKey(embeddedKey))) throw new Error('The two API key copies do not match.');
  const certificatePath = resolve(folder, 'Certificates.p12');
  const certificate = p12Certificate(certificatePath, fields.P12_PASSWORD);
  if (!certificate.raw.equals(readFileSync(resolve(folder, 'distribution.cer')))) throw new Error('Distribution certificate does not match the P12.');
  if (!certificate.subject.split('\n').includes(`OU=${release.teamId}`) || !certificate.subject.includes('CN=Apple Distribution:')) throw new Error('Wrong signing team or certificate type.');
  if (Date.parse(certificate.validTo) <= Date.now() || Date.parse(certificate.validFrom) > Date.now()) throw new Error('Signing certificate is not currently valid.');
  return { fields, privateKey, certificate, certificatePath };
}

function authorization(credentials) {
  const encode = value => Buffer.from(JSON.stringify(value)).toString('base64url');
  const now = Math.floor(Date.now() / 1000);
  const body = `${encode({ alg: 'ES256', kid: credentials.fields.APPSTORE_API_KEY_ID, typ: 'JWT' })}.${encode({ iss: credentials.fields.APPSTORE_API_ISSUER_ID, iat: now, exp: now + 600, aud: 'appstoreconnect-v1' })}`;
  return `${body}.${sign('sha256', Buffer.from(body), { key: credentials.privateKey, dsaEncoding: 'ieee-p1363' }).toString('base64url')}`;
}

async function request(credentials, path, body) {
  const url = new URL(path, apiOrigin);
  if (url.origin !== apiOrigin) throw new Error('Refusing to send Apple credentials to another origin.');
  let response;
  try {
    response = await fetch(url, { method: body ? 'POST' : 'GET', redirect: 'error', signal: AbortSignal.timeout(30000), headers: { Authorization: `Bearer ${authorization(credentials)}`, 'Content-Type': 'application/json' }, ...(body ? { body: JSON.stringify(body) } : {}) });
  } catch { throw new Error('Cannot reach App Store Connect. Run this command with network access to Apple.'); }
  if (!response.ok) throw new Error(`App Store Connect returned HTTP ${response.status}. Confirm the API key has access to this app and to Certificates, Identifiers & Profiles.`);
  return response.json();
}

async function list(credentials, path) {
  const rows = [];
  while (path) {
    const page = await request(credentials, path);
    rows.push(...page.data); path = page.links?.next;
  }
  return rows;
}

async function configure(credentials) {
  // Check GitHub authentication and repository access before creating Apple resources.
  command('gh', ['repo', 'view', release.repo, '--json', 'nameWithOwner']);
  const app = await request(credentials, `/v1/apps/${release.appId}`);
  if (app.data.attributes.bundleId !== release.bundleId) throw new Error('The App Store Connect app has a different bundle ID; nothing was changed.');
  const bundles = await list(credentials, `/v1/bundleIds?filter[identifier]=${release.bundleId}&limit=200`);
  const bundle = bundles.find(item => item.attributes.identifier === release.bundleId);
  if (!bundle) throw new Error('The API key cannot access the registered bundle ID.');
  const certificates = await list(credentials, '/v1/certificates?limit=200');
  const certificate = certificates.find(item => Buffer.from(item.attributes.certificateContent ?? '', 'base64').equals(credentials.certificate.raw));
  if (!certificate) throw new Error('The supplied certificate is not available to this API key.');

  const profiles = await list(credentials, '/v1/profiles?filter[profileType]=IOS_APP_STORE&limit=200');
  let selected;
  for (const item of profiles) {
    if (item.attributes.profileState !== 'ACTIVE' || !item.attributes.profileContent) continue;
    try {
      const bytes = Buffer.from(item.attributes.profileContent, 'base64');
      validateProfile(decodeProfile(bytes), credentials.certificate.raw);
      selected = bytes; break;
    } catch { /* Other apps and expired profiles are left untouched. */ }
  }
  if (!selected) {
    const created = await request(credentials, '/v1/profiles', { data: {
      type: 'profiles', attributes: { name: `Pattern Atlas App Store ${new Date().toISOString().replace(/[:.]/g, '-')}`, profileType: 'IOS_APP_STORE' },
      relationships: { bundleId: { data: { type: 'bundleIds', id: bundle.id } }, certificates: { data: [{ type: 'certificates', id: certificate.id }] } },
    } });
    selected = Buffer.from(created.data.attributes.profileContent, 'base64');
  }
  const profile = validateProfile(decodeProfile(selected), credentials.certificate.raw);
  const values = {
    APPLE_TEAM_ID: release.teamId,
    BUILD_CERTIFICATE_BASE64: readFileSync(credentials.certificatePath).toString('base64'),
    P12_PASSWORD: credentials.fields.P12_PASSWORD,
    BUILD_PROVISION_PROFILE_BASE64: selected.toString('base64'),
    APP_STORE_CONNECT_API_KEY_ID: credentials.fields.APPSTORE_API_KEY_ID,
    APP_STORE_CONNECT_API_KEY_ISSUER_ID: credentials.fields.APPSTORE_API_ISSUER_ID,
    APP_STORE_CONNECT_API_KEY_BASE64: credentials.privateKey.toString('base64'),
  };
  for (const [name, value] of Object.entries(values)) {
    command('gh', ['secret', 'set', name, '--repo', release.repo], value);
    console.log(`Configured repository secret: ${name}`);
  }
  console.log(`Ready: ${release.bundleId}; profile ${profile.name}. Push main to start the TestFlight workflow.`);
}

async function main() {
  const [action, path, certificatePath] = process.argv.slice(2);
  if (action === 'validate-profile') {
    if (!path || !certificatePath || !process.env.P12_PASSWORD) throw new Error('Provide the profile path, P12 path, and P12_PASSWORD.');
    const certificate = p12Certificate(certificatePath, process.env.P12_PASSWORD);
    if (Date.parse(certificate.validTo) <= Date.now() || Date.parse(certificate.validFrom) > Date.now()) throw new Error('Signing certificate is not currently valid.');
    const profile = validateProfile(decodeProfile(readFileSync(path)), certificate.raw);
    console.log(JSON.stringify({ uuid: profile.uuid, name: profile.name, team: release.teamId, bundleId: release.bundleId }));
    return;
  }
  if (!['inspect', 'configure'].includes(action) || !path) throw new Error('Usage: node scripts/ios-release.mjs inspect|configure <credentials-folder>');
  const credentials = loadCredentials(path);
  if (action === 'configure') return configure(credentials);
  let profileMatches = false;
  if (credentials.fields.BUILD_PROVISION_PROFILE_BASE64) {
    try { validateProfile(decodeProfile(Buffer.from(credentials.fields.BUILD_PROVISION_PROFILE_BASE64, 'base64')), credentials.certificate.raw); profileMatches = true; } catch { /* Report the mismatch without exposing profile contents. */ }
  }
  console.log(JSON.stringify({ apiKeyParses: true, apiKeyCopiesMatch: true, p12PasswordWorks: true, signingCertificateMatches: true, certificateExpires: credentials.certificate.validTo, teamId: release.teamId, targetBundleId: release.bundleId, suppliedProfileMatches: profileMatches, applePermissionsVerified: false }, null, 2));
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
