from  .models import *
from django import forms
from django.forms import ModelForm


# using form class  cuz crispy forms
class LoginForm(forms.Form):
    userIdentifier = forms.CharField(label='User', max_length=100)
    password = forms.CharField(label='Password', max_length=100)


class RoomAllotmentRequestForm(ModelForm):
    class Meta:
        model = RoomAllotmentRequest
        fields = ["requestedRoomNo", "attachment", "message", "sports", "debate", "other_skill"]
