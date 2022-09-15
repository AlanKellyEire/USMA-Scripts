'''
    File name: export-environment-users.py
    Author: Alan Kelly
    Email: alan.kelly@intl.att.com
    Date created: 15/09/2022
    Date last modified:
    Description: This script will export Users from the from environment/users page on USM Anywhere Instance and return them in TAB Space Value format.
'''

import requests
import sys
import datetime

TAB = "\t"
email="Email"


cookie = {'JSESSIONID': ''}
api_path = '/api/2.0/analysis/users'

def help():
    print("Script usage:")
    print("python3 export-environment-users.py <SUBDOMAIN> <JSESSIONID>")
    print("Example usage:")
    print("python3 export-environment-users.py https://subdomain.alienvault.cloud node065fwtf39oe9dxcxvu1j8v50k54987.node0")

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
    #get number of pages
    total_page = r.json()['page']['totalPages']
    print("Name", TAB, "Email", TAB, "Phone_Numbers", TAB, "Location", TAB, "Description", TAB, "Manager", TAB, "Status", TAB, "Created", TAB, "Last_Seen", TAB, "ID")
    # page count
    c = 0
    while c < total_page:
        # looping through all the pages and get each investigation.
        url = sys.argv[1] + api_path + '?page=' + str(c)
        cookie['JSESSIONID'] = str(sys.argv[2])
        try:
            r = requests.get(url, cookies=cookie)
        except:
            print("ERROR: With Request")
            exit(2)
        data = r.json()['_embedded']['users']
        for i in data:
            print(i['name'], TAB, i['emailAddresses'], TAB, i['phoneNumbers'], TAB, i['officeLocation'], TAB, i['description'], TAB, i['manager'], TAB, i['status'], TAB, i['created'], TAB, i['lastSeen'], TAB, i['id'])
        c += 1

else:
    print("ERROR: Request status = " + str(r.status_code))
