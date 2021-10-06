These scripts will export the Rules in TSV format.

**Requirements:**

- USM Anywhere Subdomain
- API Client User & Password - https://cybersecurity.att.com/documentation/usm-anywhere/user-guide/user-management/api-clients.htm
- Python3 installed


**How to use functions.**

Instantiate the get-api-key in your script.

Call the function for your product and assign the returned value to your API key variable. In the example below im using the USM Anywhere function.
On the command line move to the location of the script and run the script

	api_key = get_usma_api_key("https://<subdomain>.alienvault.cloud", "user", "secret")

**Result**

The functions return output is just the parsed api key like below unless an exception occured.

	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiYWxpZW52YXVsdCJdLCJzY29wZSI6WyJ0cnVzdCIsInJlYWQiLCJ3cml0ZSJdLCJleHAiOjE2MzM1MTQ1MzUsImF1dGhvcml0aWVzIjpbIlJPTEVfbXNzcCIsIlJPTEVfbWFuYWdlciJdLCJqdGkiOiJlMzVhNjgxNy0xYzQ0LTRjZTctYWNhNy02OTc3ZDc2M2YxODYiLCJjbGllbnRfaWQiOiJha2VsbHkifQ.akGlfy-D6Tmy5m_0TpF-pmfwiBeymW0UsFsa5WidaCI


