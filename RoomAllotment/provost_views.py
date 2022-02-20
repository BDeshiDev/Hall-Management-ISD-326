
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from .models import *
from .forms import *
from .AuthHelper import *
from .room_suggestion import *
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

            form = RoomAllotForm(request.POST)
            if form.is_valid():
                form.clean()
                student_id = form.cleaned_data['student_id']
                room_no = form.cleaned_data['room_no']


                student = Student.objects.get(pk=student_id)
                old_room = student.roomNo

                application = RoomAllotmentRequest.objects.filter(stdID__exact = student)[0]
                print(application)

                if room_no is None:
                    application.approvalStatus = RoomAllotmentRequest.DECLINED
                    application.save()
                else:
                    room = Room.objects.get(pk=room_no)

                    if old_room is not None:
                        old_room.vacantSeats += 1
                    
                    student.roomNo = room
                    room.vacantSeats -= 1
                    application.approvalStatus = RoomAllotmentRequest.ACCEPTED 

                    student.save()
                    room.save()
                    if old_room is not None:
                        old_room.save()
                    application.save()

                return HttpResponseRedirect(reverse('provost-room-allot', args=[prv_id]))
            else:
                print(form.errors)
                return Http404("wrong form")
        else:
            return Http404("Not logged in")


