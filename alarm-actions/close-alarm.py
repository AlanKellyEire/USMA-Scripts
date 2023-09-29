import requests
import sys

headers = {'X-Xsrf-Token': '',}
cookies = {'JSESSIONID': ''}

json_data = {
    'status': 'CLOSED',
    'alarms': [],
    'route': [
    ],
}

def help():
    print("Script usage:")
    print("python3 close-alarm.py <SUBDOMAIN> <JSESSIONID> <XSRF-TOKEN> <ALARM_UUID>")
    print("Example usage:")
    print("python3 close-alarm.py https://subdomain.alienvault.cloud node065fwtf39oe9dxcxvu1j8v50k54987.node0 d5f7b5dd-f809-4c39-b3f5-7cfca7bedfd1 37097b31-7ad7-a4d6-68f5-022ef738a61f")

if len(sys.argv) != 5:
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

url = sys.argv[1]
cookies['JSESSIONID'] = str(sys.argv[2])
headers['X-Xsrf-Token'] = str(sys.argv[3])
json_data['alarms'].append(str(sys.argv[4]))


try:
    r = requests.put(f'{url}/api/2.0/security/alarms/status', cookies=cookies, headers=headers, json=json_data, verify=False, )
except:
    print("ERROR: With Request")
    exit(2)

if r.status_code != 200 :
    print("ERROR: Request status code = " + str(r.status_code))
