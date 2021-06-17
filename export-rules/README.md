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

python3 \&lt;download-correlation-rules.py\&gt; \&lt;https://SUBDOMAIN.alienvault.cloud\&gt; \&lt;JSESSIONID\&gt;

Example

python3 download-correlation-rules.py https://avsolardemo.alienvault.cloud node0183aejchdef7n1eqnuobnt3lt75256.node0

**Result**

The script should output the rules in TSV format like below.

Rule\_Name Rule Description Rule Type Rule Conditions Mute Strategy Method

AWSGuardDuty\_Backdoor\_EC2\_Spambot The machine has increased the traffic on port 25, reserved for Simple Mail Transfer Protocol (SMTP). This is a clear indicator of SPAM bot infection. If the machine is compromised, it might be sending out SPAM mails. Correlation Alarm Rule [&quot;plugin\_device == &#39;GuardDuty&#39; and\n rep\_device\_rule\_id == &#39;Backdoor:EC2/Spambot&#39; and source\_canonical \&gt;\&gt; [source]&quot;] [&#39;1h&#39;] Suspicious Behavior Possible SPAM Traffic

AWSGuardDuty\_Backdoor\_EC2\_CNC\_Activity.B.DNS There is an EC2 instance in your AWS environment that is querying a domain name associated with a known command and control server. Correlation Alarm Rule [&quot;plugin\_device == &#39;GuardDuty&#39; and\n (rep\_device\_rule\_id == &#39;Backdoor:EC2/C&amp;CActivity.B!DNS&#39; or rep\_device\_rule\_id == &#39;Backdoor:EC2/C&amp;CActivity.B&#39;)and source\_canonical \&gt;\&gt; [source]&quot;] [&#39;1h&#39;] C&amp;C Communication Known command and control server

This can then be imported into excel or whatever tool you want to use to analyse or backup the rules.