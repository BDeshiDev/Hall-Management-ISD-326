
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

            room_assigned = False
            sortCrit = request.GET.get('sort', None)

            if sortCrit:
                rooms = Room.objects.filter(vacantSeats__gt = 0)

                if sortCrit == 'seniority':
                    applications = assignRoomsBySeniority(applications, rooms)
                    room_assigned = True
                elif sortCrit == 'cgpa':
                    applications = assignRoomsByCgpa(applications, rooms)
                    room_assigned = True
                elif sortCrit == 'address':
                    applications = assignRoomsByAddress(applications, rooms)
                    room_assigned = True
                elif sortCrit == 'eca':
                    applications = assignRoomsByEca(applications, rooms)
                    room_assigned = True


            return render(request, 'RoomAllotment/room_provostSide.html',{"Requests": applications, "room_assigned": room_assigned})
        return Http404("You are not logged in.")


    def post(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        context = {"loggedIn": is_logged_in(request)}

        if context["loggedIn"]:
            fill_context(request, context)
            if not context["is_provost"]:
                return Http404("Not logged in")

            

        else:
            return Http404("Not logged in")




def assignRoomsBySeniority(applications, rooms):
    applications = sorted(applications, key = lambda a : (a.stdID.level, a.stdID.term, -a.RequestID))
    applications = reversed(applications)
    applications = list(applications)
    assignRooms(applications, rooms)
    return applications 

def assignRoomsByCgpa(applications, rooms):
    applications = sorted(applications, key = lambda a : (a.stdID.cgpa, -a.RequestID))
    applications = reversed(applications)
    applications = list(applications)
    assignRooms(applications, rooms)
    return applications

def assignRoomsByAddress(applications, rooms):
    applications = sorted(applications, key = lambda a : (1 if a.stdID.present_address != 'Dhaka' and a.stdID.permanent_address != 'Dhaka' else 0, -a.RequestID))
    applications = reversed(applications)
    applications = list(applications)
    assignRooms(applications, rooms)
    return applications

def assignRoomsByEca(applications, rooms):
    applications = sorted(applications, key = lambda a : (int(a.debate) + int(a.sports) + int(a.other), -a.RequestID))
    applications = reversed(applications)
    applications = list(applications)
    assignRooms(applications, rooms)
    return applications

def assignRooms(applications, rooms):
    for a in applications:
        a.possible_room_no = None

        for r in rooms:
            if r == a.requestedRoomNo and r.vacantSeats > 0:
                a.possible_room_no = r.RoomNo
                r.vacantSeats -= 1
                break

        if a.possible_room_no:
            continue

        for r in rooms:
            if r.vacantSeats > 0:
                a.possible_room_no = r.RoomNo
                r.vacantSeats -= 1
                break


        
    return 
