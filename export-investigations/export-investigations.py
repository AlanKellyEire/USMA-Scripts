'''
    File name: export-investigations.py
    Author: Alan Kelly
    Email: alan.kelly@intl.att.com
    Date created: 22/07/2021
    Date last modified: 22/07/2021
    Description: This script will export investigations from a USM Anywhere Instance and return them in TAB Space Value format.
'''

import requests
import sys
import datetime

TAB = "\t"
email="Email"


cookie = {'JSESSIONID': ''}
api_path = '/api/2.0/investigations/search/r'

def help():
    print("Script usage:")
    print("python3 download-rules.py <SUBDOMAIN> <JSESSIONID>")
    print("Example usage:")
    print("python3 download-rules.py https://subdomain.alienvault.cloud node065fwtf39oe9dxcxvu1j8v50k54987.node0")

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
    data = r.json()['_embedded']['investigations']
    print("Title", TAB, "ID", TAB, "Severity", TAB, "Status", TAB, "Intent", TAB, "Created", TAB, "Assignee", TAB, "Last Updated", TAB, "Last Updated By", TAB, "UUID")
    for i in data:
        print(i['title'], TAB, i['investigationNumber'], TAB, i['severity']['name'], TAB, i['status']['name'], TAB, i['intent']['name'], TAB, datetime.datetime.fromtimestamp(i['created']/1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], TAB, i['assignee'], TAB, datetime.datetime.fromtimestamp(i['lastUpdated'] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], TAB, i['lastUpdatedBy'], TAB, i['id'])
else:
    print("ERROR: Request status = " + str(r.status_code))



