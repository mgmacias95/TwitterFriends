# script python para guardar en la base de datos los datos de twitter que nos 
# interesan
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "TwitterFriends.settings")
import django
django.setup()
import tweepy
import time     # to sleep when it exceeds the max number of calls to the api
from findfriends.models import TwitterUser

n_calls = 0 # parameter to control the number of calls to the twitter api

# función para obtener los amigos de un determinado usuario y guardarlos en
# la base de datos.
def save_user(user):
    if not TwitterUser.objects.filter(user_id=user.id).exists():
        print("Saving: ",user.screen_name)
        u = TwitterUser()
        u.user_id = user.id
        u.screen_name = user.screen_name
        u.is_verified = user.verified
        u.location = user.location
        # u.friends = None
        u.save()
    else:
        print(user.screen_name, " is already on the data base")


def get_and_save_friends(user_id):
    global n_calls
    for friend in tweepy.Cursor(api.friends, user_id=user_id, count=200).items():
        n_calls += 1
        if n_calls > 13*199:
            print("About to exceed max number of calls")
            time.sleep(60*15) # wait 15 minutes
            n_calls = 0
        else:
            save_user(friend)


# Las claves de acceso a twitter están definidas como variables de entorno
auth = tweepy.OAuthHandler(environ["TWITTER_CONSUMER_KEY"], 
                           environ["TWITTER_CONSUMER_SECRET"])
auth.set_access_token(environ["TWITTER_ACCESS_TOKEN"], 
                      environ["TWITTER_ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth)

# guardamos el objeto usuario del usuario identificado en la base de datos
me = api.me()
save_user(me)
# guardamos sus amigos y los amigos de sus amigos en la base de datos
get_and_save_friends(user_id=me.id)
amigos = api.friends_ids(user_id=me.id)
for amigo in amigos:
    get_and_save_friends(user_id=amigo)

