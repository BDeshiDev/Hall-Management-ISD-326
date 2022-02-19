
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

            # TODO send these free room list too
            rooms = Room.objects.filter(vacantSeats__gt = 0)

            return render(request, 'RoomAllotment/provost_profile.html',context)
        return Http404("You are not logged in.")


class ProvostRoomAllotView(View):
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        if get_user(request):
            applications = RoomAllotmentRequest.objects.filter(approvalStatus__exact = RoomAllotmentRequest.PENDING)

            assignments = {}
            sortCrit = request.GET.get('sort', None)

            if sortCrit:
                rooms = Room.objects.filter(vacantSeats__gt = 0)

                if sortCrit == 'seniority':
                    applications, assingments = assignRoomsBySeniority(applications, rooms)
                elif sortCrit == 'cgpa':
                    pass
                elif sortCrit == 'address':
                    pass:
                elif sortCrit == 'eca':
                    pass:


            return render(request, 'RoomAllotment/room_provostSide.html',{"Requests":applications, "assignments": assignments})
        return Http404("You are not logged in.")




def assignRoomsBySeniority(applications, rooms):
    applications = sorted(applications, key = lambda a : (a.stdID.level * 10 + a.stdID.term))
    applications = reversed(applications)
    return applications, {}


def assignRoomsByCgpa(applications, rooms):
    #TODO
    applications = sorted(applications, key = lambda a : (a.stdID.level * 10 + a.stdID.term))
    applications = reversed(applications)
    return applications, {}


def assignRoomsByAddress(applications, rooms):
    #TODO
    applications = sorted(applications, key = lambda a : (a.stdID.level * 10 + a.stdID.term))
    applications = reversed(applications)
    return applications, {}


def assignRoomsByEca(applications, rooms):
    #TODO
    applications = sorted(applications, key = lambda a : (a.stdID.level * 10 + a.stdID.term))
    applications = reversed(applications)
    return applications, {}

