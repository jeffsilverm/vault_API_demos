#! /usr/bin/python3
#
# Demonstration interface to vault APIs
#
import sys
import os
import hvac
# import urllib3
import requests
from pprint import PrettyPrinter

# Test that environment is working
# print(f"Executing {sys.version_info} and have hvac at {hvac.__file__} and urllib3 at {urllib3.__file__}", file=sys.stderr)

# The contents of expeditors/pyvenv.cfg
# home = /usr/bin
# include-system-site-packages = true
# version = 3.10

pp = PrettyPrinter(depth=2)
# There's gotta be more sophisticate ways of dealing with missing envars
URL = os.environ.get('VAULT_URL', "https://localhost:8200")
CA_CERT = os.environ.get('VAULT_CA_CERT', None)
CLIENT_CERT = os.environ.get('VAULT_CLIENT_CERT', None)
CLIENT_KEY = os.environ.get('VAULT_CLIENT_KEY', None)
VAULT_TOKEN = os.environ.get('VAULT_TOKEN', None)


class VaultExceptions(Exception):
    pass
class VaultRanOutOfKeys(Exception):
    pass


def main():
    try:
        client_: hvac.Client = authenticate(url=URL, vault_token=VAULT_TOKEN,
                                            client_cert_path=CLIENT_CERT,
                                            client_key_path=CLIENT_KEY,
                                            server_cert_path=CA_CERT)

    except requests.exceptions.ConnectionError as e:
        print(
            "initialize failed to connect to the vault server using URL"
            f" {URL}. Error is {e}.  Perhaps the server is not running.",
            file=sys.stderr)
        raise
    except VaultExceptions as e:
        print(f"Did connect to the vault but did not authenticate {e}")
        client_ = hvac.Client(url=URL)
    pp.pprint(client_)
    if not is_initialized():
        keys = initialize(client_, shares=5, threshold=3)
        if keys is None:
        # Generate new keys using one of the rekey? methods
            print(f"This database is not initialized and initialize returned"
                  f"no keys", file=sys.stderr)
    key_num = 0
    while client_.sys.is_sealed():
        unseal_response = client_.sys.submit_unseal_key(keys[key_num])
        print(f"Key {key_num}: Unseal response is {unseal_response}")
        if key_num >= len(keys):
            print(f"Run out of keys {key_num}, there are {len(keys)} available")
            raise VaultRanOutOfKeys("Ran out of keys.  Are you **sure** you are who you claim to be?")

    print("Read and write secrets here", file=sys.stderr)
    client_.sys.unseal()
    print(f"About to seal the client_: client_.sys.is_sealed() is {client_.sys.is_sealed()}")
    client_.sys.seal()
    print(f"The client_ is sealed: client_.sys.is_sealed() is {client_.sys.is_sealed()}")
    return 0


def authenticate(url: str, vault_token, client_cert_path=None, client_key_path=None,
                 server_cert_path=None) -> hvac.Client:
    # Return a client that has been authenticated

    if "https://" in url.lower():
        _client = hvac.Client(url=url,
                              token=vault_token,
                              cert=(client_cert_path, client_key_path),
                              verify=server_cert_path)
    elif "http://" in url.lower():
        _client = hvac.Client(url=url)
    else:
        raise VaultExceptions(f"I don't think the URL is correct {url}")
    if _client.is_authenticated():
        return _client
    raise VaultExceptions("Client failed authentication")

def initialize(client: hvac.Client, shares: int = 5, threshold: int = 3):
    # I think normally, you'd want to do the initialization on the server, not on the
    # client.
    assert shares >= threshold, f"shares {shares} must not be < threshold {threshold}"

    if client.sys.is_initialized():
        print("The vault is already initialized, continuing", file=sys.stderr)
        _keys = None   # NEVER return the keys.  They're private keys.
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


# >>> print("\n".join(dir(client.sys)))
# __class__
# __delattr__
# __dict__
# __dir__
# __doc__
# __eq__
# __format__
# __ge__
# __getattr__
# __getattribute__
# __gt__
# __hash__
# __init__
# __init_subclass__
# __le__
# __lt__
# __metaclass__
# __module__
# __ne__
# __new__
# __reduce__
# __reduce_ex__
# __repr__
# __setattr__
# __sizeof__
# __str__
# __subclasshook__
# __weakref__
# _adapter
# adapter
# calculate_hash
# cancel_rekey
# cancel_rekey_verify
# cancel_root_generation
# create_namespace
# create_or_update_policy
# delete_namespace
# delete_policy
# disable_audit_device
# disable_auth_method
# disable_secrets_engine
# enable_audit_device
# enable_auth_method
# enable_secrets_engine
# force_restore_raft_snapshot
# generate_root
# get_capabilities
# get_encryption_key_status
# get_private_attr_name
# implemented_classes
# initialize
# is_initialized
# is_sealed
# join_raft_cluster
# list_auth_methods
# list_enabled_audit_devices
# list_leases
# list_mounted_secrets_engines
# list_namespaces
# list_policies
# move_backend
# read_auth_method_tuning
# read_backup_keys
# read_health_status
# read_init_status
# read_leader_status
# read_lease
# read_mount_configuration
# read_policy
# read_raft_config
# read_rekey_progress
# read_rekey_verify_progress
# read_root_generation_progress
# read_seal_status
# rekey
# rekey_multi
# rekey_verify
# rekey_verify_multi
# remove_raft_node
# renew_lease
# restore_raft_snapshot
# retrieve_mount_option
# revoke_force
# revoke_lease
# revoke_prefix
# rotate_encryption_key
# seal
# start_rekey
# start_root_token_generation
# step_down
# submit_unseal_key   <=================== how to unseal!
# submit_unseal_keys
# take_raft_snapshot
# tune_auth_method
# tune_mount_configuration
# unimplemented_classes
# unwrap
# >>>
# >>> print("\n".join(dir(client))
# ... )
# __class__
# __delattr__
# __dict__
# __dir__
# __doc__
# __eq__
# __format__
# __ge__
# __getattr__
# __getattribute__
# __gt__
# __hash__
# __init__
# __init_subclass__
# __le__
# __lt__
# __module__
# __ne__
# __new__
# __reduce__
# __reduce_ex__
# __repr__
# __setattr__
# __sizeof__
# __str__
# __subclasshook__
# __weakref__
# _adapter
# _auth
# _secrets
# _sys
# adapter
# allow_redirects
# auth
# auth_cubbyhole
# delete
# generate_root_status
# get_policy
# ha_status
# is_authenticated
# key_status
# list
# login
# logout
# lookup_token
# read
# rekey_status
# renew_token
# revoke_token
# seal_status
# secrets
# session
# sys
# token
# url
# write
# >>>
