import argparse
import datetime
import sys
import os
import shlex
import yaml

from subprocess import call, check_call, check_output
import defusedxml.ElementTree as et

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ftf_geonode.settings")

import django
if not hasattr(django, 'apps'):
    django.setup()
from django.core.management import call_command
from geonode.layers.management.commands import importlayers

geometry_type_to_path = {
    "POINT": "points",
    "LINE": "multilinestrings"
}

geometry_type_to_shpt = {
    "POINT": "POINT",
    "LINE": "ARC"
}


def extract_tags(node):
    tags = []
    for tag in node.findall('tag'):
        tags.append({
            "name": tag.get('k', '*'),
            "value": tag.get('v', '*')
        })
    return tags


def slug(x):
    if x[0] in ["=", "-", "_"]:
        x = x[1:len(x)]
    if x[len(x)-1] in ["=", "-", "_"]:
        x = x[0:len(x)-1]
    x = x.replace("=","-")
    x = x.replace("_","-")
    return x


def run(args):
    now = datetime.datetime.now()
    #==#
    verbose = args.verbose
    path_pbf = args.pbf
    config_path = args.config
    temp = args.temp
    #==#
    if verbose:
        print "################"
        print "Running osm_refresh.py w/ args: ", args
        print ""
    if path_pbf is None:
        print "Error: pbf must be specified.  "
        sys.exit(1)
    if config_path is None:
        print "Error: config must be specified.  "
        sys.exit(1)
    #==#
    config_text = ""
    with open(config_path, "r") as f:
        config_text = f.read()
    config = yaml.load(config_text)
    #==#
    path_pbf = os.path.expanduser(path_pbf)
    basepath = os.path.splitext(path_pbf)[0]
    path_osm = basepath
    if basepath.endswith(".osm"):
        basepath = os.path.splitext(basepath)[0]
    basepath = os.path.split(basepath)[1]
    path_osm = os.path.join(temp, basepath + ".osm")
    #==#
    if not os.path.isdir(temp):
        os.makedirs(temp)
    #==#
    for layer in config.get("layers"):
        print "####################"
        print "Importing layer", layer["id"]
        layerId = layer["id"]
        if layerId != "all_roads":
            continue
        keep = layer["keep"]
        if not isinstance(keep, basestring):
            keep = " ".join(keep)
        geometry_type = layer.get("geometry_type", "MULTIPOINT")
        category = layer.get("category", None)
        regions = args.regions or layer.get("regions", None)
        if regions:
            if not isinstance(regions, basestring):
                regions = ",".join(regions)
        cwd = os.path.join(temp, slug(layerId))
        path_osm_filtered = os.path.join(cwd, basepath + "-" + slug(layerId) +"-filtered.osm")
        path_osm_filtered_nodes = os.path.join(cwd, basepath + "-" + slug(layerId) + "-filtered-nodes.osm")
        path_osm_cleaned = os.path.join(cwd, basepath + "-" + slug(layerId) + "-cleaned.osm")
        path_shp = os.path.join(cwd, basepath + "-" + slug(layerId)+"-shp")
        path_shp_actual = os.path.join(path_shp, geometry_type_to_path[geometry_type]+".shp")
        path_osm_config = os.path.join("osm", "conf", layerId+".ini")
        #==#
        #print "path_pbf:", path_pbf
        #print "path_osm:", path_osm
        #print "path_osm_filtered:", path_osm_filtered
        #print "path_osm_filtered_nodes:", path_osm_filtered_nodes
        #print "path_osm_filtered_nodes_cleaned:", path_osm_filtered_nodes_cleaned
        #print "path_shp:", path_shp
        #print "cmd_shp:", "ogr2ogr -f \"ESRI Shapefile\" "+path_shp+" "+path_osm_filtered_nodes_cleaned+" --config OSM_CONFIG_FILE "+path_osm_config
        #==#
        if not os.path.isdir(cwd):
            os.makedirs(cwd)
        #==#
        if verbose:
            print "Filtering and reducing import data"
        if os.path.isfile(path_shp_actual) == False:

            if os.path.isfile(path_osm) == False:
                print check_output(shlex.split("osmconvert "+path_pbf+" -o="+path_osm))

            if geometry_type == "POINT":
                if os.path.isfile(path_osm_filtered) == False:
                    print check_output(shlex.split("osmfilter "+path_osm+" --keep='"+keep+"' -o="+path_osm_filtered))
                if os.path.isfile(path_osm_filtered_nodes) == False:
                    print check_output(shlex.split("osmconvert "+ path_osm_filtered+" --add-bbox-tags --all-to-nodes -o="+path_osm_filtered_nodes))
                if os.path.isfile(path_osm_cleaned) == False:
                    print check_output(shlex.split("osmfilter "+path_osm_filtered_nodes+" --keep='"+keep+"' -o="+path_osm_cleaned))
            else:
                if os.path.isfile(path_osm_cleaned) == False:
                    print check_output(shlex.split("osmfilter "+path_osm+" --keep='"+keep+"' --drop-author --drop-relations -o="+path_osm_cleaned))

            if geometry_type == "POINT":
                print check_output(shlex.split("ogr2ogr -f \"ESRI Shapefile\" "+path_shp+" "+path_osm_cleaned+" -lco ENCODING=UTF-8 -lco SHPT="+geometry_type_to_shpt[geometry_type]+" -skipfailures --config OSM_CONFIG_FILE "+path_osm_config+" --config OSM_USE_CUSTOM_INDEXING NO"))
            else:
                print check_output(shlex.split("ogr2ogr -f \"ESRI Shapefile\" "+path_shp+" "+path_osm_cleaned+" -lco ENCODING=UTF-8 -skipfailures --config OSM_CONFIG_FILE "+path_osm_config+" --config OSM_USE_CUSTOM_INDEXING NO"))

        call_command(
            'importlayers',
            path_shp_actual,
            title=layerId,
            date=now.strftime("%Y-%m-%d %H:%M:%S"),
            category=category,
            keywords=",".join(layer.get("keywords", [])),
            regions=regions,
            overwrite=True)

#==#
parser = argparse.ArgumentParser(description='Update GeoNode with data from .osm file')
parser.add_argument("--pbf", help="The path to the .osm.pbf file.")
parser.add_argument("--config", help="The path to the config file.")
parser.add_argument("--temp", default="temp", help="The path to the temp folder.")
parser.add_argument("--regions", default=None, help="The GeoNode metadata region for the layers.")
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
args = parser.parse_args()

run(args)
