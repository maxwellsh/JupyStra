# JupyStra
Painlessly run Jupyter notebook servers on O2 / Orchestra

**NOTE**: By default, JupyStra now connects to O2. To force a connection to Orchestra, use the `--orchestra` flag.

## Description
O2 / Orchestra does not officially support hosting Jupyter notebook servers but through
the magic of SSH, a notebook server can be securely spawned and accessed.
This process is non-trivial (of course - it's O2 / Orchestra), so here we provide a simple python command line tool to
take care of all the tricky stuff for you.

As an added bonus, the tool can output a shell script which can be run on any Linux / macOS
computer in the world to establish a connection to the server ... so long as the user has
Orchestra login credentials.

## Requirements
1. python 3.5+ (python 2.7 / 3.3+ will probably also work) 
2. paramiko (python SSHv2 implementation)

That's it.

## Getting Started
0. Install Jupyter on O2 / Orchestra:

   While JupyStra can handle negotiating with O2 / Orchestra on your behalf, it cannot install Jupyter for you.
   The most painless way to get Jupyter on O2 / Orchestra is to simply install [Anaconda](https://www.continuum.io/downloads).
   For those unfamiliar with Anaconda / conda, it's a modern package distribution / environment management system that 
   replaces the need for virtualenvs and pip. It can be installed by logging into O2 / Orchestra and executing:
   ```bash
   $ wget https://repo.continuum.io/archive/Anaconda3-4.3.0-Linux-x86_64.sh
   $ bash Anaconda3-4.3.0-Linux-x86_64.sh
   ```
   and following the onscreen prompts. Be sure to accept the .bashrc modification at the end. Finally, open your .bashrc file
   and move the final line (something like `export PATH=/path/to/anaconda3/bin:$PATH`) to the very top of the file.

1. Get JupyStra

   On your local machine, navigate to a directory of choice and execute
   ```bash
   $ git clone https://github.com/msherman997/JupyStra.git
   ```

2. Install paramiko

   On your local machine, execute: `conda install paramiko` or `pip install paramiko`

3. Start a server
 
   ```
   $ ./JupyStra.py <ecommonsID> --connect.
   ```

4. Enjoy Jupyter on O2 / Orchestra.

## Usage
```
usage: ./JupyStra.py login_ID [options]

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
```

## FAQ

1. *I want to use Jupyter on O2 / Orchestra, but I don't want to commit to conda. What can I do?*

   JupyStra will work so long as a Jupyter install exists on your Orchestra path. See [here](http://jupyter.readthedocs.io/en/latest/install.html)
   for other ways of installing Jupyter.

2. *JupyStra keeps writing shell scripts that I don't use. What can I do?*

   Run JupyStra with the `--no_script` flag to suppress this behavior. Be warned: this can make reconnecting to a server (see below) more difficult.

3. *How long will a JupyStra server persist on O2 / Orchestra?*

   By default, the server is run in the `short` queue, so it will exist for 12 hours. If you want a longer-living server, you can submit to any queue you have
   access to using the `-q` flag. Be sure to also specify the walltime using the `-W` flag.

   The python-mediated connection between your local machine and the server on Orchestra will die after 12 hours. You can reconnect (see below) if the server is still alive.
   The shell script connection will last indefinitely until the user kills it with `crtl^C`.

4. *I disconnected from the server. Can I reconnect to it?*

   Absolutely. Simply execute the shell script JupyStra wrote when you spanwed the server, and you'll be reconnected. 

   If you suppressed the script output, you'll have to reconnect manually. To do this, you'll need to know the name of the compute node hosting the server and the port on which
   the server is running. JupyStra writes this information to the terminal when the Server is established `Server is now running on host_name:port`,
   so you can get the info from there. If you've closed the terminal, login to O2 / Orchestra and run `squeues -u <ecommons>` (`bjobs -w` on Orchestra). Look for the job with a JOB_NAME like `jupyter` on O2 or
   `jupyter notebook --port:<port> --browser=none` on Orchestra. On O2, the `NODELIST` provides the host; now run `scontrol show job <JOBID>` where the JOBID is the ID of the jupyter job, and look for the `command` entry to get the port. For Orchestra, Get the EXEC_HOST (minus the trailing .orchestra) and the `<port>` number from this output.
   Finally, you can reconnect by running on your local machine a command such as:
   ```bash
    $ ssh -t -L 8888:127.0.0.1:8888 -l <ecommonsID> <server.address> "ssh -N -L 8888:127.0.0.1:<port> <exec_host>"
   ``` 
    where `server.address` is `o2.hms.harvard.edu` or `orchestra.med.harvard.edu`
    and pointing your browser to http://localhost:8888

5. *JupyStra launches a server in my `home/` directory, but I want it to launch in a different directory. Can I do this?*

   Sure. Simply pass `--cmds "cd path/to/your/dir"` to JupyStra and it will launch in the specified directory.

6. *When I open http://localhost:8888 in my browser, the browser says it can't connect. The terminal says something like `channel 2: open failed: connect failed: Connection refused`*

   O2 / Orchestra is just being a bit slow. Wait 10-15 seconds and try again.

7. *Why am I prompted for my ecommons password when JupyStra connects to the server? This is annoying. Make it stop!*

   The reason your prompted for a password is a bit technical. Basically, the architecture of O2 / Orchestra prevents direct access to compute nodes,
   so to access the server on a compute node, you must first go through a login node. Due to the security settings of O2 / Orchestra, the
   connection from the login node to the compute node requires credential verification even though you've already verified when connecting
   to the login node. I'm sure dev ops has a good reason for this...

   We agree it's annoying. While we can't alter JupyStra to work around this, you can get around it on your end with the magic of RSA keys and the beauty of shared filesystems.
   Here's what to do:
   1. Use JupyStra to establish a server
   2. Login to Orchestra.
   3. Run `squeue -u <ecommonsid>` or `bjobs -w` to get the EXEC_HOST name (minus the trailing .orchestra)
   4. Run `ssh-keygen -t rsa` and follow the prompts. Leave the password field empty.
   5. Run `ssh-copy-id <EXEC_HOST>`
   Next time you connect to a server, you won't be prompted for a password. What's happening? In essence you gave your O2 / Orchestra account permission to access itself. Nifty, right?

8. *I tried connecting to the server and got something like this:*
   ```
   bind: Address already in use
   channel_setup_fwd_listener_tcpip: cannot listen to port: <PORT>
   Could not request local forwarding.
   ```
   What does that mean??*

   That means the port JupyStra used to connect to the login node is already being used by something else (probably another JupyStra instance).
   While JupyStra attempts to minimize the probability of this occuring, it might still happen. Try spawning another server -- JupyStra will pick a different port.

9. *I'm done with my server but it's still running. How can I kill it?*

   Login to O2 / Orchestra and use the standard `scancel <JOBID>` or `bkill <JOBID>` where `<JOBID>` is the ID of the Jupyter server job.

## Under the hood
The establishment of a JupyStra server proceeds in several steps:

1. JupyStra uses paramiko to establish an ssh connection to an O2 / Orchestra login node.
    + By default JupyStra attempts to use RSA key authentication to establish the connection.
    + If this fails, it will prompt the user for their O2 / Orchestra password and authenticate with the password
2. JupyStra uses the ssh connection to submit a job on O2 / Orchestra which will establish a Jupyter server with access to a particular port
3. JupyStra pings Orchestra to check the status of the job until the status is reported as `RUN`
    + To prevent endless pinging, JupyStra will fail if the job isn't running after 20 checks (~45 seconds)
4. Once the server is running, JupyStra queries O2 / Orchestra for the name of the compute node hosting the server.

Connection to the server is a two step process, though JupyStra handles this as a single system command submitted via the subprocess module.
The user will be prompted to enter passwords as necessary.

1. An ssh connection is established between the local machine and an O2 / Orchestra login node using local port forwarding
    + Local port forwarding connects a port on the local machine to a port on the login node
2. A second ssh connection is opened between the login node and the compute node hosting the server again using local port fowarding
    + The fowarding is done in such a way that the local port is daisy-chained to the compute node port to which the Jupyter server has access, 
      effectively connecting the local machine to the Jupyter notebook server.
    + Since this connection must remain active, JupyStra will hang at this point until the subprocess is terminated either because it times out
      after 12 hours or is killed by the user using `ctrl^C`.
