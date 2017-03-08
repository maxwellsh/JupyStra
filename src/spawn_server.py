# spawn_server.py - Spawn a Jupyter Notebook server on Orchestra
#
# v 0.1.0
# rev 2017-03-07 (MS: better additional command handling)
# Notes: more informative print statements

import paramiko
import argparse
import getpass
import time
import re
import subprocess

from . import script_writer

def prompt_password():
    password = getpass.getpass("Orchestra password: ")
    return password

class Spawner(object):
    """ A class for spanwing Jupyter notebook servers on Orchestra
    """

    client = None
    args = None
    password = None

    def __init__(self, args):
        # self.args = self._parse_args()
        self.args = args
        self.login = self.args.login_ID

        if not self.args.password:
            self.password = prompt_password()

        # connect to remote host
        self._connect()

        # Run additional cmds
        # self.run_addtn_cmds()

        # Submit job to estblish server and get exec host name
        self.submit_server_job()
        self.get_exec_host()

        # Write shell script
        if self.args.script:
            self.write_shell_script()

        # Connect to server if necessary
        if self.args.connect:
            self.connect_to_jup_server()

    # def _prompt_password(self):
    #     password = getpass.getpass("Orchestra password: ")
    #     return password

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
        cmd = "bash -l -c "
        cmd += "\"" + "; ".join(self.args.cmds)
        cmd += "; " + "bsub -q {queue} -W {walltime} -o {outfile} 'jupyter notebook --port={port_jup} --browser=\"none\"'\"".format(**kwargs)
        # cmd = cmd_addnt + '; ' + cmd_jup
        # print(cmd)

        stdin, stdout, stderr = self.exec_cmd(cmd, verbose=False, output=True)
        out = stdout.read().decode('utf-8')

        # 'job <JOBID> submitte to queue QUEUE'
        self.jobID = out.split()[1].split('<')[1].split('>')[0]

    def get_exec_host(self):
        # Ensure job is running
        self.ping_job()
        
        stdin, stdout, stderr = self.exec_cmd('bash -l -c "bjobs -w {}"'.format(self.jobID), verbose=False, output=True)

        # only interested in the second line
        stdout.readline()
        out = stdout.readline()
        self.exec_host = out.split()[5].split('.')[0]

        print("Server is now running on {}:{}".format(self.exec_host, self.args.port))

    def write_shell_script(self):
        sw = script_writer.ShellWriter(self.exec_host, port_local=self.args.local_port, port_remote=self.args.remote_port, port_jup=self.args.port)
        sw.write_bash_script()
        print("bash script written to file {}".format(sw.fname))

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

         # return True

    def connect_to_jup_server(self):
        sw = script_writer.ShellWriter(self.exec_host, port_local=self.args.local_port, port_remote=self.args.remote_port, port_jup=self.args.port, username=self.login)
        cmd = sw.get_ssh_cmd()
    
        timeout = 12*60*60

        print("\nConnecting to Server. If successful, the script will appear to hang.")
        print("In your favorite browser, got to http://localhost:{}".format(self.args.local_port))
        print("ctrl^C to disconnect")

        try:
            p = subprocess.run(cmd, shell=True, timeout=timeout)
        except KeyboardInterrupt:
            print("Connection to server killed by user")

# def parse_args():
#     parser = argparse.ArgumentParser(description="Launch a Jupyter notebook server on Orchestra")
#     parser.add_argument('login_ID', type=str, help='your orchestra login ID')
#     parser.add_argument('-P', '--password', type=str, default=None, help='Orchestra password. NEVER USE WHEN RUNNING API YOURSELF!!')
#     parser.add_argument('-p', '--port', type=str, default='8888', help='port on Orchestra which to start server')
#     parser.add_argument('-L', '--local_port', type=str, default='8888', help='local port on which users connect to orchestra')
#     parser.add_argument('-r', '--remote_port', type=str, default='8888', help='remote port to use on login node')
#     parser.add_argument('-R', '--mem', type=str, default='8000', help='memory allocation for server')
#     parser.add_argument('-q', '--queue', type=str, default='short', help='queue for server job execution')
#     parser.add_argument('-W', '--wall_time', type=str, default='12:00', help='wall time for server existence')
#     parser.add_argument('-o', '--outfile', type=str, default='jupyter.lsf', help='LSF output file for server job')
#     parser.add_argument('--cmds', nargs='+', type=str, default=[], help='additional commands to run before launching the server')
#     parser.add_argument('--no_script', dest='script', action='store_false', default=True, help='do not output bash script to connect to server')
#     parser.add_argument('--connect', action='store_true', default=False, help='automatically connect to server after establishing it')
# 
#     return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    spawn = Spawner(args)