# JupyStra
Painlessly run Jupyter notebook servers on Orchestra

## Description
Orchestra does not officially support hosting Jupyter notebook servers but through
the magic of SSH, a notebook server can be securely spawned and accessed.
This process is non-trivial (of course - it's Orchestra), so here we provide a simple python command line tool to
take care of all the tricky stuff for you.

As an added bonus, the tool can output a shell script which can be run on any Linux / macOS
computer in the world to establish a connection to the server ... so long as the user has
Orchestra login credentials.

## Requirements
1. python 3.5+ (python 2.7 / 3.3+ will probably also work) 
2. paramiko (python SSHv2 implementation)

That's it.

## Getting Started
0. Install Jupyter on Orchestra:

   While JupyStra can handle negotiating with Orchestra on your behalf, it cannot install Jupyter for you.
   The most painless way to get Jupyter on Orchestra is to simply install [Anaconda](https://www.continuum.io/downloads).
   For those unfamiliar with Anaconda / conda, it's a modern package distribution / environment management system that 
   replaces the need for virtualenvs and pip. It can be installed by logging into Orchestra and executing:
   ```bash
   $ wget https://repo.continuum.io/archive/Anaconda3-4.3.0-Linux-x86_64.sh
   $ bash Anaconda3-4.3.0-Linux-x86_64.sh
   ```
   and following the onscreen prompts. Be sure to accept the .bashrc modification at the end.

1. Get JupyStra

   In your directory of choice: `$ git clone https://github.com/msherman997/JupyStra.git`

2. Install paramiko
   `conda install paramiko` or `pip install paramiko`

3. `./JupyStra <ecommonsID> --connect --no_script` to spawn and connect to a server.

## Usage
usage: ./JupyStra.py [-h] [-P PASSWORD] [-p PORT] [-L LOCAL_PORT]
                   [-r REMOTE_PORT] [-R MEM] [-q QUEUE] [-W WALL_TIME]
                   [-o OUTFILE] [--cmds CMDS [CMDS ...]] [--no_script]
                   [--connect]
                   login_ID

Launch a Jupyter notebook server on Orchestra

positional arguments:
  + login_ID              your orchestra login ID

optional arguments:
  + -h, --help            show this help message and exit
  + -P PASSWORD, --password PASSWORD
                        Orchestra password. NEVER USE WHEN RUNNING API
                        YOURSELF!!
  + -p PORT, --port PORT  port on Orchestra which to start server
  + -L LOCAL_PORT, --local_port LOCAL_PORT
                        local port on which users connect to orchestra
  + -r REMOTE_PORT, --remote_port REMOTE_PORT
                        remote port to use on login node
  + -R MEM, --mem MEM     memory allocation for server
  + -q QUEUE, --queue QUEUE
                        queue for server job execution
  + -W WALL_TIME, --wall_time WALL_TIME
                        wall time for server existence
  + -o OUTFILE, --outfile OUTFILE
                        LSF output file for server job
  + --cmds CMDS [CMDS ...]
                        additional commands to run before launching the server
  + --no_script           do not output bash script to connect to server
  + --connect             automatically connect to server after establishing it

## Under the hood
spawn_server.py establishes an ssh connection to an Orchestra login node using the provided login ID and
user-supplied password using paramiko. Any additional cmds provided are executed
and then a job is submitted which establishes a Jupyter notebook server on a computer node.
The script then monitors the job to ensure that it is running before obtaining the exec host name.
Using the exec host name and provided ports, the script writes a bash script which allows any
user with orchestra credentials to connect to the server.
