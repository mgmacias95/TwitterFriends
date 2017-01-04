# script python para crear relaciones entre los usuarios almacenados
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "TwitterFriends.settings")
import django
django.setup()
import tweepy
import time     # to sleep when it exceeds the max number of calls to the api
from findfriends.models import TwitterUser

n_calls = 0 # parameter to control the number of calls to the twitter api

# function to save frienship on database
def create_frienship(friends, userid):
    user = TwitterUser.objects.get(user_id=userid)
    print("Saving ", user.screen_name, "'s friends")
    for friend in friends:
        if TwitterUser.objects.filter(user_id=friend).exists():
            u = TwitterUser.objects.get(user_id=friend)
            print(u.screen_name, " is friend of ", user.screen_name)
            user.friends.add(u)

# Las claves de acceso a twitter están definidas como variables de entorno
auth = tweepy.OAuthHandler(environ["TWITTER_CONSUMER_KEY"], 
                           environ["TWITTER_CONSUMER_SECRET"])
auth.set_access_token(environ["TWITTER_ACCESS_TOKEN"], 
                      environ["TWITTER_ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)

me = api.me()

# guardamos los amigos del usuario identificado
amigos = api.friends_ids(user_id=me.id)
create_frienship(friends=amigos, userid=me.id)
# guardamos los amigos de los amigos del usuario identificado
for amigo in amigos:
    if TwitterUser.objects.filter(user_id=amigo).exists():
        n_calls += 1
        if n_calls > 13*180:
            print("About to exceed max number of calls")
            time.sleep(16*60) # sleep 15+1 minutes
            n_calls = 0

        create_frienship(friends=api.friends_ids(user_id=amigo), userid=amigo)
