# script python para guardar en la base de datos los datos de twitter que nos 
# interesan
from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "TwitterFriends.settings")
import django
django.setup()
import tweepy
from findfriends.models import TwitterUser

# función para obtener los amigos de un determinado usuario y guardarlos en
# la base de datos.
def save_user(user):
    print("Saving: ",user.screen_name)
    u = TwitterUser()
    u.user_id = user.id
    u.screen_name = user.screen_name
    u.is_verified = user.verified
    u.location = user.location
    u.friends = api.friends_ids(user_id=user.id)
    u.save()

def get_and_save_friends(user_id):
    for friend in tweepy.Cursor(api.friends, user_id=user_id).items():
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
amigos = TwitterUser.objects.filter(pk=me.id).friends
for amigo in amigos:
    get_and_save_friends(user_id=amigo)

