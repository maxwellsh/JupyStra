# script_write.py - Write bash script to connect to Jupyter notebook server on Orchestra
#
# v 0.0.4
# rev 2017-03-06 (MS: more informative message)
# Notes: 

# import pathlib2
import time

class ShellWriter(object):
    def __init__(self, exec_host, name="my_server", port_local=8888, port_remote=8888, port_jup=8888):
        # time_str = time.strftime("%d-%m-%Y")
        time_str = time.strftime("%d-%m-%Y-%H:%M:%S")
        self.fname =  "{}_{}.sh".format(name, time_str)

        self.f = open(self.fname, 'w')

        self._write_help()
        self._write_msg(port_local)
        self._write_ssh(exec_host, port_local, port_remote, port_jup)

        self.f.close()

    def _write_help(self):
        hlp = """ 
function usage()
{
    echo "Connect to a Jupyter notebook server on Orchestra"
    echo ""
    echo "usage: bash test_script.sh [-h] login_ID"
    echo ""
    echo "Positional arguments:"
    echo ""
    echo "	login_ID: orchestra login ID"
    echo ""
    echo "Optional arguments"
    echo ""
    echo "	-h --help: print this help message and exit"
    echo ""
}

if [ $# -ne 1 ]
  then
    usage
    exit
fi

if [ $1 == '-h' -o $1 == '--help' ]
    then
        usage
        exit
fi
"""
        self.f.write(hlp)

    def _write_msg(self, port_local):
        msg = """
echo "Connecting to server"
echo "If successful, the script will appear to hand. This is good"
echo "In you browser, go to: 127.0.0.1:{}"
echo ""
echo "ctrl^c to exit"
echo ""
\n""".format(port_local)
        self.f.write(msg)

    def _write_ssh(self, exec_host, port_local, port_remote, port_jup):
        kwargs = {'port_local': port_local,
                  'port_remote': port_remote,
                  'port_jup': port_jup,
                  'exec_host': exec_host
        }

        cmd = "ssh -t -L {port_local}:127.0.0.1:{port_remote} -l $1 orchestra.med.harvard.edu \"ssh -N -L {port_remote}:127.0.0.1:{port_jup} {exec_host}\"".format(**kwargs)
        self.f.write(cmd)
