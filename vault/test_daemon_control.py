from daemon_control import DaemonControl
class TestDaemonControl(object):

    daemon_obj = DaemonControl()
    assert daemon_obj.daemon_pid == 0

    def test_start_daemon(self):
        self.daemon_obj.start_daemon(config_file_name = "", options = [])
        assert self.daemon_obj.daemon_pid == 1

    def test_is_daemon_running(self, port="anything"):
        assert self.daemon_obj.is_daemon_running(port=port)

    def test_stop_daemon(self):
        self.daemon_obj.stop_daemon(pid_filename="?")
        assert self.daemon_obj.daemon_pid == 0
