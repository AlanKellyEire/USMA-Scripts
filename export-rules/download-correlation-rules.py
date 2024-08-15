'''
    File name: download-correlation-rules.py
    Author: Alan Kelly
    Email: alan.kelly@intl.att.com
    Date created: 17/06/2021
    Date last modified: 02/08/2021
    Description: This script will download correlation rules from a USM Anywhere Instance and return them in TAB Space Value format.

    Usage:
    python3 download-correlation-rules.py https://SUBDOMAIN.alienvault.cloud JSESSIONID
'''


import requests
import sys

TAB = "\t"
email="Email"


cookie = {'JSESSIONID': ''}
api_path = '/api/2.0/rulePacks'

def help():
    print("Script usage:")
    print("python3 download-rules.py <SUBDOMAIN> <JSESSIONID>")
    print("Example usage:")
    print("python3 download-rules.py https://subdomain.alienvault.cloud node065fwtf39oe9dxcxvu1j8v50k54987.node0")

if len(sys.argv) != 3:
    print("ERROR: Wrong number of arguments. " + str(len(sys.argv)))
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
    print("Rule_Name", TAB, "Rule Intent", TAB, "Rule Description", TAB, "Rule Type", TAB, "Rule Conditions", TAB, "Mute", TAB, "Strategy", TAB, "Method", TAB, "Mitre Attack ID")

    data = r.json()
    for i in data:
        print(i["id"], TAB, i["intent"], TAB, "method-definition" in i and i["method-definition"] or "NONE", TAB, "Correlation Alarm Rule", TAB, i["conditions"], TAB, "mute-length" in i and i["mute-length"] or "No Mute Time", TAB, i["strategy"], TAB, i["method"], TAB, i["attack_id"])
else:
    print("ERROR: Request status = " + str(r.status_code))
