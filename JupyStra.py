#!/usr/bin/env python

# JupyStra.py - top level script for JupySyta package
#
# v 0.2.0a
# rev 2018-02-27 (MS: by default connects to o2)
# Notes: Updated flag for connecting to Orchestra

import argparse

from src import spawn_server
from src import spawn_server_o2

def parse_args():
    parser = argparse.ArgumentParser(description="Launch a Jupyter notebook server on Orchestra")
    parser.add_argument('login_ID', type=str, help='your orchestra login ID')
    parser.add_argument('-P', '--password', type=str, default=None, help='Orchestra password. NEVER USE WHEN RUNNING API YOURSELF!!')
    parser.add_argument('-p', '--port', type=str, default='8888', help='port on Orchestra which to start server')
    parser.add_argument('-L', '--local_port', type=str, default='8888', help='local port on which users connect to orchestra')
    parser.add_argument('-r', '--remote_port', type=str, default='random', help='remote port to use on login node')
    parser.add_argument('-R', '--mem', type=str, default='8G', help='memory allocation for server')
    parser.add_argument('-c', '--cores', type=str, default='1', help='number of cores to allocate to jupyter server')
    parser.add_argument('-q', '--queue', type=str, default='short', help='queue for server job execution')
    parser.add_argument('-W', '--wall_time', type=str, default='12:00:00', help='wall time for server existence')
    parser.add_argument('-o', '--outfile', type=str, default='jupyter.lsf', help='LSF output file for server job')
    parser.add_argument('--count', type=int, default=20, help='maximum number of times to ping cluster when establishing server')
    parser.add_argument('--cmds', nargs='+', type=str, default=[], help='additional commands to run before launching the server')
    parser.add_argument('--no_script', dest='script', action='store_false', default=True, help='do not output bash script to connect to server')
    parser.add_argument('--connect', action='store_true', default=False, help='automatically connect to server after establishing it')
    parser.add_argument('--orchestra', dest="O2", action='store_false', default=True, help='Connect to orchestra instead of O2 -- PLEASE SET WALLTIME MANUALLY.')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.O2:
        spawn = spawn_server_o2.Spawner(args)
    else:    
        spawn = spawn_server.Spawner(args)
