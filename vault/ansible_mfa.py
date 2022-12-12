#
import subprocess
import sys
import socket

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
    VAULT_EXECUTABLE = "/usr/local/bin/vault"       # You could also use shutil.which() to locate vault at run-time

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
        # Is the responsibility of the sysadmin to verify that the vault
        # daemon is connected to the port.  If something else is listening
        # on the port, then there will be strange and hard-to-troubleshoot
        # errors.
        try:
# Calling hvac.Client is not a reliable way to determine that the server
# is running.
# From https://hvac.readthedocs.io/en/stable/source/hvac_v1.html
#            self.client = hvac.Client(url=self.VAULT_ADDR)
            s = socket.socket()
            s.connect((self.local_addr.ip, int(self.local_addr.port)))
            return True
        except ConnectionRefusedError as e:
            print(f"Failed to connect to {self.local_addr.ip} "\
                    f"TCP port {self.local_addr.port} "+e.strerror, file=sys.stderr)
            return False
        # finally is seldom used.  It **always** executes, even if one of the
        # execpt or else blocks returns.
        finally:
            s.close()




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
        # Start the vault daemon.
        # This is getting complicated, and I am beginning to think that
        # must be a simpler way.
        assert isinstance(args, list), \
            f"args should be a list but it's really a {type(args)}."
        # The URL must come last.
        # Command flags must be provided before positional arguments.
        # Run vault in the background.
        arg_list = [self.VAULT_EXECUTABLE, "server"] + args + [ url, "&"]
        raise NotImplemented(f"Start the daemoin with the command\n{' '.join(arg_list)}\nin another terminal window")
        try:
            print(f"Starting the daemon with {' '.join(arg_list)}", file=sys.stderr )
            # subprocess.run is recommended after python 3.5
            # env takes a mapping type, os.environ is a map.  This allows the
            # child to get the full environment set of the parent.  It might
            # not be necessary.  Since the vault program is a daemon, use the
            # shell to run it in background.  Maybe I should use pexpect?
            results = subprocess.Popen(args=arg_list, shell=True,
                                       capture_output=True, check=True,
                                       stdout=PIPE, stderr=PIPE,
                                       env=os.environ)
        except subprocess.CalledProcessError as c:
            print("subprocess.run failed with subprocess.CalledProcessError "
                  f"exception {c}.\n arg_list is {arg_list}.\n"
                  f"return code is {c.returncode} \n"
                  f"stdout is {c.stdout}\nstderr is {c.stderr} \n\n",
                  f"The command was {c.cmd}", file=sys.stderr)
            raise
        try:
            output, errors = results.communicate(timeout=10)
        except TimeoutExpired:
            print
        return output
