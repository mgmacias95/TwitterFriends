# script python para crear relaciones entre los usuarios almacenados
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "TwitterFriends.settings")
import django
django.setup()
import tweepy
from findfriends.models import TwitterUser

# function to save frienship on database
def create_frienship(api, userid):
    user = TwitterUser.objects.get(user_id=userid)
    if len(user.friends.all()) == 0:
        friends = api.friends_ids(user_id=userid)
        print("Saving ", user.screen_name, "'s friends")
        for friend in friends:
            if TwitterUser.objects.filter(user_id=friend).exists():
                u = TwitterUser.objects.get(user_id=friend)
                print(u.screen_name, " is friend of ", user.screen_name)
                user.friends.add(u)
    else:
        print(user.screen_name, "'s friends are already saved")

# Las claves de acceso a twitter están definidas como variables de entorno
auth = tweepy.OAuthHandler(environ["TWITTER_CONSUMER_KEY"], 
                           environ["TWITTER_CONSUMER_SECRET"])
auth.set_access_token(environ["TWITTER_ACCESS_TOKEN"], 
                      environ["TWITTER_ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth_handler=auth, wait_on_rate_limit_notify=True, 
    wait_on_rate_limit=True)

me = api.me()

# guardamos los amigos del usuario identificado
amigos = api.friends_ids(user_id=me.id)
create_frienship(api=api, userid=me.id)
# guardamos los amigos de los amigos del usuario identificado
for amigo in amigos:
    if TwitterUser.objects.filter(user_id=amigo).exists():
        create_frienship(api=api, userid=amigo)
