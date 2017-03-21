from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from geonode.layers.models import Layer
from geonode.base.models import TopicCategory

def build_overlays(category=None, featurelayers=None):
    overlays = []

    overlay_print = {
        "id": "print_map",
        "type": "text",
        "title": "Print Map",
        "position": {
            "top": "calc(1rem + 10px + 2rem + 10px + 0.5rem)",
            "right": "1rem",
            "bottom": "auto",
            "left": "auto"
        },
        "text": {
            "content": u"\uf02f",
            "font": {
                "family": "FontAwesome",
                "size": "2rem"
            }
        },
        "tooltip": {
            "placement": "left",
            "content": "Print Map"
        },
        "css": {
            "properties": [
                {"name": "background", "value": "rgba(0, 0, 0, 0.8)"},
                {"name": "padding", "value": "0.5rem 1rem"},
                {"name": "border-radius", "value": "8px"},
            ]
        },
        "intents": [{"name": "printMap"}]
    }
    #overlays.append(overlay_print)

    return overlays


def build_navbar_title(breadcrumbs=None):
    tabs = [
        {
            "title": "Data Driven\nFarming GeoNode",
            "value": "Data Driven\nFarming GeoNode",
            #"tooltip": { "content": "Viewer"},
            "css": {
                "classes": [""],
                "properties": [
                    { "name": "font-size", "value": "20px" },
                    { "name": "font-family", "value": "\"proxima-nova-soft\", sans-serif !important" },
                    { "name": "font-weight", "value": "600 !important"},
                    { "name": "border-radius", "value": "0px 0px 0px 0px"},
                    { "name": "text-align", "value": "left"},
                    { "name": "line-height", "value": "24px"},
                    { "name": "background", "value": "rgba(0, 0, 0, 0.8)" }
                ]
            },
            "link": {
                "url": "/",
                "target": "_top"
            }
        },
        {
            "title": "Viewer",
            "value": "Viewer",
            #"tooltip": { "content": "Viewer"},
            "css": {
                "classes": [""],
                "properties": [
                    { "name": "font-size", "value": "20px" },
                    { "name": "font-family", "value": "\"proxima-nova-soft\", sans-serif !important" },
                    { "name": "font-weight", "value": "600 !important"},
                    { "name": "border-radius", "value": "0px 0px 0px 0px"},
                    { "name": "text-align", "value": "left"},
                    { "name": "line-height", "value": "48px"},
                    { "name": "background", "value": "rgba(0, 0, 0, 0.8)" }
                ]
            },
            "link": {
                "url": "/viewer?main:config=/dashboards/viewer/config",
                "target": "_top"
            }
        }
    ]
    for bc in breadcrumbs:
        tab = {
            "title": bc['title'],
            "value": bc['title'],
            #"tooltip": { "content": "Viewer"},
            "css": {
              "classes": [""],
              "properties": [
                    { "name": "font-size", "value": "20px" },
                    { "name": "font-family", "value": "\"proxima-nova-soft\", sans-serif !important" },
                    { "name": "font-weight", "value": "600 !important"},
                    { "name": "border-radius", "value": "0px 0px 0px 0px"},
                    { "name": "text-align", "value": "left"},
                    { "name": "line-height", "value": "48px"},
                    { "name": "background", "value": "rgba(0, 0, 0, 0.8)" }
              ]
            },
            "link": {
                "url": bc.get('url'),
                "target": "_top"
            }
        }
        tabs.append(tab)

    #tab = {
    #    "title": u"\uf03a",
    #    "value": "List Layers",
    #    "tooltip": { "content": "List Layers"},
    #    "wrapper": { "css": { "classes": [], "properties": [{ "name": "flex-grow", "value": "0"}] } },
    #    "css": {
    #        "classes": [""],
    #        "properties": [
    #            { "name": "font-size", "value": "20px" },
    #            { "name": "font-family", "value": "FontAwesome" },
    #            { "name": "border-radius", "value": "0px 0px 0px 0px"},
    #            { "name": "width", "value": "80px" },
    #            { "name": "flex-grow", "value": "0"},
    #            { "name": "line-height", "value": "48px"},
    #            { "name": "background", "value": "rgba(0, 0, 0, 0.8)" }
    #        ]
    #    },
    #    "link": { "url": "/layers", "target": "_top" }
    #}
    #tabs.append(tab)


    navbar_title = {
        "id": "toolbar",
        "placement": "top",
        "css" : {
          "classes": [""],
          "properties": [
              { "name": "left", "value": "0px" },
              { "name": "right", "value": "auto" }
          ]
        },
        "tabs":tabs
    }
    return navbar_title


def build_navbar_toolbar(geolocation=True):
    navbar_toolbar = {
      "id": "toolbar",
      "placement": "left",
      "css": {
          #"classes": ["hidden-sm-down"],
          "properties": [
              {"name": "top", "value": "6rem"}
          ]
      },
      "tabs": []
    }
    css = {
        "classes": [""],
        "properties": [
            { "name": "font-size", "value": "1.25rem" },
            { "name": "font-family", "value": "FontAwesome" },
            { "name": "background", "value": "rgba(0, 0, 0, 0.8)" }
        ]
    }
    navbar_toolbar['tabs'].append({
        "title": u"\uf00e",
        "value": "Zoom In",
        "tooltip": { "content": "Zoom in"},
        "css": css,
        "intents": [{"name": "zoomIn"}]
    })
    navbar_toolbar['tabs'].append({
        "title": u"\uf010",
        "value": "Zoom Out",
        "tooltip": { "content": "Zoom out"},
        "css": css,
        "intents": [{"name": "zoomOut"}]
    })
    if geolocation:
        navbar_toolbar['tabs'].append({
            "title": u"\uf124",
            "value": "Fly to Current Location",
            "tooltip": { "content": "Fly to Current Location"},
            "css": css,
            "intents": [{"name": "flyToCurrentLocation"}]
        })
        navbar_toolbar['tabs'].append({
            "title": u"\uf183",
            "value": "Show Current Location",
            "tooltip": { "content": "Show Current Location"},
            "css": css,
            "intents": [{"name": "toggleGeolocation"}]
        })
    navbar_toolbar['tabs'].append({
        "title": u"\uf0ac",
        "value": "Reset Extent",
        "tooltip": { "content": "Reset Extent"},
        "css": css,
        "intents": [
            {"name": "flyToExtent", "properties": [{"name": "extent", "value": "initial"}]}
        ]
    })

    return navbar_toolbar

def build_navbar_featurelayers(featurelayers=None):

    tabs = []

    tab = {
        "title": "Layers (Click on buttons below to toggle layers on/off)",
        "value": "all",
        #"tooltip": { "placement": "left", "content": layer.title },
        "css": {
            "properties": [
              #{ "name": "font-size", "value": "1rem" },
              #{ "name": "font-family", "value": "FontAwesome" },
              { "name": "background", "value": "rgba(0, 0, 0, 0.8)" },
              { "name": "border-radius", "value": "0px 0px 0px 0px" },
              { "name": "border-top", "value": "8px solid rgb(97, 153, 142)" }

            ]
        },
        "wrapper": {
            "css": {
                "classes": ["col-12"]
            }
        }
    }
    tabs.append(tab)

    for fl in featurelayers:
        tabs.append({
            "title": fl["title"],
            "value": fl["id"],
            #"tooltip": { "placement": "left", "content": layer.title },
            "tooltip": { "placement": "top", "container": "body", "content": fl['description'] },
            "css": {
                "properties": [
                  #{ "name": "font-size", "value": "1rem" },
                  #{ "name": "font-family", "value": "FontAwesome" },
                  { "name": "background", "value": "rgba(0, 0, 0, 0.8)" },
                  { "name": "border-radius", "value": "0px 0px 0px 0px" }
                ]
            }
        })

    navbar_featurelayers = {
        "id": "layers",
        "placement": "bottom",
        "intents": [{
            "name": "toggleFeatureLayer",
            "properties": [{ "name": "layer", "value": "{{ tab.value }}"}]
        }],
        "css": {
            "properties": [
                #{ "name": "height", "value": "1rem" }
            ]
        },
        "markdown": False,
        "tabs": tabs
    }

    return navbar_featurelayers

def build_navbar_categories():

    tabs = []

    tab = {
        "title": "Categories (Select a category below)",
        "value": "all",
        "css": {
            "properties": [
              { "name": "background", "value": "rgba(0, 0, 0, 0.8)" },
              { "name": "border-radius", "value": "0px 0px 0px 0px" },
              { "name": "border-top", "value": "8px solid rgb(97, 153, 142)" }
            ]
        },
        "wrapper": {
            "css": {
                "classes": ["col-12"]
            }
        }
    }
    tabs.append(tab)

    count = Layer.objects.all().count()
    tab = {
        "title": "All Layers ("+str(count)+")",
        "value": "all",
        #"tooltip": { "placement": "left", "content": layer.title },
        "css": {
            "properties": [
              #{ "name": "font-size", "value": "1rem" },
              #{ "name": "font-family", "value": "FontAwesome" },
              { "name": "background", "value": "rgba(0, 0, 0, 0.8)" },
              { "name": "border-radius", "value": "0px 0px 0px 0px" }
            ]
        },
        "link": {
            "url": reverse('viewer')+"?main:config="+reverse('dashboard_config_all'),
            "target": "_self"
        }
    }
    tabs.append(tab)

    for category in TopicCategory.objects.all().order_by("identifier"):
        count = Layer.objects.filter(category__identifier=category.identifier).count()
        if count > 0:
            tab = {
                "title": category.gn_description +" ("+str(count)+")",
                "value": category.identifier,
                "tooltip": { "placement": "top", "container": "body", "content": category.description },
                "css": {
                    "properties": [
                      #{ "name": "font-size", "value": "1rem" },
                      #{ "name": "font-family", "value": "FontAwesome" },
                      { "name": "background", "value": "rgba(0, 0, 0, 0.8)" },
                      { "name": "border-radius", "value": "0px 0px 0px 0px" }
                    ]
                },
                "link": {
                    "url": reverse('viewer')+"?main:config="+reverse('dashboard_config_category', args=[category.identifier]),
                    "target": "_self"
                }
            }
            tabs.append(tab)

    navbar_categories = {
        "id": "categories",
        "placement": "bottom",
        "css": {
            "properties": [
                #{ "name": "height", "value": "1rem" }
            ]
        },
        "markdown": False,
        "tabs": tabs
    }
    return navbar_categories

def build_baselayers():
    baselayers = []

    bl = {
        "id": "osm",
        "title": "OpenStreetMap",
        "description": "OpenStreetMap Basemap, Standard Style",
        "type": "tiles",
        "source": {
            "attribution": '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            "name": "OpenStreetMap"
        },
        "tile": {
            "url": "https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        }
    }

    baselayers.append(bl)

    return baselayers

def build_featurelayers(category=None):
    featurelayers = []
    site = Site.objects.get_current()

    layers = None
    if category:
        layers = Layer.objects.filter(category__identifier=category).order_by('title')
    else:
        layers = Layer.objects.all().order_by('title')

    for layer in layers:
        popupTitle = None
        attrNames = []
        popupFields = []
        for attr in layer.attribute_set.exclude(attribute='the_geom'):
            if attr.attribute not in ["other_tags"]:
                attrName = attr.attribute
                attrNames.append(attrName)
                if attrName == "osm_id":
                    popupField = {
                        "type": "link",
                        "attribute": attrName,
                        "label": attr.attribute_label or attrName,
                        "when": "defined",
                        "value": "{{ feature.attributes."+attrName+" }}",
                        "url": "http://www.openstreetmap.org/node/{{ feature.attributes.osm_id}}"
                    }
                else:
                    popupField = {
                        "attribute": attr.attribute,
                        "label": attr.attribute_label or attrName,
                        "when": "defined"
                    }

                popupFields.append(popupField)

        popupField = {
            "type": "link",
            "attribute": attrName,
            "label": "Download",
            "value": "{{ layer.title }}",
            "url": "/layers/{{ layer.id }}"
        }
        popupFields.append(popupField)

        if popupTitle is None:
            for attrName in ["name", "name_long", "name_shrt"]:
                if attrName in attrNames:
                    popupTitle = layer.title+": {{ feature.attributes. "+attrName+" }}"

        if popupTitle is None:
            popupTitle = layer.title

        fl = {
            "id": layer.typename,
            "type": "WMS",
            "title": layer.title,
            "description": layer.abstract,
            "source": {
                "name": site.name,
                "attribution": site.name,
                "site": site.name
            },
            "wms": {
                "layers": [layer.typename],
                "url": "/geoserver/wms"
            },
            "wfs": {
                "layers": [layer.typename],
                "url": "/geoserver/wfs",
                "version": "1.0.0"
            },
            "popup": {
                "title": popupTitle,
                "panes": [{
                    "id": "overview",
                    "tab": { "label": "Overview" },
                    "fields": popupFields
                }]
            }
        }
        featurelayers.append(fl)
    return featurelayers
