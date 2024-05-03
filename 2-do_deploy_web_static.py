#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ["54.236.8.64", "100.24.72.30"]
env.user = 'ubuntu'  # Username for SSH

def do_deploy(archive_path):
    """Deploy package to remote server."""
    if not archive_path or not os.path.exists(archive_path):
        return False
    put(archive_path, '/tmp')
    ar_name = archive_path[archive_path.find("/") + 1: -4]
    run('mkdir -p /data/web_static/releases/{}/'.format(ar_name))
    run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.format(ar_name, ar_name))
    run('rm /tmp/{}.tgz'.format(ar_name))
    run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(ar_name, ar_name))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(ar_name))
    run('rm -rf /data/web_static/current')
    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(ar_name))
    print("New version deployed!")
    return True
