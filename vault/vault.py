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
URL = "http://localhost:8200"

class VaultExceptions(Exception):
    pass

def main():
    global client
    try:
        client = authenticate(url=URL)
    except requests.exceptions.ConnectionError as e:
        print(f"initialize failed to connect to the vault using URL {URL}.  Error is {e}", file=sys.stderr)
    except VaultExceptions:
        print("Initialize did connect to the vault but did not authenticate")

    keys = initialize(shares=5, threshold=3)

    key_num = 0
    while client.sys.is_sealed():
        unseal_response = client.sys.submit_unseal_key(keys[key_num])
        print(f"Unseal response is {unseal_response}")

    print("Read and write secrets here", file=sys.stderr)

    print(f"About to seal the client: client.sys.is_sealed() is {client.sys.is_sealed()}")
    client.sys.seal()
    print(f"The client is sealed: client.sys.is_sealed() is {client.sys.is_sealed()}")
    return 0



def authenticate(url: str) -> hvac.Client :
    # Return a client that has been authenticate
    _client = hvac.Client(url=url)
    if _client.is_authenticated():
        return _client
    raise VaultExceptions("Client failed authentication")

def initialize( shares: int = 5, threshold: int = 3):
    assert shares >= threshold, f"shares {shares} must not be < threshold {threshold}"
    global client
    if client.sys.is_initialized():
        print("The vault is already initialized", file=sys.stderr)
    else:
        result = client.sys.initialize(secret_shares=shares, secret_threshold=threshold)
        if not client.sys.is_initialized():
            raise VaultExceptions("The server failed to initialize")
        root_token = result['root_token']
        _keys = result['keys']
        client.token = root_token
    print(f"The type of keys is {type(_keys)} . ", file=sys.stderr)
    return _keys



if "__main__" == __name__:
    main()





