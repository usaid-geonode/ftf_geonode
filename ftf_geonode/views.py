import yaml

try:
    import simplejson as json
except ImportError:
    import json

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse

from ftf_geonode.utils import build_overlays, build_navbar_title, build_navbar_toolbar, build_navbar_featurelayers, build_navbar_categories, build_baselayers, build_featurelayers

def dashboard_config_viewer(request):
    data = None

    featurelayers = build_featurelayers()

    data = yaml.load(get_template("dashboards/viewer.yml").render({}))
    data["baselayers"] = build_baselayers()
    data["overlays"] = build_overlays(category=id, featurelayers=featurelayers)
    data["navbars"] = [
        build_navbar_title(breadcrumbs=[]),
        build_navbar_toolbar(),
        build_navbar_categories()
    ]
    data["featurelayers"] = featurelayers

    data["view"] = {
        "baselayer": "osm",
        #"featurelayers": [x["id"] for x in featurelayers]
        "featurelayers": ["geonode:cities", "geonode:nepal_ftf_zoi"],
        "latitude": 28.183,
        "longitude": 84.853,
        "maxZoom": 18,
        "minZoom": 0,
        "zoom": 6,
        "controls": []
    }
    data["renderlayers"] = [x["id"] for x in featurelayers] + ["osm"]
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

def dashboard_config_all(request):
    data = None

    featurelayers = build_featurelayers()

    data = yaml.load(get_template("dashboards/viewer.yml").render({}))
    data["overlays"] = build_overlays(featurelayers=featurelayers)
    data["navbars"] = [
        build_navbar_title(breadcrumbs=[{"title": "All"}]),
        build_navbar_toolbar(),
        build_navbar_featurelayers(featurelayers=featurelayers)
    ]
    data["baselayers"] = build_baselayers()
    data["featurelayers"] = featurelayers

    data["view"] = {
        "baselayer": "osm",
        #"featurelayers": [x["id"] for x in featurelayers]
        "featurelayers": ["geonode:cities", "geonode:nepal_ftf_zoi"],
        "latitude": 28.183,
        "longitude": 84.853,
        "maxZoom": 18,
        "minZoom": 0,
        "zoom": 6,
        "controls": []
    }
    data["renderlayers"] = [x["id"] for x in featurelayers] + ["osm"]
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

def dashboard_config_category(request, id=None):
    data = None

    featurelayers = build_featurelayers(category=id)

    data = yaml.load(get_template("dashboards/viewer.yml").render({}))
    data["overlays"] = build_overlays(category=id, featurelayers=featurelayers)
    data["navbars"] = [
        build_navbar_title(breadcrumbs=[{"title": "Category: "+id}]),
        build_navbar_toolbar(),
        build_navbar_featurelayers(featurelayers=featurelayers)
    ]
    data["baselayers"] = build_baselayers()
    data["featurelayers"] = featurelayers

    data["view"] = {
        "baselayer": "osm",
        #"featurelayers": [x["id"] for x in featurelayers]
        "featurelayers": ["geonode:cities", "geonode:nepal_ftf_zoi"],
        "latitude": 28.183,
        "longitude": 84.853,
        "maxZoom": 18,
        "minZoom": 0,
        "zoom": 6,
        "controls": []
    }
    data["renderlayers"] = [x["id"] for x in featurelayers] + ["osm"]
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

def dashboard_config_template(request, id):
    data = None
    if id == "home":
        data = yaml.load(get_template("dashboards/"+id+".yml").render({}))
        data["navbars"] = [
            build_navbar_title(breadcrumbs=[]),
            build_navbar_toolbar(geolocation=False)
        ]
    else:
        featurelayers = build_featurelayers()
        data = yaml.load(get_template("dashboards/"+id+".yml").render({}))
        data["overlays"] = build_overlays(category=None, featurelayers=featurelayers)
        data["navbars"] = [
            build_navbar_title(breadcrumbs=[]),
            build_navbar_toolbar()
        ]
        data["baselayers"] = build_baselayers()
        data["featurelayers"] = featurelayers

        data["view"] = {
            "baselayer": "osm",
            #"featurelayers": [x["id"] for x in featurelayers]
            "featurelayers": ["geonode:cities", "geonode:nepal_ftf_zoi"],
            "latitude": 28.183,
            "longitude": 84.853,
            "maxZoom": 18,
            "minZoom": 0,
            "zoom": 6,
            "controls": []
        }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

def dashboard_state(request, id=None, page=None):
    data = None
    if id == "viewer":
        data = {
            "view": {
                "featurelayers": ["geonode:cities", "geonode:nepal_ftf_zoi"]
            }
        }
    else:
        data = {}

    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
