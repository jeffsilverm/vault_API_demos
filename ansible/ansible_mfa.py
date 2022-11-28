#
import subprocess
import sys

import hvac
import psutil
import signal
from typing import List
import os


class AnsibleMFA(object):
    VAULT_ADDR = os.environ.get('VAULT_ADDR',
                                "https://localhost:8200")  # where to find the
    # vault server
    VAULT_CA_CERT = os.environ.get('VAULT_CA_CERT',
                                   None)  # A trustworthy cert by definition
    VAULT_CLIENT_CERT = os.environ.get('VAULT_CLIENT_CERT',
                                       None)  # Public key - give to the client
    VAULT_CLIENT_KEY = os.environ.get('VAULT_CLIENT_KEY',
                                      None)  # Private key - stays in the
    # server!
    VAULT_TOKEN = os.environ.get('VAULT_TOKEN', None)
    DAEMON_ARGUMENTS = ["-config=tls_config.hcl"]

    def __init__(self) -> None:
        self.was_started_already = True  # Assume that the server is already
        # started
        scheme, laddr = self.VAULT_ADDR.split("//")
        addr, port = laddr.split(":")
        # we will need this in stop_daemon, to make sure we are killing the
        # correct daemon
        self.local_addr = psutil._common.addr(ip=addr, port=port)
        self.values = dict()
        self.client = None

    def is_daemon_running(self) -> bool:
        # Is the daemon running?  Find out by trying to connect to it.  If the
        # the connection succeeds, then the daemon is already running: set
        # was_started_already to True and return.  If the connection fails,
        # then the daemon is not running, then set the was_started_already
        # to False and return.
        # It is the caller's responsibility to call start_daemon if needed.
        #
        # This function has a side effect: if the daemon is running, then
        # there is state in self

        # From https://hvac.readthedocs.io/en/stable/source/hvac_v1.html
        try:
            self.client = hvac.Client(url=self.VAULT_ADDR)
        except Exception as e:
            print("In is_deamon_running, an exception was raised:\n " \
                f"\n{str(e)}\nContinuiong (for now)",
                file=sys.stderr)
            return False
        else:
            return True

    def is_initialized(self) -> bool:
        # root token, keys go in session

        return True

    def initialize(self, keys=1, threshold=1) -> None:
        pass

    def is_sealed(self) -> bool:
        return True

    def add_secret(self, key, value) -> None:
        print("Do not use add_secret for any kind of production!!!",
              file=sys.stderr)
        self.values[key] = value

    def get_secret(self, key) -> object:
        print("Do not use get_secret for any kind of production!!!",
              file=sys.stderr)
        return self.values[key]

    def unseal(self) -> None:
        pass

    def seal(self) -> None:
        pass

    def stop_daemon(self) -> None:
        # This stops any running vault daemon.  This assumes that the daemon
        # is running on the same computer as this program

        # See https://github.com/giampaolo/psutil/blob/master/README.rst
        my_euid: int = psutil.Process(pid=None).uids().effective
        pid_list: Iterator[Process] = psutil.process_iter(['uids', 'exe'])
        for pid_obj in pid_list:
            daemon_euid = pid_obj.uids().effective
            # Going to be hard to stop the daemon if it's not in the same UID
            # as I am.
            assert isinstance(daemon_euid, int)
            assert isinstance(my_euid, int)
            if daemon_euid != my_euid:
                continue
            # pcl = process connection list. "tcp" -> TCP w/both IPv4 and IPv6
            try:
                pcl: List = pid_obj.connections(kind="tcp")
            except psutil.AccessDenied as pA:
                print(f"Access denied.  My EUID is {my_euid}. "
                      f"The daemon EUID is {daemon_euid}. "
                      f"The rest of the pid_obj is {pid_obj}. ",
                      file=sys.stderr)
                # There may be several reasons why a process has denied access.
                continue
            # If there are no connections from this process, then it cannot be
            # the daemon I am looking for.  So skip it and try the next one.
            if len(pcl) == 0:
                continue
            for conn in pcl:
                if self.local_addr == conn.laddr:
                    print(f"preparing to kill PID {pid.pid} running {pid.exe()}"
                          f"command line {pid.cmdline()} listening on "
                          f"{conn.laddr}",
                          file=sys.stderr)
                    # This is the equivalent to sending control-C.  The vault
                    # daemon will need some time to shut down clearly
                    pid.send_signal(sig=signal.SIGINT)
                    # In a future version, if the vault daemon won't shut down
                    # in a "reasonable" amount of time, then terminate it.
                    break
            else:
                print("Did not kill any daemons.  Perhaps none are running",
                      file=sys.stderr)
        print("Exiting from stop_daemon", file=sys.stderr)

    def start_daemon(self, url: str, args: List[str]):

        assert isinstance(args, list), \
            f"args should be a list but it's really a {type(args)}."
        args = ["vault", "server", url] + args
        try:
            print(f"Starting the daemon with {args}", file=sys.stdout )
            # subprocess.run is recommended after python 3.5
            # env takes a mapping type, os.environ is a map.  This allows the
            # child to get the
            # full environment set of the parent.  It might not be necessary
            results = subprocess.run(args=args, shell=False,
                                     capture_output=True, check=True,
                                     env=os.environ)
            output = results.stdout
        except subprocess.CalledProcessError as c:
            print("subprocess.run failed with subprocess.CalledProcessError "
                  f"exception {c}.\n args is {args}.\n", file=sys.stderr)

            returncode = c.returncode
            cmd = c.cmd
            output = c.output
            print(f"Return code was {returncode}, command was {cmd} "
                  f" and output was \n{output}\n", file=sys.stderr)
            # other exceptions are possible, but I am not going to handle
            # them, just raise them.
        return output
