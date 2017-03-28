import datetime
import os
import subprocess


def get_version(version=None):
    return os.getenv('GEONODE_VERSION', '0.0.1')
