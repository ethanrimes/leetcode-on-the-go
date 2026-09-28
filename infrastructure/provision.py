"""Provision the project storage table and private API settings without logging secrets."""
import hashlib
import json
import os
import secrets
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'infrastructure/azure.json').read_text())

def az(*args, secret=False):
    command = ['az', *args, '--subscription', CONFIG['subscriptionId'], '--only-show-errors', '-o', 'json']
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        if secret:
            raise RuntimeError('Could not configure private Azure app settings.')
        raise RuntimeError(result.stderr.strip() or 'Azure command failed.')
    return json.loads(result.stdout) if result.stdout.strip() else None

deployment = az('deployment', 'group', 'create', '--resource-group', CONFIG['resourceGroup'],
                '--name', 'pattern-atlas-infrastructure', '--template-file', str(ROOT / 'infrastructure/main.bicep'))
storage = deployment['properties']['outputs']['storageName']['value']
connection = az('storage', 'account', 'show-connection-string', '--name', storage,
                '--resource-group', CONFIG['resourceGroup'])['connectionString']

private = ROOT / '.local'
private.mkdir(mode=0o700, exist_ok=True)
os.chmod(private, 0o700)
key_file = private / 'cloud-sync-key'
if not key_file.exists():
    descriptor = os.open(key_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as stream:
        stream.write(secrets.token_urlsafe(48))
os.chmod(key_file, 0o600)
key_hash = hashlib.sha256(key_file.read_text().strip().encode()).hexdigest()
account = CONFIG['leetcodeAccount']
owner = CONFIG['ownerGithub']

az('staticwebapp', 'appsettings', 'set', '--name', CONFIG['siteName'],
   '--resource-group', CONFIG['resourceGroup'], '--setting-names',
   f'PATTERN_ATLAS_TABLE_CONNECTION={connection}',
   f'PATTERN_ATLAS_SYNC_KEY_SHA256={key_hash}',
   f'PATTERN_ATLAS_OWNER_GITHUB={owner}',
   f'PATTERN_ATLAS_LEETCODE_ACCOUNT={account}', secret=True)
print(f'Provisioned private history table in {storage}; API settings configured.')
