#! /usr/bin/python3
#
# Demonstration interface to vault APIs
#
import sys
import hvac
import urllib3
import requests

# Test that environment is working
# print(f"Executing {sys.version_info} and have hvac at {hvac.__file__} and urllib3 at {urllib3.__file__}", file=sys.stderr)

# The contents of expeditors/pyvenv.cfg
# home = /usr/bin
# include-system-site-packages = true
# version = 3.10

# Make this more sophisticated - look at the VAULT_URL environmental variable
URL = "https://localhost:8200"

class VaultExceptions(Exception):
    pass

def initialize(url: str) -> hvac.Client :
    # Return a client that has been authenticate
    client = hvac.Client(url=url)
    if client.is_authenticated():
        return client
    raise VaultExceptions("Client failed to authentication")

if "__main__" == __name__:
    try:
        initialize(url=URL)
    except requests.exceptions.ConnectionError as e:
        print("initialize failed to connect to the vault using URL {URL}.  Error is {e}", file=sys.stderr)
    except VaultExceptions:
        print("Initial did connect to the vault but did not authenticate")





