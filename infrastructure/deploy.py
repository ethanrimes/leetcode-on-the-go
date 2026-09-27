"""Deploy a built site. Credentials remain in subprocess memory, never files or logs."""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'infrastructure/azure.json').read_text())
def az(*args):
    return subprocess.check_output(['az', *args, '--subscription', config['subscriptionId'], '--only-show-errors', '-o', 'json'], text=True)

token = json.loads(az('staticwebapp', 'secrets', 'list', '--name', config['siteName'], '--resource-group', config['resourceGroup']))['properties']['apiKey']
env = os.environ.copy()
env['SWA_CLI_DEPLOYMENT_TOKEN'] = token
env['SWA_CLI_TELEMETRY'] = 'false'
subprocess.run(['npx', '--yes', '@azure/static-web-apps-cli@2.0.10', 'deploy', 'apps/web/dist', '--env', 'production', '--no-use-keychain'], cwd=ROOT, env=env, check=True)
site = json.loads(az('staticwebapp', 'show', '--name', config['siteName'], '--resource-group', config['resourceGroup']))
print('Deployed site: https://' + site['defaultHostname'])
