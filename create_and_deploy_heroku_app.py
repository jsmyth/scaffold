import subprocess
import requests
import sys
import json
import pprint
import getpass
from colorama import Fore, Style


# ----------------------------------
# 1. heroku container:login 
# 2. heroku create
# 3. heroku container:push web
# 4. heroku container:release web
# 5. heroku open
# ----------------------------------

app_name = 'jsmyth-tombstone'

API_ENDPOINT = 'https://api.heroku.com/apps'

data = {
  'name': f'{app_name}'
}

#token = getpass.getpass(prompt='Heroku Token: ')

#headers = {
#  'Accept': 'application/vnd.heroku+json; version=3',
#  'Authorization': f'Bearer {token}'
#}

def log_check(message):
  print(f' {Style.BRIGHT}{Fore.GREEN}\N{HEAVY CHECK MARK} {Style.RESET_ALL}{message}')

def log_error(message):
  print(f'❌ {Style.BRIGHT}{Fore.RED}{message}{Style.RESET_ALL}')

def log_info(message):
  print(f'👉 {Style.BRIGHT}{message}{Style.RESET_ALL}')

def log_launch(message):
  print(f'🚀 {Style.BRIGHT}{message}{Style.RESET_ALL}')

def run(command,universal_newlines=True):
    cp = subprocess.run(
        command,
        universal_newlines=universal_newlines,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if int(cp.returncode) > 0:
        log_error(f'ERROR({cp.returncode}): {cp.stderr}')
        sys.exit(cp.returncode)

    return(cp.stdout.strip())

log_check('Heroku container login')
run(["heroku", "container:login"])

log_launch('Heroku Create')
create_output = run(["heroku", "create", "-t", "learnsecurely"])
log_check(create_output)

log_launch('Heroku Container Push')
push_output = run(["heroku", "container:push", "web"])
log_check(push_output)

log_launch('Heroku Release')
release_output = run(["heroku", "container:release", "web"])
log_check('Heroku Container Released')
heroku_info_output = run(["heroku", "info"])
log_info(heroku_info_output)

#r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)
#print(f'Status Code: {r.status_code}')
#pprint.pprint(json.loads(r.content))

#if r.status_code != 200:
#  sys.exit()

#clone_url = r.text.clone_url
#subprocess.check_output(['git', 'clone', clone_url], cwd=repo_dir)
