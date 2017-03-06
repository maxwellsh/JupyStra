# spawn_server.py - Spawn a Jupyter Notebook server on Orchestra
#
# v 0.0.3
# rev 2017-03-06 (MS: Server job submission and pinging for RUN status)
# Notes: 

import paramiko
import argparse
import getpass
import time
import re

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
        self.submit_server_job()
        self.get_exec_host()

    def _prompt_password(self):
        password = getpass.getpass("Orchestra password: ")
        return password

    def _connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('orchestra.med.harvard.edu', username=self.login, password=self.password)

        self.ssh = ssh

    def exec_cmd(self, cmd, verbose=True, output=False):
        if verbose:
            print("Executing: {}".format(cmd))

        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        for line in stderr:
            print(line)

        if verbose:
            for line in stdout:
                print(line)

        if output:
            return stdin, stdout, stderr

    def run_addtn_cmds(self):
        for cmd in self.args.cmds:
            self.exec_cmd(cmd)

    def submit_server_job(self):
        kwargs = { 'queue': self.args.queue,
                   'walltime': self.args.wall_time,
                   'outfile': self.args.outfile,
                   'port_jup': self.args.port
                 }

        cmd = """bash -l -c "bsub -q {queue} -W {walltime} -o {outfile} 'jupyter notebook --port={port_jup} --browser="none" '" """.format(**kwargs)

        stdin, stdout, stderr = self.exec_cmd(cmd, verbose=False, output=True)
        out = stdout.read().decode('utf-8')

        'job <JOBID> submitte to queue QUEUE'
        self.jobID = out.split()[1].split('<')[1].split('>')[0]

    def get_exec_host(self):
        # Ensure job is running
        self.ping_job()
        
        stdin, stdout, stderr = self.exec_cmd('bash -l -c "bjobs -w {}"'.format(self.jobID), verbose=False, output=True)

        # only interested in the second line
        stdout.readline()
        out = stdout.readline()
        self.exec_host = out.split()[5].split('.')[0]

    def ping_job(self):
        """ Ping job until status is run
        """
        print("Checking that server is running...")
        time.sleep(5)

        count = 0
        while True:
            stdin, stdout, stderr = self.exec_cmd('bash -l -c "bjobs {}"'.format(self.jobID), verbose=False, output=True)
            out = stdout.read().decode('utf-8')

            if re.search('RUN', out):
                print('YES!')
                break
            else:
                print('NO!')

            if count == 20:
                raise ValueError("number of iterations allowed exceeded")

            count += 1
            time.sleep(2)

        print("Server is now running")

         # return True

    def _parse_args(self):
        parser = argparse.ArgumentParser(description="Launch a Jupyter notebook server on Orchestra")
        parser.add_argument('login_ID', type=str, help='your orchestra login ID')
        parser.add_argument('-p', '--port', type=str, default='8888', help='port on Orchestra which to start server')
        parser.add_argument('-L', '--local_port', type=str, default='8888', help='local port on which users connect to orchestra')
        parser.add_argument('-R', '--mem', type=str, default='8000', help='memory allocation for server')
        parser.add_argument('-q', '--queue', type=str, default='short', help='queue for server job execution')
        parser.add_argument('-W', '--wall_time', type=str, default='12:00', help='wall time for server existence')
        parser.add_argument('-o', '--outfile', type=str, default='jupyter.lsf', help='LSF output file for server job')
        parser.add_argument('--cmds', nargs='+', type=str, default=[], help='additional commands to run before launching the server')

        return parser.parse_args()

if __name__ == "__main__":
    spawn = Spawner()
