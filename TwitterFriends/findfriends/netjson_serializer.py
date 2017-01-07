# python script that creates the net from data
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "TwitterFriends.settings")
import django
django.setup()
from findfriends.models import TwitterUser

# function that generates a json to be represented on d3
def generate_net_json():
    net = {"nodes":[], "links":[]}
    for user in TwitterUser.objects.all():
        net["nodes"].append({"id": user.screen_name, "group":1})
        for friend in user.friends.all():
            net["links"].append({"source": user.screen_name,
                "target": friend.screen_name, "value":1})

    return net

# function that generates a gdf file to work on gephi
def generate_net_gdf():
    net = []
    # start with nodes
    net.append("nodedef>name VARCHAR,label VARCHAR,verified BOOLEAN,location VARCHAR")
    for user in TwitterUser.objects.all():
        net.append('{},{},{},{}'.format(user.user_id, user.screen_name, 
            user.is_verified, user.location))
    # then add edges
    net.append("edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN")
    for user in TwitterUser.objects.all():
        for friend in user.friends.all():
            net.append('{},{},true'.format(user.user_id, friend.user_id))

    return '\n'.join(net)
