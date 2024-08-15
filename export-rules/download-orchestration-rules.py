'''
    File name: download-orchestration-rules.py
    Author: Alan Kelly
    Email: alan.kelly@intl.att.com
    Date created: 09/06/2021
    Date last modified: 09/06/2021
    Description: This script will download orchestration rules from a USM Anywhere Instance and return them in TAB Space Value format.
'''

import requests
import sys

TAB = "\t"
email="Email"


cookie = {'JSESSIONID': ''}
api_path = '/api/2.0/orchestrationRules'

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
    print("Rule_Name", TAB, "Rule Description", TAB, "Rule Type", TAB, "Rule Conditions", TAB, "Enabled", TAB, "Occurences", TAB, "Length", TAB, "Mute", TAB, "Notification Type", TAB, "Email Subject", TAB, "Destination Email Addresses", TAB, "DD Priority")
    data = r.json()['_embedded']['orchestrationRules']
    for i in data:
        notification_type = ""
        email_subject = ""
        email_destination = ""
        sns_topic = ""
        dd_priority = ""
        mute_time = ""
        if i['action'] == "notification":
                for z in i['actionParameters']:
                    if z['key'] == "notificationType":
                        notification_type = z['value']
                        if notification_type == "SES":
                            if "" in {email_subject, notification_type, email_destination}:
                                for x in i['actionParameters']:
                                    if x['key'] == "emailSubject":
                                        email_subject = x['value']
                                    elif x['key'] == "emailDestination":
                                        email_destination = x['value']
                            else:
                                break
                        elif notification_type == "SNS":
                            for x in i['actionParameters']:
                                if x['key'] == "topic":
                                    sns_topic = x['value']
                                    break
                        elif notification_type == "Datadog":
                            for x in i['actionParameters']:
                                if x['key'] == "ddPriority":
                                    dd_priority = x['value']
                                    break
        elif i['action'] == "alarm":
            for z in i['actionParameters']:
                if z['key'] == "mute":
                    mute_time = z['value']
                    break
        print(i['name'], TAB, i['description'], TAB, i['action'], TAB, i['matchRule'], TAB, i['enabled'], TAB, i['occurrences'], TAB, i['length'], TAB, mute_time, TAB, "SES"==notification_type and "Email" or notification_type, TAB, email_subject, TAB, email_destination, TAB, dd_priority)
else:
    print("ERROR: Request status = " + str(r.status_code))



