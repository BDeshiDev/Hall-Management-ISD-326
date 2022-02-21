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
        fields = ["requestedRoomNo", "attachment", "message", "sports", "debate", "other"]


class RoomAllotForm(forms.Form):
    room_no = forms.IntegerField(label='room_no', required=False)
    student_id = forms.IntegerField(label='student_id', required=False)
    sortCrit = forms.CharField(label='sortCrit', max_length=20, required=False)
    action = forms.CharField(label='action', max_length=20)
