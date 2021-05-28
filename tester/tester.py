import os
import requests
import urllib3
import time
import sys
import yaml
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AUTOMATION_LIST = []

# Define Critical Automation List to be tested
def load_config_file(config_file):
  with open(config_file) as automation_list:
    AUTOMATION_LIST = yaml.load(automation_list, Loader=yaml.CLoader)
    return AUTOMATION_LIST

# Define Ansible Credential
ANSIBLE_HOST = os.getenv('ANSIBLE_HOST')
ANSIBLE_HEADERS = {"Authorization": f"Bearer {os.getenv('ANSIBLE_TOKEN')}"}

# Execute automation using Ansible API
def launch_automation(id):
    r = requests.post(f"{ANSIBLE_HOST}/api/v2/job_templates/{id}/launch/", headers=ANSIBLE_HEADERS, verify = False)
    try:
      return r.json()['job']
    except Exception as e:
      print(f"FAILED TO LAUNCH THE AUTOMATION WITH ID: {id}")
      print(r.json()['detail'])
      sys.exit(1)


# Get status from Ansible Job Execution
def get_automation_status(job_id):
  r = requests.get(f"{ANSIBLE_HOST}/api/v2/jobs/{job_id}", headers=ANSIBLE_HEADERS, verify = False)
  return r.json()['status']

# Print Results in a friendly way
def print_results(results):
  print("#######################################################")
  print("These are the results of the critical automation tests:")
  print("#######################################################")
  for result in results:
    print(f"Name: {result['name']} - ID: {result['id']} - Status: {result['execution_status'].upper()}")
    print('-----------------------------------------------------')
  print("#######################################################")  




# Orchestrate this module execution
def main():
  AUTOMATION_LIST = load_config_file(sys.argv[1])
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

  print_results(AUTOMATION_LIST)
  if len([automation for automation in AUTOMATION_LIST if automation['execution_status'] != "successful"]) > 0:
    sys.exit(1)
  else:
    sys.exit(0)
    


if __name__ == '__main__':
  main()


  