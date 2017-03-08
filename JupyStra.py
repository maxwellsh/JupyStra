#!/usr/bin/env python

# JupyStra.py - top level script for JupySyta package
#
# v 0.1.2
# rev 2017-03-08 (MS: randomly generate remote port by default)
# Notes: 

import argparse

from src import spawn_server

def parse_args():
    parser = argparse.ArgumentParser(description="Launch a Jupyter notebook server on Orchestra")
    parser.add_argument('login_ID', type=str, help='your orchestra login ID')
    parser.add_argument('-P', '--password', type=str, default=None, help='Orchestra password. NEVER USE WHEN RUNNING API YOURSELF!!')
    parser.add_argument('-p', '--port', type=str, default='8888', help='port on Orchestra which to start server')
    parser.add_argument('-L', '--local_port', type=str, default='8888', help='local port on which users connect to orchestra')
    parser.add_argument('-r', '--remote_port', type=str, default='random', help='remote port to use on login node')
    parser.add_argument('-R', '--mem', type=str, default='8000', help='memory allocation for server')
    parser.add_argument('-q', '--queue', type=str, default='short', help='queue for server job execution')
    parser.add_argument('-W', '--wall_time', type=str, default='12:00', help='wall time for server existence')
    parser.add_argument('-o', '--outfile', type=str, default='jupyter.lsf', help='LSF output file for server job')
    parser.add_argument('--cmds', nargs='+', type=str, default=[], help='additional commands to run before launching the server')
    parser.add_argument('--no_script', dest='script', action='store_false', default=True, help='do not output bash script to connect to server')
    parser.add_argument('--connect', action='store_true', default=False, help='automatically connect to server after establishing it')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    spawn = spawn_server.Spawner(args)
