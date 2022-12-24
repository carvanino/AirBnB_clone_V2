#!/usr/bin/python3
"""
Creates and distributes an archive to your web servers, using the
function deploy
"""

from fabric.api import *
from os.path import isfile
from datetime import datetime


env.hosts = ['3.84.238.247', '52.91.120.191']
env.user = "ubuntu"


def do_pack():
    """ Genertes the archive files, stores them in a folder versions
    """
    try:
        time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        arcfile = "versions/web_static_{}.tgz".format(time)

        local('mkdir -p versions')
        arclocal = local(
                "tar -cvzf {} web_static/".format(
                    arcfile), capture=True)
        return arclocal
    except err:
        return None


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

    run('mkdir -p /data/web_static/releases/{}/'.format(archfile))

    # Uncompress the archive to the folder /data/web_static/releases/filename
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/" .format(
        archfile_we, archfile))
    # Deletes the archive from the web server
    run('rm /tmp/{}'.format(archfile_we))

    # run('rm -rf /data/web_static/releases/{}/web_static'.format(archfile))

    # Delete the symbolic link /data/web_static/current
    run('rm -rf /data/web_static/current')

    # Move the newly created archive folder outside of the folder
    run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/ ".format(archfile, archfile))

    # Create a new symbolic link
    sudo('ln -s /data/web_static/releases/{} /data/web_static/current'.format(
        archfile))
    return True


def deploy():
    """
    Creates and distributes the archive on the webserver
    """

    arch_path = do_pack()
    if not arch_path:
        print('yes')
        return False
    # print(arch_path.__dict__)
    deploy = arch_path.__dict__['command'].split(" ")[2]
    return do_deploy(deploy)
