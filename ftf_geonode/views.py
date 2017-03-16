import yaml

try:
    import simplejson as json
except ImportError:
    import json

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse

def dashboard_config(request, id):
    return HttpResponse(json.dumps(yaml.load(get_template("dashboards/"+id+".yml").render({}))), content_type='application/json')
