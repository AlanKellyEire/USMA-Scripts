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

	python3 <script.py> <https://SUBDOMAIN.alienvault.cloud> <JSESSIONID>

Example

	python3 download-correlation-rules.py https://demo.alienvault.cloud node0000aejchdef7n1eqnuobnt3lt00000.node0

**Result**

The script should output the rules in TSV format like below.

	Rule_Name 	 Rule Description 	 Rule Type 	 Rule Conditions 	 Mute 	 Strategy 	 Method
	AWSGuardDuty_Backdoor_EC2_Spambot 	 The machine has increased the traffic on port 25, reserved for Simple Mail Transfer Protocol (SMTP). This is a clear indicator of SPAM bot infection. If the machine is compromised, it might be sending out SPAM mails. 	 Correlation Alarm Rule 	 ["plugin_device == 'GuardDuty' and\n                rep_device_rule_id == 'Backdoor:EC2/Spambot' and source_canonical >> [source]"] 	 ['1h'] 	 Suspicious Behavior 	 Possible SPAM Traffic
	AWSGuardDuty_Backdoor_EC2_CNC_Activity.B.DNS 	 There is an EC2 instance in your AWS environment that is querying a domain name associated with a known command and control server. 	 Correlation Alarm Rule 	 ["plugin_device == 'GuardDuty' and\n                (rep_device_rule_id == 'Backdoor:EC2/C&CActivity.B!DNS' or rep_device_rule_id == 'Backdoor:EC2/C&CActivity.B')and source_canonical >> [source]"] 	 ['1h'] 	 C&C Communication 	 Known command and control server



This can then be imported into excel or whatever tool you want to use to analyse or backup the rules.


