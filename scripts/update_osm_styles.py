import argparse
import datetime
import os
import requests
import shlex
import shutil
import sys
import yaml

from subprocess import call, check_call, check_output
import defusedxml.ElementTree as et

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ftf_geonode.settings")

import django
if not hasattr(django, 'apps'):
    django.setup()

from django.core.management import call_command
from django.conf import settings
from geonode.layers.management.commands import importlayers
from geonode.layers.models import Layer


def run(args):
    now = datetime.datetime.now()
    #==#
    verbose = args.verbose
    config_path = args.config
    user_geometry_type = args.geometry_type
    user_layer_id = args.layer_id
    #==#
    print "################"
    print "Running import_osm.py w/ args: ", args
    print ""
    if config_path is None:
        print "Error: config must be specified.  "
        sys.exit(1)
    #==#
    config_text = ""
    with open(config_path, "r") as f:
        config_text = f.read()
    config = yaml.load(config_text)
    #==#

    for layer in config.get("layers"):
        print "####################"
        layerId = layer["id"]
        layer_geometry_type = layer.get("geometry_type", "MULTIPOINT")

        if ((user_layer_id is None) or (user_layer_id == layer["id"])) and ((user_geometry_type is None) or (user_geometry_type == layer_geometry_type)):
            path_sld_template = os.path.join("osm", "conf", layerId+".sld")

            sld_body = None
            if os.path.isfile(path_sld_template):
                with open(path_sld_template) as f:
                    sld_body = f.read()

            if sld_body:
                #print "sld_body:", sld_body
                for style_id in [layerId, layerId+"_layer"]:
                    print "--------------------"
                    url = settings.OGC_SERVER['default']['LOCATION']+"rest/styles/"+style_id+".sld"
                    auth = (settings.OGC_SERVER['default']['USER'], settings.OGC_SERVER['default']['PASSWORD'])
                    print "URL: ", url
                    print "Auth: ", auth
                    #response = requests.delete(url, auth=auth)
                    #print "Delete style ", style_id
                    #print "Response status code", response.status_code
                    #print response.text
                    #response = requests.put(
                    #    url,
                    #    auth=auth,
                    #    headers={'Content-type': 'application/vnd.ogc.sld+xml'},
                    #    params={'file': path_sld_actual},
                    #    data=sld_body)
                    response = requests.put(url, auth=auth, headers={'Content-type': 'application/vnd.ogc.sld+xml'}, data=sld_body)
                    print "Put style ", style_id
                    print "Response status code", response.status_code
                    print response.text

        else:
            print "Skipping layer", layer["id"]

#==#
parser = argparse.ArgumentParser(description='Update GeoNode with data from .osm file')
parser.add_argument("--config", help="The path to the config file.")
parser.add_argument("--geometry-type", '-gt', default=None, help="Only update layers with geometry type POINT.")
parser.add_argument("--layer-id", '-l', default=None, help="Only layers with the layer id.")
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
args = parser.parse_args()

run(args)
