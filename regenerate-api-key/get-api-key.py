import requests
import sys

# auth endpoint for USM ANYWHERE
USMA_API_TOKEN_EP = '/api/2.0/oauth/token?grant_type=client_credentials'
# auth endpoint for USM CENTRAL
USMC_API_TOKEN_EP = '/api/1.1/oauth/token?grant_type=client_credentials'


# Parses API KEY from RESPONSE JSON
def get_api_key_from_response(response):
    data = response.json()
    return data['access_token']


# Gets API KEY for USMA
def get_usma_api_key(domain, user, psswd):
    url = domain + USMA_API_TOKEN_EP

    try:
        r = requests.post(url, auth=(user, psswd))
    except:
        return "ERROR: With Request"

    try:
        r.raise_for_status()
        return get_api_key_from_response(r)
    except requests.exceptions.HTTPError as e:
        # Response code is not 200
        return "Error: " + str(e)


# Gets API KEY for USMC
def get_usmc_api_key(domain, user, psswd):
    url = domain + USMC_API_TOKEN_EP

    try:
        r = requests.post(url, auth=(user, psswd))
    except:
        return "ERROR: With Request"

    try:
        r.raise_for_status()
        return get_api_key_from_response(r)
    except requests.exceptions.HTTPError as e:
        # Response code is not 200
        return "Error: " + str(e)



