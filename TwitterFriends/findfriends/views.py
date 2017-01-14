from django.http import HttpResponse, JsonResponse
from django.template import loader
from .netjson_serializer import *
# para el formulario
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import WholeNetForm

whole_net = False

def netgdf(request):
    global whole_net
    net = generate_net_gdf(whole_net)
    return HttpResponse(net, content_type='text/plain')

def netjson(request):
    global whole_net
    net = generate_net_json(whole_net)
    return JsonResponse(net)

def netnet(request):
    global whole_net
    net = generate_net_net(whole_net)
    return HttpResponse(net, content_type='text/plain')

def netgml(request):
    global whole_net
    net = generate_net_gml(whole_net)
    return HttpResponse(net, content_type='text/plain')

def get_whole_net(request):
    if request.method == 'POST':
        whole = WholeNetForm(request.POST)
        whole_net = whole.make_whole_net
    else:
        whole = WholeNetForm()
    return render(request, 'findfriends/index.html', {'form': whole})


def index(request):
    # netjson = generate_net_json()
    template = loader.get_template('findfriends/index.html')
    context = {
        # 'netjson': netjson,
    }
    return HttpResponse(template.render(context, request))
