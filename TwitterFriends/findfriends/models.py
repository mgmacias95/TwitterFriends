from django.db import models

# Como sólo queremos encontrar información sobre usuarios y relaciones entre 
# los mismos, sólo tendremos un modelo Usuario. Hay que tener en cuenta que
# estos datos se usarán para un análisis posterior, por tanto, es útil guardar
# información como la localización o si es cuenta verificada.

class TwitterUser(models.Model):
    # id numérico del usuario en twitter. Nos servirá para identificarlo en
    # la base de datos
    user_id = models.IntegerField(primary_key=True)
    # nombre de usuario en twitter (@...). No debe repetirse en la tabla
    screen_name = models.CharField(unique=True)
    # flag para saber si es una cuenta verificada
    is_verified = models.BooleanField()
    # localización del usuario
    location = models.CharField()
    # lista de amigos del usuario
    friends = models.ForeignKey('self', on_delete=models.CASCADE)
