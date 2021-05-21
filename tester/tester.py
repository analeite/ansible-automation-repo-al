import os
import requests
import urllib3
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
    launch_automation(automation['id'])



if __name__ == '__main__':
  main()