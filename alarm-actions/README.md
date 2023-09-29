This scripts will close an Alarm

**Requirements:**

- USM Anywhere Subdomain
- Cookie info: `JSESSIONID`
- Cookie info: `XSRF-TOKEN`
- Alarm UUID: [How to get Alarm UUID](https://cybersecurity.att.com/documentation/usm-anywhere/deployment-guide/admin/obtain-uid-info.htm)
- Python3 installed

**How to get** `JSESSIONID` and `XSRF-TOKEN` **.**

1. Login to the USM Anywhere instance in a Web Brower.
2. In this example I will use Firefox.
3. Open the developer tools ([https://developer.mozilla.org/en-US/docs/Tools](https://developer.mozilla.org/en-US/docs/Tools) ).
4. Once opened go to the network tab and refresh the page.
5. Click on any 200 request and select the cookies option.
6. Copy the `JSESSIONID` and `XSRF-TOKEN`.

**How to use scripts.**

Download script from here.

On the command line move to the location of the script and run the script

	python3 close-alarm.py <https://SUBDOMAIN.alienvault.cloud> <JSESSIONID> <XSRF-TOKEN> <ALARM_UUID>

Example

	python3 close-alarm.py https://demo.alienvault.cloud node0000aejchdef7n1eqnuobnt3lt00000.node0 d5f7b5dd-f809-4c39-b3f5-7cfca7bedfd1 37097b31-7ad7-a4d6-68f5-022ef738a61f