#!/usr/bin/python3
"""
Distribute an archive to web server uisng do_deploy()
"""

from fabric.api import *
from os.path import isfile

env.hosts = ['3.84.238.247', '52.91.120.191']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Uploads the archive to the /tmp/ directory of the web server
    Uncompresses the archive to the folder
    /data/web_static/releases/<archive filename without extension>
    Deletes the archive from the web server
    Deletes the symbolic link /data/web_static/current from the server
    Creates a new symbolic link /data/web_static/current
    and links to /data/web_static/releases/<archive filename without extension>
    """

    # env.hosts = ['3.84.238.247', '52.91.120.191']
    # env.user = "ubuntu"
    if not isfile(archive_path):
        return False
    # Uploads the archive to /tmp/ directory of the web servers
    put(archive_path, '/tmp/')

    filename = archive_path.split('/')
    # filename = ['versions', 'web_static_20170315003959.tgz']
    archfile_we = filename[-1]
    # archfile_we = web_static_20170315003959.tgz
    archfile = archfile_we.split('.')
    # archfile = ['web_static_20170315003959', 'tgz']
    archfile = archfile[0]
    # archfile = 'web_static_20170315003959'

    run('rm -rf /data/web_static/releases/{}/'.format(archfile))
    run('mkdir -p /data/web_static/releases/{}/'.format(archfile))

    # Uncompress the archive to the folder /data/web_static/releases/filename
    # run('rm -rf /data/web_static/releases/{}/'.format(archfile))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/" .format(
        archfile_we, archfile))
    # Deletes the archive from the web server
    run('rm /tmp/{}'.format(archfile_we))
    run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/ ".format(archfile, archfile))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(archfile))
    # Delete the symbolic link /data/web_static/current
    run('rm -rf /data/web_static/current')
    # Create a new symbolic link
    run('ln -s /data/web_static/current /data/web_static/releases/{}'.format(
        archfile))
    return True
