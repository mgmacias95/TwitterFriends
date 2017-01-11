#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script that creates the net from data
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "TwitterFriends.settings")
import django
django.setup()
from findfriends.models import TwitterUser

# function that generates a json to be represented on d3
def generate_net_json():
    net = {"nodes":[], "links":[]}
    # we first add the authenticated user
    u = TwitterUser.objects.first()
    net["nodes"].append({"id": u.screen_name, "group":1})
    for friend in u.friends.all():
        net["links"].append({"source": u.screen_name, 
            "target":friend.screen_name, "value":1})

    # then, do the same with its friends
    for user in u.friends.all():
        net["nodes"].append({"id": user.screen_name, "group":1})
        # we get the friends in common
        common_f = user.friends.filter(friends__in=u.friends.all()).distinct()
        for friend in common_f:
            net["links"].append({"source": user.screen_name,
                "target": friend.screen_name, "value":1})

    return net

# function that generates a gdf file to work on gephi
def generate_net_gdf(whole_net = False):
    net = []
    # start with nodes
    net.append("nodedef>name VARCHAR,label VARCHAR,verified BOOLEAN,location VARCHAR")
    u = TwitterUser.objects.first()
    net.append('{},{},{},\'{}\''.format(u.user_id, u.screen_name, 
            u.is_verified, u.location))

    for user in u.friends.all():
        net.append('{},{},{},\'{}\''.format(user.user_id, user.screen_name, 
            user.is_verified, user.location))

    # then add edges
    net.append("edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN")
    
    for friend in u.friends.all():
        net.append('{},{},true'.format(u.user_id, friend.user_id))
    
    if not whole_net:
        for user in u.friends.all():
            # we get the friends in common
            common_f = user.friends.filter(friends__in=u.friends.all()).distinct()
            for friend in common_f:
                net.append('{},{},true'.format(user.user_id, friend.user_id))
    else:
        for user in u.friends.all():
            # we take the whole net with all users and links
            for friend in user.friends.all():
                net.append('{},{},true'.format(user.user_id, friend.user_id))

    return '\n'.join(net)
