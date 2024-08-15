'''
    File name: export-users.py
    Author: Alan Kelly
    Email: alan.kelly@intl.att.com
    Date created: 13/09/2022
    Date last modified: 
    Description: This script will download all users on an USM Anywhere Instance and return them in TAB Space Value format.
'''

import requests
import sys

TAB = "\t"
email="Email"


cookie = {'JSESSIONID': ''}
api_path = '/api/2.0/users'

def help():
    print("Script usage:")
    print("python3 export-users.py <SUBDOMAIN> <JSESSIONID>")
    print("Example usage:")
    print("python3 export-users.py https://subdomain.alienvault.cloud node065fwtf39oe9dxcxvu1j8v50k54987.node0")

if len(sys.argv) != 3:
    print("ERROR: Wrong number of arguments." + str(len(sys.argv)))
    help()
    print("Exiting!")
    exit(0)
else:
    if not str(sys.argv[1]).lower().startswith("https://") and not str(sys.argv[1]).lower().endswith(".alienvault.cloud"):
        print("first argument is not a valid USM URL")
        print("subdomain should start with https:// and end with .alienvault.cloud")
        print("Example :")
        print("https://subdomain.alienvault.cloud")
        print("Exiting!")
        exit(1)

url = sys.argv[1] + api_path
cookie['JSESSIONID'] = str(sys.argv[2])
try:
    r = requests.get(url, cookies=cookie)
except:
    print("ERROR: With Request")
    exit(2)


if r.status_code == 200:
    print("User", TAB, "User Email", TAB, "Role", TAB, "Status", TAB, "Enabled", TAB, "MFA", TAB, "Account Locked")
    data = r.json()['_embedded']['users']
    for i in data:
        # user = i['fullName']
        # user_email = i['email']
        # role = i['roles'][0]['name']
        status = "Disabled"
        if i['enabled']:
            status = "Enabled"
        mfa = "Disabled"
        if i['mfa']:
            mfa = "Enabled"
        account_locked =  "NO"
        if i['locked']:
            account_locked = "YES"
        print(i['fullName'], TAB, i['email'], TAB, i['roles'][0]['name'], TAB, status, TAB, mfa, TAB, account_locked)
else:
    print("ERROR: Request status = " + str(r.status_code))



