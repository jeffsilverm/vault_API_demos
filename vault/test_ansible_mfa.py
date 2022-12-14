#! /usr/bin/env python3
#
# Test the ansible_mfa.py module
import sys

import pytest
from ansible_mfa import AnsibleMFA
import os


class TestAnsibleMFA:

    self.session = AnsibleMFA()

    def test_start_stop_daemon(self) -> None:
        try:
            if self.session.is_daemon_running():
                self.session.was_started_already = True
                self.session.stop_daemon()
            else:
                self.session.was_started_already = False
            assert not self.session.is_daemon_running(), "is_daemon_running() " \
                "thinks the daemon is running, but test_start_stop_daemon " \
                "had called stop_daemon() which should've stopped the daemon."\
                "Either stop_daemon doesn't stop the daemon or else" \
                "is_daemon_running() is wrong"
            self.session.start_daemon(url=AnsibleMFA.VAULT_ADDR,
                                      args=AnsibleMFA.DAEMON_ARGUMENTS)
            assert self.session.is_daemon_running(), "is_daemon_running() thinks " \
                "the daemon is not running, but test_daemon_running had called " \
                "start_daemon to start it.  Either is_daemon_running is wrong " \
                "or else start_daemon failed to start it.\n" \
                f"VAULT_ADDR is {AnsibleMFA.VAULT_ADDR} and args is " + \
                f" {session.args}."
            self.session.was_started_already = True  # Since stop_daemon had
            # started it
        except NotImplementedError as n:
            print(f"NotImplemented was raised, {str(n)}.  Method start_daemon isn't implemented", file=sys.stderr)


@pytest.fixture(scope='session')
def mfa_fixture():
    test_ansible_MFA: testAnsibleMFA = TestAnsibleMFA()
    test_ansible_MFA.session = AnsibleMFA()
    assert test_ansible_MFA.session.is_daemon_running(),\
        "The daemon is NOT running."
    print("The daemon IS running", file=sys.stderr)
    return test_ansible_MFA

# ansible_mfa = AnsibleMFA()

# def test___is_daemon_running(self) -> bool:
#    # I want to just see if the daemon is running, I don't want to test
#    # is_daemon_running because as of this writing (2022/12/11) it doesn't work.
#    assert self.session.is_daemon_running(), "The vault daemon is not running"
#    print ("The vault daemon IS running", file=sys.stderr)

# if "__main__" == __name__ or 'test_ansible_mfa' == __name__:
#    test___is_daemon_running()
