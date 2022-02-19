
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from .models import *
from .forms import *
from .AuthHelper import *
from django.urls import reverse
from django.db.models import F
from django.views import View


class ProvostHomeView(View):
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        if get_user(request):
            context = {}
            fill_context(request, context)
            return render(request, 'RoomAllotment/provost_profile.html',context)
        return Http404("You are not logged in.")


class ProvostRoomAllotView(View):
    # TODO check if logged in
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        if get_user(request):
            applications = RoomAllotmentRequest.objects.all()
            return render(request, 'RoomAllotment/room_provostSide.html',{"Requests":applications})
        return Http404("You are not logged in.")
