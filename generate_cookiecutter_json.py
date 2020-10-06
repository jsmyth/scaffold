import subprocess
import sys
import yaml
import json
import pprint
import click
import os
from colorama import Fore, Style

def horizontal_rule():
    print(f'{Style.BRIGHT}{Fore.BLUE}―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――{Style.RESET_ALL}')

def upper_rule():
    print(f'{Style.BRIGHT}{Fore.BLUE}▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔{Style.RESET_ALL}')

def lower_rule():
    print(f'{Style.BRIGHT}{Fore.BLUE}▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁{Style.RESET_ALL}')

def log_launch(message):
  print(f'🚀 {Style.BRIGHT}{message}{Style.RESET_ALL}')

def log_info(message):
  print(f'👉 {Style.BRIGHT}{message}{Style.RESET_ALL}')
  #print(f'👀 {Style.BRIGHT}{message}{Style.RESET_ALL}')

def log_question(message):
  print(f'❓ {Style.BRIGHT}{message}{Style.RESET_ALL}')

def log_check(message):
  print(f' {Style.BRIGHT}{Fore.GREEN}\N{HEAVY CHECK MARK} {Style.RESET_ALL}{message}')

def log_error(message):
  print(f'❌ {Style.BRIGHT}{Fore.RED}{message}{Style.RESET_ALL}')

def log_link(prefix="",url=""):
  print(f'   🌎 {Style.BRIGHT}{Fore.WHITE}{prefix} {Fore.CYAN}{url}{Style.RESET_ALL}')

def log_blank(message):
  print(f'   {message}')

def log_blank_bright(message):
  print(f'   {Style.BRIGHT}{message}{Style.RESET_ALL}')

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

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

scratch_dir = os.environ.get('scratch_dir')

full_name = click.prompt(f'❓ {Style.BRIGHT}Enter Full Name{Style.RESET_ALL}', type=str)

email = click.prompt(f'❓ {Style.BRIGHT}What is your email address{Style.RESET_ALL}', type=str)

project_name = click.prompt(f'❓ {Style.BRIGHT}Enter your Project Name{Style.RESET_ALL}', type=str)

project_short_description = click.prompt(f'❓ {Style.BRIGHT}A short description of your project{Style.RESET_ALL}', type=str)

app_name = click.prompt(f'❓ {Style.BRIGHT}Enter the Application Name{Style.RESET_ALL}', type=str, default=project_name.lower().replace('-', '_').replace(' ', '_'))

github_username = click.prompt(f'❓ {Style.BRIGHT}Enter the Github Username{Style.RESET_ALL}', type=str)

github_repo = click.prompt(f'❓ {Style.BRIGHT}Enter the Github Repository Name{Style.RESET_ALL}', type=str, default=app_name)

python_version = "3.8"

node_version = "12"

flask_cookiecutter = {
  "default_context": {
    "full_name": full_name,
    "email": email,
    "project_name": project_name,
    "project_short_description": project_short_description,
    "app_name": app_name,
    "github_username": github_username,
    "github_repo": github_repo,
    "python_version": python_version,
    "node_version": node_version
  }
}

with open(f'{scratch_dir}/cookiecutter.yaml', 'w') as outfile:
  yaml.dump(flask_cookiecutter, outfile, width=10000)

#log_check(f'Push to Github')
#push_branch_to_github()
