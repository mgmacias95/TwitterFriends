from django.http import HttpResponse
from django.template import loader
from .netjson_serializer import generate_net_json


def index(request):
    netjson = generate_net_json()
    template = loader.get_template('findfriends/index.html')
    context = {
        'netjson': netjson,
    }
    return HttpResponse(template.render(context, request))
