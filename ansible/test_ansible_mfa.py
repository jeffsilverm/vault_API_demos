#! /usr/bin/env python3
#
# Test the ansible_mfa.py module

# import pytest
from ansible_mfa import AnsibleMFA
import os


class TestAnsibleMFA:

    def __init__(self):
        mfa = AnsibleMFA()
        self.session = mfa

    def test_daemon_running(self):
        self.session.stop_daemon()
        self.session.was_started_already = False     # Since stop_daemon had stopped it
        assert not self.session.is_daemon_running(), "is_daemon_running() thinks the " \
               "daemon is running, but test_daemon_running had stopped it"
        self.session.start_daemon(url=AnsibleMFA.VAULT_ADDR, args=AnsibleMFA.DAEMON_ARGUMENTS )
        assert self.session.is_daemon_running(), "is_daemon_running() thinks the " \
               "daemon is not running, but test_daemon_running had started it"
        self.session.was_started_already = True     # Since stop_daemon had started it


test_ansible_MFA = TestAnsibleMFA()
test_ansible_MFA.test_daemon_running()
