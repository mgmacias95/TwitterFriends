# python script that creates the net from data
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "TwitterFriends.settings")
import django
django.setup()
from findfriends.models import TwitterUser
from json import dumps

def generate_net_json():
    net = {"nodes":[], "links":[]}
    for user in TwitterUser.objects.all():
        net["nodes"].append({"id": user.screen_name, "group":1})
        for friend in user.friends.all():
            net["links"].append({"source": user.screen_name,
                "target": friend.screen_name, "value":1})

    return dumps(net)
