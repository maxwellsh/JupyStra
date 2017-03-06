# spawn_server.py - Spawn a Jupyter Notebook server on Orchestra
#
# v 0.0.1
# rev 2017-03-06 (MS: Created)
# Notes: 

import paramiko
import argparse
import getpass

class Spawner(object):
    """ A class for spanwing Jupyter notebook servers on Orchestra
    """

    client = None
    args = None
    password = None

    def __init__(self):
        self.args = self._parse_args()
        self.login = self.args.login_ID
        self.password = self._prompt_password()
        self._connect()

        self.run_addtn_cmds()

    def _prompt_password(self):
        password = getpass.getpass("Orchestra password: ")
        return password

    def _parse_args(self):
        parser = argparse.ArgumentParser(description="Launch a Jupyter notebook server on Orchestra")
        parser.add_argument('login_ID', type=str, help='your orchestra login ID')
        parser.add_argument('-p', '--port', type=str, default='8888', help='port on Orchestra which to start server')
        parser.add_argument('-L', '--local_port', type=str, default='8888', help='local port on which users connect to orchestra')
        parser.add_argument('--cmds', nargs='+', type=str, default=[], help='additional commands to run before launching the server')

        return parser.parse_args()

    def _connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('orchestra.med.harvard.edu', username=self.login, password=self.password)

        self.ssh = ssh

    def exec_cmd(self, cmd, verbose=True, output=False):
        if verbose:
            print("Executing: {}".format(cmd))

        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        if verbose:
            for line in stdout:
                print(line)

            for line in stderr:
                print(line)

        if output:
            return stdin, stdout, stderr

    def run_addtn_cmds(self):
        for cmd in self.args.cmds:
            self.exec_cmd(cmd)

if __name__ == "__main__":
    spawn = Spawner()
