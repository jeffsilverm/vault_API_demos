#! /usr/bin/env python3
#
# Test the ansible_mfa.py module
import sys

import pytest
from ansible_mfa import AnsibleMFA
import os


class TestAnsibleMFA:

    session = AnsibleMFA()
    if not session.is_daemon_running():
        print("The daemon isn't running so there is no point in continuing", file=sys.stderr)
        sys.exit(1)

    @pytest.mark.skip
    def test_is_daemon_running(self):
        global session
        try:
            if self.session.is_daemon_running():
                self.session.was_started_already = True
                self.session.stop_daemon()
            else:
                self.session.was_started_already = False
            assert not self.session.is_daemon_running(), "is_daemon_running() " \
                                                         "thinks the " \
                                                         "daemon is running, " \
                                                         "but test_daemon_running " \
                                                         "" \
                                                         "" \
                                                         "" \
                                                         "had called stop_daemon(" \
                                                         ") which " \
                                                         "should have stopped it. " \
                                                         "" \
                                                         "" \
                                                         "" \
                                                         " Either stop_daemon " \
                                                         "doesn't stop the " \
                                                         "daemon or else " \
                                                         "is_daemon_running() is " \
                                                         "wrong"
            session.start_daemon(url=AnsibleMFA.VAULT_ADDR,
                                      args=AnsibleMFA.DAEMON_ARGUMENTS)
            assert self.session.is_daemon_running(), "is_daemon_running() thinks " \
                "the daemon is not running, but test_daemon_running had called " \
                "start_daemon to start it.  Either is_daemon_running or else " \
                "start_daemon failed to start it.\n" \
                f"VAULT_ADDR is {AnsibleMFA.VAULT_ADDR} and args is " + \
                AnsibleMFA.DAEMON_ARGUMENTS
            self.session.was_started_already = True  # Since stop_daemon had
            # started it
        except NotImplementedError as n:
            print(f"NotImplemented was raised, {str(n)}. ", file=sys.stderr)


@pytest.fixture(scope='session')
def mfa_fixture():
    test_ansible_MFA: TestAnsibleMFA = TestAnsibleMFA()
    assert test_ansible_MFA.hasattr("session"), f"test_ansible_MFA does not have attribute session, and it should.\n{dir(test_ansible_MFA)}.\n"
    assert test_ansible_MFA.session.is_daemon_running(), "Immediately after instantiating TestAnsibleMFA, the daemon is not running"
    print("Immediately after instantiating TestAnsibleMFA, the daemon IS running", file=sys.stderr)
    return test_ansible_MFA

# ansible_mfa = AnsibleMFA()

def test___is_daemon_running(mfa_fixture) -> bool:
    # I want to just see if the daemon is running, I don't want to test
    # is_daemon_running because as of this writing (2022/12/11) it doesn't work.
    assert test_ansible_MFA.session.is_daemon_running(), "The vault daemon is not running"
    print ("The vault daemon IS running", file=sys.stderr)

# if "__main__" == __name__ or 'test_ansible_mfa' == __name__:
#    test___is_daemon_running()
