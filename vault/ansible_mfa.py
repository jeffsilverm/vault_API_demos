
#
import subprocess
import sys

import hvac


class AnsibleMFA(object):

    def __init__(self) -> None:
        self.was_started_already = True
        self.values = dict()

    def daemon_running(self) -> bool:
        self.was_started_already = False
        return True

    def is_initialized(self) -> bool:
        # root token, keys go in session

        return True

    def initialize(self, keys=1, threshold=1) -> None:
        pass

    def is_sealed(self) -> bool:
        return True

    def add_secret(self, key, value) -> None:
        print("Do not use add_secret for any kind of production!!!", file=sys.stderr)
        self.values[key] = value

    def get_secret(self, key) -> object:
        print("Do not use get_secret for any kind of production!!!", file=sys.stderr)
        return self.values[key]

    def unseal(self) -> None:
        pass

    def seal(self) -> None:
        pass

    def stop_daemon(self) -> None:
        pass
