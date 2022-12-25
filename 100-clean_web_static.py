#!/usr/bin/python3
"""
Deletes out-of date archives using the function do_clean
"""

from fabric.api import *

env.hosts = ['3.84.238.247', '52.91.120.191']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of date archives in versions/ && /data/web_static/releases
    on both web servers

    Args:
        number: number of the archives, including the most recent, to keep

    """

    if int(number) <= 1:
        number = 1
    else:
        number = int(number)

    with lcd('versions/'):
        recent_file = local(
                "ls -t | head -{}".format(number), capture=True).split()
        files = local("ls -t", capture=True).split()
        for fil in files:
            if fil not in recent_file:
                local("sudo rm ./{}".format(fil))

    with cd('/data/web_static/releases/'):
        recent_file = run(
                "ls -t | grep 'web_static_' | head -{}".format(number))
        files = run("ls -t  | grep 'web_static_'").split()
        for fil in files:
            if fil not in recent_file:
                run("sudo rm -r ./{}".format(fil))
