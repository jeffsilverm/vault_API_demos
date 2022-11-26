# /usr/bin/exec python3
#
#

from ansible_mfa import AnsibleMFA
import random

KEYS = 5
THRESHOLD = 5


def main():
    # This program implements a complete implementation of the ansible MFA system

    session = AnsibleMFA()

    if not session.daemon_running():
        session.start_daemon()

    if not session.is_initialized():
        # root token, keys go in session
        session.initialize(keys=KEYS, threshold=THRESHOLD)

    if session.is_sealed():
        session.unseal()

    key = random.randint(0, 1000)
    value = random.randbytes(8)
    session.add_secret(key=key, value=value)

    decoded_secret = session.get_secret(key=key)
    assert value == decoded_secret, f"the value was {value} but the decoded_secret was {decoded_secret}"

    session.seal()

    if not session.was_started_already:
        session.stop_daemon()


if "__main__" == __name__:
    main()
