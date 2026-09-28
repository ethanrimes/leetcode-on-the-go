import test from 'node:test';
import assert from 'node:assert/strict';
import { parseSecrets, validateProfile, release } from './ios-release.mjs';

const now = Date.parse('2026-09-27T00:00:00Z');
const certificate = Buffer.from('fixture certificate');
const profile = () => ({ uuid: '12345678-1234-1234-1234-123456789ABC', name: 'Fixture',
  team: [release.teamId], appId: `${release.teamId}.${release.bundleId}`,
  debug: false, beta: true, devices: false, allDevices: false,
  expires: '2027-05-14T06:17:21Z', certificates: [certificate.toString('base64')] });

test('credential parser preserves multiline keys, punctuation and quoted passwords as data', () => {
  const parsed = parseSecrets('API_KEY=YWJj\nZGVm\n\nP12_PASSWORD="value=with:punctuation"\nBUNDLE_ID: example.app\n');
  assert.equal(parsed.API_KEY, 'YWJj\nZGVm');
  assert.equal(parsed.P12_PASSWORD, 'value=with:punctuation');
  assert.equal(parsed.BUNDLE_ID, 'example.app');
  assert.equal(parseSecrets('PASSWORD=$(touch /tmp/must-not-execute)').PASSWORD, '$(touch /tmp/must-not-execute)');
});

test('accepts a current App Store profile for the exact app, team and certificate', () => {
  assert.equal(validateProfile(profile(), certificate, now).name, 'Fixture');
});

test('rejects a valid profile from the other app in the supplied credential folder', () => {
  assert.throws(() => validateProfile({ ...profile(), appId: `${release.teamId}.com.ethankallett.moneycontrol` }, certificate, now), /different app/);
  assert.throws(() => validateProfile({ ...profile(), team: ['OTHERTEAM1'] }, certificate, now), /different app/);
});

test('rejects development, ad hoc and enterprise profiles', () => {
  for (const change of [{ debug: true }, { devices: true }, { allDevices: true }, { beta: false }]) {
    assert.throws(() => validateProfile({ ...profile(), ...change }, certificate, now), /App Store distribution/);
  }
});

test('rejects expired profiles, including the exact expiry instant and invalid dates', () => {
  for (const expires of ['2026-01-01T00:00:00Z', new Date(now).toISOString(), 'invalid']) {
    assert.throws(() => validateProfile({ ...profile(), expires }, certificate, now), /expiry|expired/);
  }
});

test('rejects a profile signed for another certificate', () => {
  assert.throws(() => validateProfile(profile(), Buffer.from('other certificate'), now), /supplied signing certificate/);
});

test('rejects profile UUIDs that could escape the installation path or environment file', () => {
  for (const uuid of ['../../other-profile', '12345678-1234-1234-1234-123456789ABC\nEXTRA=value']) {
    assert.throws(() => validateProfile({ ...profile(), uuid }, certificate, now), /UUID/);
  }
});
