#!/usr/bin/python3
"""
Generates a .tgz archive from the content of web_static folder
using the do_pack function
"""
from fabric.api import *
from datetime import datetime


def do_pack():
    """ Genertes the archive files, stores them in a folder versions
    """
    try:
        time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        arcfile = "versions/web_static_{}.tgz".format(time)

        local('mkdir -p versions')
        arclocal = local(
                "tar -czvf {} web_static/".format(
                    arcfile), capture=True)
        return arclocal
    except err:
        return None
