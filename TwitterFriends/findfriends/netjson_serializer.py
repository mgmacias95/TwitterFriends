#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python script that creates the net from data
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "TwitterFriends.settings")
import django
django.setup()
from findfriends.models import TwitterUser

# function that generates a json to be represented on d3
def generate_net_json(whole_net):
    net = {"nodes":[], "links":[]}
    if not whole_net:
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
    else:
        for user in TwitterUser.objects.all():
            net["nodes"].append({"id": user.screen_name, "group":1})
            for friend in user.friends.all():
                net["links"].append({"source": u.screen_name, 
                    "target":friend.screen_name, "value":1})

    return net

# function that generates a gdf file to work on gephi
def generate_net_gdf(whole_net):
    net = []
    # start with nodes
    net.append("nodedef>name VARCHAR,label VARCHAR,verified BOOLEAN,location VARCHAR")
    if not whole_net:
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
    
    
        for user in u.friends.all():
            # we get the friends in common
            common_f = user.friends.filter(friends__in=u.friends.all()).distinct()
            for friend in common_f:
                net.append('{},{},true'.format(user.user_id, friend.user_id))
    else:
        for user in TwitterUser.objects.all():
            net.append('{},{},{},\'{}\''.format(user.user_id, user.screen_name, 
                user.is_verified, user.location))

        # then add edges
        net.append("edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN")

        for user in TwitterUser.objects.all():
            # we get the whole net
            for friend in user.friends.all():
                net.append('{},{},true'.format(user.user_id, friend.user_id))

    return '\n'.join(net)

# function that generates a gml file to work on gephi
def generate_net_gml(whole_net):
    net = []
    # start with nodes
    net.append("graph\n[\n")
    if not whole_net:
        u = TwitterUser.objects.first()
        # net.append('\tnode\n\t[\n\t\tid {}\n\t\tlabel \"{}\"\n\t]\n'.format(
        #     u.user_id, u.screen_name))

        for user in u.friends.all():
            net.append('\tnode\n\t[\n\t\tid {}\n\t\tlabel \"{}\"\n\t]\n'.format(
                user.user_id, user.screen_name))

        # then add edges
        # for friend in u.friends.all():
        #     net.append('\tedge\n\t[\n\t\tsource {}\n\t\ttarget {}\n\t]\n'.format(
        #         u.user_id, friend.user_id))
    
    
        for user in u.friends.all():
            # we get the friends in common
            common_f = user.friends.filter(friends__in=u.friends.all()).distinct()
            for friend in common_f:
                if friend.screen_name != u.screen_name:
                    net.append('\tedge\n\t[\n\t\tsource {}\n\t\ttarget {}\n\t]\n'.format(
                        user.user_id, friend.user_id))

    else:
        for user in TwitterUser.objects.all():
            net.append('\tnode\n\t[\n\t\tid {}\n\t\tlabel \"{}\"\n\t]\n'.format(
                user.user_id, user.screen_name))

        # then add edges

        for user in TwitterUser.objects.all():
            # we get the whole net
            for friend in user.friends.all():
                net.append('\tedge\n\t[\n\t\tsource {}\n\t\ttarget {}\n\t]\n'.format(
                    user.user_id, friend.user_id))

    net.append("]")

    return '\n'.join(net)

# function that generates a gdf file to work on gephi
def generate_net_net(whole_net):
    net = []
    keys = {}
    counter = 1
    # start with nodes
    if not whole_net:
        u = TwitterUser.objects.first()
        net.append("*Vertices "+str(u.friends.count()+1))
        net.append('{} \"{}\"'.format(counter, u.screen_name))
        keys[u.screen_name] = counter
        counter += 1

        for user in u.friends.all():
            net.append('{} \"{}\"'.format(counter, user.screen_name))
            keys[user.screen_name] = counter
            counter += 1

        # then add edges
        net.append("*Edges")

        for friend in u.friends.all():
            net.append('{} {}'.format(keys[u.screen_name], keys[friend.screen_name]))
    
    
        for user in u.friends.all():
            # we get the friends in common
            common_f = user.friends.filter(friends__in=u.friends.all()).distinct()
            for friend in common_f:
                net.append('{} {}'.format(keys[user.screen_name], keys[friend.screen_name]))
    else:
        net.append("*Vertices "+str(TwitterUser.objects.count()))
        for user in TwitterUser.objects.all():
            net.append('{} \"{}\"'.format(counter, user.screen_name))
            keys[user.screen_name] = counter
            counter += 1

        # then add edges
        net.append("*Edges")

        for user in TwitterUser.objects.all():
            # we get the whole net
            for friend in user.friends.all():
                net.append('{} {}'.format(keys[user.screen_name], keys[friend.screen_name]))

    return '\n'.join(net)
