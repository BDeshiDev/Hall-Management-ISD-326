from  .models import *
from django.forms import ModelForm


class RoomAllotmentRequestForm(ModelForm):
    class Meta:
        model = RoomAllotmentRequest
        exclude = ['RequestID']