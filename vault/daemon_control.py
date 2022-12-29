#! /usr/bin/env python3
#
# This class provides control for the daemon.  Ordinarily, it won't be needed,
# the daemon will already be running.  But for development, it might be because
# the daemon will need to be reconfigured.

# Review PEP 3143 Standard daemon process library.
# https://peps.python.org/pep-3143/
import daemon
import sys

class DaemonControl(object):

    daemon_pid = 0

    def __init__(self):
        pass

    def start_daemon(self, config_file_name: str, options: list) -> None:
        # Returns the process identifier (PID) of the created daemon file

        self.daemon_pid = 1
        daemon_context = daemon.DaemonContext()
        print(dir(daemon_context), file=sys.stderr)
        pass

    def is_daemon_running(self, port):
        return self.daemon_pid >= 1

    def stop_daemon(self, pid_filename):
        self.daemon_pid = 0


if "__main__"  == __name__ :
    print("Instantiating the daemon object")
    d_obj = DaemonControl()
    print(f"The daemon {'IS' if d_obj.is_daemon_running(port=7) else 'is NOT'} running")
    print("Starting the daemon", file=sys.stderr)
    d_obj.start_daemon(config_file_name="?", options=[])
    print(f"The daemon {'IS' if d_obj.is_daemon_running(port=7) else 'is NOT'} running")
    print("Stopping the daemon")
    d_obj.stop_daemon(pid_filename="fg")
    print(f"The daemon {'IS' if d_obj.is_daemon_running(port=7) else 'is NOT'} running")





