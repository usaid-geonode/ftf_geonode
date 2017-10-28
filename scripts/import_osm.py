import argparse
import datetime
import os
import requests
import shlex
import shutil
import sys
import requests
import yaml
import urllib

from subprocess import call, check_call, check_output
import defusedxml.ElementTree as et

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ftf_geonode.settings")

import django
if not hasattr(django, 'apps'):
    django.setup()

from django.core.management import call_command
from django.conf import settings
from geonode.base.models import Link, SpatialRepresentationType, TopicCategory, Region, License
from geonode.layers.management.commands import importlayers
from geonode.layers.models import Layer

geometry_type_to_path = {
    "POINT": "points",
    "LINE": "lines",
    "POLYGON": "multipolygons"
}

#geometry_type_to_shpt = {
#    "POINT": "POINT",
#    "LINE": "ARC"
#}

SCRIPT_PATH = os.path.realpath(__file__)

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


def encode_keep(x):
    y = x
    if not isinstance(y, basestring):
        y = " ".join(y)
    y = y.replace("*", "")
    return y

def run(args):
    now = datetime.datetime.now()
    #==#
    verbose = args.verbose
    clean = args.clean
    url = args.url
    path_pbf = args.pbf
    config_path = args.config
    temp = args.temp
    user_geometry_type = args.geometry_type
    user_layer_id = args.layer_id
    user_layer_name_prefix = args.layer_name_prefix
    user_layer_title_prefix = args.layer_title_prefix
    #==#
    print "################"
    print "Running import_osm.py w/ args: ", args
    print ""
    if path_pbf is None and url is None:
        print "Error: url or pbf must be specified.  "
        sys.exit(1)
    if config_path is None:
        print "Error: config must be specified.  "
        sys.exit(1)
    #==#
    if clean and temp:
        if os.path.isfile(path_pbf):
            os.remove(path_pbf)
        if os.path.isdir(temp):
            shutil.rmtree(temp)
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
    path_osm = os.path.join(temp, basepath + ".o5m")
    #==#
    if not os.path.isdir(temp):
        os.makedirs(temp)
    #==#
    #print "os.path.isfile(path_pbf):", os.path.isfile(path_pbf)
    #print "path_pbf:", path_pbf
    if os.path.isfile(path_pbf) == False:
        if url is not None:
            print "Downloading pbf file from url <", url, ">."
            urllib.URLopener().retrieve(url, path_pbf)
            if os.path.isfile(path_pbf) == False:
                print "Error: Could not download PBF file from url <", url, ">."
                sys.exit(1)
        else:
            print "Error: Could not find pbf file and url is none."
            sys.exit(1)
    #==#
    if os.path.isfile(path_osm) == False:
        print "####################"
        print "Coverting input pbf to o5m"
        print "path_pbf:", path_pbf
        print "path_osm:", path_osm
        print check_output(shlex.split("osmconvert "+path_pbf+" -o="+path_osm))
    #==#c
    for cache in config.get("caches"):
        print "####################"
        print "Creating cache", cache["id"]
        cwd = os.path.join(temp, "caches")
        if not os.path.isdir(cwd):
            os.makedirs(cwd)
        path_osm_cached = os.path.join(cwd, cache["id"]+".o5m")
        if os.path.isfile(path_osm_cached) == False:
            print check_output(shlex.split("osmfilter "+path_osm+" --keep='"+encode_keep(cache["keep"])+"' --drop-author --drop-relations -o="+path_osm_cached))

    for layer in config.get("layers"):
        print "####################"
        layerId = layer["id"]
        layerTitle = layer.get("title") or layer["id"]
        layer_geometry_type = layer.get("geometry_type", "MULTIPOINT")

        if ((user_layer_id is None) or (user_layer_id == layer["id"])) and ((user_geometry_type is None) or (user_geometry_type == layer_geometry_type)):
            print "Importing layer", layer["id"]
            layerCache = layer.get("cache")
            keep = encode_keep(layer["keep"])
            license = args.license or layer.get("license", None)
            category = layer.get("category", None)
            regions = args.regions or layer.get("regions", None)
            if regions:
                if not isinstance(regions, basestring):
                    regions = ",".join(regions)

            cwd = os.path.join(temp, "layers", slug(layerId))
            path_osm_filtered = os.path.join(temp, "caches", layerCache+".o5m") if layerCache else os.path.join(cwd, basepath + "-" + slug(layerId) +"-filtered.osm")
            path_osm_filtered_nodes = os.path.join(cwd, basepath + "-" + slug(layerId) + "-filtered-nodes.o5m")
            path_osm_cleaned = os.path.join(cwd, basepath + "-" + slug(layerId) + "-cleaned.osm")
            path_shp = os.path.join(cwd, basepath + "-" + slug(layerId)+"-shp")
            path_shp_actual = os.path.join(path_shp, geometry_type_to_path[layer_geometry_type]+".shp")
            path_osm_config = os.path.normpath(os.path.join(SCRIPT_PATH, "..", "..", "osm", "conf", layerId+".ini"))
            #path_sld_template = os.path.join("osm", "conf", layerId+".sld")
            #path_sld_actual = os.path.join(path_shp, geometry_type_to_path[layer_geometry_type]+".sld")

            if layerCache:
                print "Using cache ", layerCache
                print "path_osm_filtered:", path_osm_filtered
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
            if os.path.isfile(path_shp_actual) == False:

                if layer_geometry_type == "POINT":
                    if os.path.isfile(path_osm_filtered) == False:
                        print check_output(shlex.split("osmfilter "+path_osm+" --keep='"+keep+"' --drop-author --drop-relations -o="+path_osm_filtered))
                    if os.path.isfile(path_osm_filtered_nodes) == False:
                        print check_output(shlex.split("osmconvert "+ path_osm_filtered+" --add-bbox-tags --all-to-nodes -o="+path_osm_filtered_nodes))
                    if os.path.isfile(path_osm_cleaned) == False:
                        print check_output(shlex.split("osmfilter "+path_osm_filtered_nodes+" --keep='"+keep+"' -o="+path_osm_cleaned))
                else:
                    if os.path.isfile(path_osm_cleaned) == False:
                        #print "osmfilter "+path_osm+" --keep='"+keep+"' --drop-author --drop-version --drop-relations -o="+path_osm_cleaned
                        #continue
                        print check_output(shlex.split("osmfilter "+path_osm+" --keep='"+keep+"' --drop-author --drop-relations -o="+path_osm_cleaned))

                print check_output(shlex.split("ogr2ogr -f \"ESRI Shapefile\" "+path_shp+" "+path_osm_cleaned+" -lco ENCODING=UTF-8 -skipfailures --config OSM_CONFIG_FILE "+path_osm_config+" --config OSM_USE_CUSTOM_INDEXING NO --config CPL_TMPDIR /tmp"))
                #if geometry_type == "POINT":
                #    print check_output(shlex.split("ogr2ogr -f \"ESRI Shapefile\" "+path_shp+" "+path_osm_cleaned+" -lco ENCODING=UTF-8 -lco SHPT="+geometry_type_to_shpt[geometry_type]+" -skipfailures --config OSM_CONFIG_FILE "+path_osm_config+" --config OSM_USE_CUSTOM_INDEXING NO --config CPL_TMPDIR /tmp"))
                #else:
                #    print "ogr2ogr -f \"ESRI Shapefile\" "+path_shp+" "+path_osm_cleaned+" -lco ENCODING=UTF-8 -lco SHPT="+geometry_type_to_shpt[geometry_type]+" -skipfailures --config OSM_CONFIG_FILE "+path_osm_config+" --config OSM_USE_CUSTOM_INDEXING NO"
                #    continue
                #    print check_output(shlex.split("ogr2ogr -f \"ESRI Shapefile\" "+path_shp+" "+path_osm_cleaned+" -lco ENCODING=UTF-8 -lco SHPT="+geometry_type_to_shpt[geometry_type]+" -skipfailures --config OSM_CONFIG_FILE "+path_osm_config+" --config OSM_USE_CUSTOM_INDEXING NO"))

            #isExistingLayer = len(Layer.objects.filter(title=layerId).values_list('id')) > 0
            #print "isExistingLayer", isExistingLayer
            #sld_body = None
            #if isExistingLayer:
            #    if os.path.isfile(path_sld_actual):
            #        os.remove(path_sld_actual)
            #else:
            #    if os.path.isfile(path_sld_template):
            #        shutil.copyfile(path_sld_template, path_sld_actual)
            #        with open(path_sld_actual) as f:
            #            sld_body = f.read()

            #if isExistingLayer:
            #    for style_id in [layerId, layerId+"_layer"]:
            #        print "--------------------"
            #        url = settings.OGC_SERVER['default']['LOCATION']+"rest/styles/"+style_id+".sld"
            #        auth = (settings.OGC_SERVER['default']['USER'], settings.OGC_SERVER['default']['PASSWORD'])
            #        print "URL: ", url
            #        print "Auth: ", auth
            #        response = requests.delete(url, auth=auth)

            abstract = "OSM Extract imported at "+now.strftime("%Y-%m-%d %H:%M:%S")+".  Filtered by the following osm tags: "+keep
            call_command(
                'importlayers',
                path_shp_actual,
                layername=(user_layer_name_prefix + layerId if user_layer_name_prefix else layerId),
                title=(user_layer_title_prefix + layerTitle if user_layer_title_prefix else layerTitle),
                abstract=abstract,
                date=now.strftime("%Y-%m-%d %H:%M:%S"),
                category=category,
                keywords=",".join(layer.get("keywords", [])),
                license=license,
                regions=regions,
                overwrite=True)

            #if sld_body and isExistingLayer:
            #    #print "sld_body:", sld_body
            #    for style_id in [layerId, layerId+"_layer"]:
            #        print "--------------------"
            #        url = settings.OGC_SERVER['default']['LOCATION']+"rest/styles/"+style_id+".sld"
            #        auth = (settings.OGC_SERVER['default']['USER'], settings.OGC_SERVER['default']['PASSWORD'])
            #        print "URL: ", url
            #        print "Auth: ", auth
            #        #response = requests.delete(url, auth=auth)
            #        #print "Delete style ", style_id
            #        #print "Response status code", response.status_code
            #        #print response.text
            #        #response = requests.put(
            #        #    url,
            #        #    auth=auth,
            #        #    headers={'Content-type': 'application/vnd.ogc.sld+xml'},
            #        #    params={'file': path_sld_actual},
            #        #    data=sld_body)
            #        response = requests.put(url, auth=auth, headers={'Content-type': 'application/vnd.ogc.sld+xml'}, data=sld_body)
            #        print "Put style ", style_id
            #        print "Response status code", response.status_code
            #        print response.text

        else:
            print "Skipping layer", layer["id"]

#==#
licenses = [x.abbreviation or x.name for x in License.objects.all()]
categories = [x.identifier for x in TopicCategory.objects.all()]
#==#
parser = argparse.ArgumentParser(description='Update GeoNode with data from .osm file.')
parser.add_argument("--url", help="The url to the remote .osm.pbf file.")
parser.add_argument("--pbf", help="The path to the .osm.pbf file.")
parser.add_argument("--config", help="The path to the config file.")
parser.add_argument("--temp", default="temp", help="The path to the temp folder.")
parser.add_argument("--category", default=None, help="The category for the layers.  One of the following: "+(", ".join(categories)))
parser.add_argument("--license", default=None, help="The license for the layers. One of the following: "+(", ".join(licenses)))
parser.add_argument("--regions", default=None, help="The GeoNode metadata region for the layers.")
parser.add_argument("--geometry-type", '-gt', default=None, help="Only update layers with geometry type POINT.")
parser.add_argument("--layer-name-prefix", default=None, help="Prefix for layer names, e.g., nepal_")
parser.add_argument("--layer-title-prefix", default=None, help="Prefix for layer titles, e.g., Nepal.")
parser.add_argument("--layer-id", '-l', default=None, help="Only layers with the layer id.")
parser.add_argument('--clean', default=0, action='count', help="Start from scratch (clean out temp files).")
parser.add_argument('--verbose', '-v', default=0, action='count', help="Print out intermediate status messages.")
args = parser.parse_args()

run(args)
