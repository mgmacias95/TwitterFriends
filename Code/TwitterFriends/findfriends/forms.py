from django import forms
from .models import WholeNet

class WholeNetForm (forms.ModelForm):

    class Meta:
        model = WholeNet
        fields = ('make_whole_net',)
