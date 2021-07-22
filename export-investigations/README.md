These scripts will export the Rules in TSV format.

**Requirements:**

- USM Anywhere Subdomain
- Cookie info: `JSESSIONID`
- Python3 installed

**How to get** `JSESSIONID` **.**

1. Login to the USM Anywhere instance in a Web Brower.
2. In this example I will use Firefox.
3. Open the developer tools ([https://developer.mozilla.org/en-US/docs/Tools](https://developer.mozilla.org/en-US/docs/Tools) ).
4. Once opened go to the network tab and refresh the page.
5. Click on any 200 request and select the cookies option.
6. Copy the `JSESSIONID`.

**How to use scripts.**

Download script from here.

On the command line move to the location of the script and run the script

	python3 export-investigations.py <https://SUBDOMAIN.alienvault.cloud> <JSESSIONID>

Example

	python3 export-investigations.py https://demo.alienvault.cloud node0000aejchdef7n1eqnuobnt3lt00000.node0

**Result**

The script should output the rules in TSV format like below.

	Title 	 ID 	 Severity 	 Status 	 Intent 	 Created 	 Assignee 	 Last Updated 	 Last Updated By 	 UUID
	Malware Infection Investigation 	 1 	 High 	 Closed 	 System Compromise 	 2021-03-31 22:05:45.834 	 john@att.com 	 2021-06-23 22:04:41.710 	 tom@att.com 	 3e71dfea-cb07-0e7e-5eff-1b796c367ea2
	DDoS Attack 	 2 	 High 	 Open 	 Exploitation & Installation 	 2021-07-01 21:34:30.214 	 tom@att.com 	 2021-07-01 21:34:30.434 	 john@att.com 	 f3ed70e5-5094-b897-ce33-dcafb15a5ee3
	Mi Investigacion 	 3 	 Medium 	 Open 	 Exploitation & Installation 	 2021-07-08 16:38:37.722 	 tom@att.com 	 2021-07-08 16:39:59.281 	 john@att.com 	 74391b63-2915-a617-11c9-19fd94100d1


This can then be imported into excel or whatever tool you want to use to analyse or backup the rules.
