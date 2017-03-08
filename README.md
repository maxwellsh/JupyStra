# JupyStra
Painlessly run Jupyter notebook servers on Orchestra

## Description
Orchestra does not officially support hosting Jupyter Notebook servers, but through
the magic of SSH, a notebook server can be securely spawned and accessed.
This process is non-trivial, so here we provide a simply python command line tool to
take care of all the tricky port forwarding for you.

As an added bonus, the tool can output a bash script which can be run on any Linux / macOS
computer in the world to establish a connection to the server...so long as the user has
Orchestra login credentials.

## Dependencies
python 3.x (likely 3.3+)
paramiko

## Usage
spawn_server.py [-h] [-p PORT] [-L LOCAL_PORT] [-r REMOTE_PORT]
                       [-R MEM] [-q QUEUE] [-W WALL_TIME] [-o OUTFILE]
                       [--cmds CMDS [CMDS ...]]
                       login_IDusage: spawn_server.py [-h] [-p PORT] [-L LOCAL_PORT] [-r REMOTE_PORT]
                       [-R MEM] [-q QUEUE] [-W WALL_TIME] [-o OUTFILE]
                       [--cmds CMDS [CMDS ...]]
                       login_ID

bash my_server_xx.sh [-h] login_ID

## Under the hood
spawn_server.py establishes an ssh connection to an Orchestra login node using the provided login ID and
user-supplied password using paramiko. Any additional cmds provided are executed
and then a job is submitted which establishes a Jupyter notebook server on a computer node.
The script then monitors the job to ensure that it is running before obtaining the exec host name.
Using the exec host name and provided ports, the script writes a bash script which allows any
user with orchestra credentials to connect to the server.
