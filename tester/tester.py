import os
import requests
import urllib3
import time
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Define Critical Automation List to be tested
AUTOMATION_LIST = [
  {
    'id': 88,
    'name': 'HelloWorld',
    'timeout': 20
  },
]

# Define Ansible Credential
ANSIBLE_HOST = os.getenv('ANSIBLE_HOST')
ANSIBLE_HEADERS = {"Authorization": f"Bearer {os.getenv('ANSIBLE_TOKEN')}"}

# Execute automation using Ansible API
def launch_automation(id):
  r = requests.post(f"{ANSIBLE_HOST}/api/v2/job_templates/{id}/launch/", headers=ANSIBLE_HEADERS, verify = False)
  return r.json()['job']

# Get status from Ansible Job Execution
def get_automation_status(job_id):
  r = requests.get(f"{ANSIBLE_HOST}/api/v2/jobs/{job_id}", headers=ANSIBLE_HEADERS, verify = False)
  return r.json()['status']

# Orchestrate this module execution
def main():
  for automation in AUTOMATION_LIST:
    job_id = launch_automation(automation['id'])
    run_time = 0
    increment_time = 5
    while run_time <= automation['timeout']:
      automation['execution_status'] = 'timeout'
      time.sleep(5)
      automation['execution_status'] = get_automation_status(job_id)
      if automation['execution_status'] == 'successful':
        break
      if automation['execution_status'] == 'failed':
        break
      
      run_time += increment_time

  print(AUTOMATION_LIST)
  if len([automation for automation in AUTOMATION_LIST if automation['execution_status'] != "successful"]) > 0:
    sys.exit(1)
  else:
    sys.exit(0)
    


if __name__ == '__main__':
  print(main())