These scripts will export the Users in TSV format.

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

	python3 export-users.py <https://SUBDOMAIN.alienvault.cloud> <JSESSIONID>

Example

	python3 export-users.py https://demo.alienvault.cloud node0000aejchdef7n1eqnuobnt3lt00000.node0

**Result**

The script should output the rules in TSV format like below.

	User 	 User Email 	 Role 	 Status 	 Enabled 	 MFA 	 Account Locked
    Tom 	 tom@secure-mssp.com 	 readOnly 	 Enabled 	 Disabled 	 NO
    Mary 	 mary@gotham.com.au 	 Manager 	 Enabled 	 Enabled 	 NO
    Billy 	 billy@mycompany.ie 	 readOnly 	 Enabled 	 Disabled 	 YES

This can then be imported into excel or whatever tool you want to use to analyse or backup the rules.
