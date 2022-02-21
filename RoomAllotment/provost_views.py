
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404, HttpResponseNotFound
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

            return render(request, 'RoomAllotment/provost_profile.html', context)
        return Http404("You are not logged in.")


class ProvostRoomAllotView(View):
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        if get_user(request):
            context = {}
            fill_context(request, context)
            applications = RoomAllotmentRequest.objects.filter(approvalStatus__exact = RoomAllotmentRequest.PENDING)

            room_assigned = False
            sortCrit = request.GET.get('sort', '')

            if sortCrit:
                rooms = Room.objects.filter(vacantSeats__gt = 0)

                if sortCrit == 'seniority':
                    applications = suggestRoomsBySeniority(applications, rooms)
                    room_assigned = True
                elif sortCrit == 'cgpa':
                    applications = suggestRoomsByCgpa(applications, rooms)
                    room_assigned = True
                elif sortCrit == 'address':
                    applications = suggestRoomsByAddress(applications, rooms)
                    room_assigned = True
                elif sortCrit == 'eca':
                    applications = suggestRoomsByEca(applications, rooms)
                    room_assigned = True

            rooms = Room.objects.filter(vacantSeats__gt = 0)

            context['Requests'] = applications
            context['room_assigned'] = room_assigned
            context['sortCrit'] = sortCrit
            context['rooms'] = rooms
            
            return render(request, 'RoomAllotment/room_provostSide.html', context)
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

                if form.cleaned_data['action'] == 'apply':
                    student_id = form.cleaned_data['student_id']
                    room_no = form.cleaned_data['room_no']
                    if student_id == None:
                        return HttpResponseRedirect(reverse('provost-room-allot', args=[prv_id]))

                    assignRooms({student_id: room_no})

                elif form.cleaned_data['action'] == 'apply-all':
                    applications = RoomAllotmentRequest.objects.filter(approvalStatus__exact = RoomAllotmentRequest.PENDING)
                    rooms = Room.objects.filter(vacantSeats__gt = 0)

                    if form.cleaned_data['sortCrit'] == 'seniority':
                        applications = suggestRoomsBySeniority(applications, rooms)

                    elif form.cleaned_data['sortCrit'] == 'cgpa':
                        applications = suggestRoomsByCgpa(applications, rooms)

                    elif form.cleaned_data['sortCrit'] == 'address':
                        applications = suggestRoomsByAddress(applications, rooms)

                    elif form.cleaned_data['sortCrit'] == 'eca':
                        applications = suggestRoomsByEca(applications, rooms)

                    else:
                        return HttpResponseRedirect(reverse('provost-room-allot', args=[prv_id]))

                    assignRooms({a.stdID.stdID : a.possible_room_no for a in applications})

                return HttpResponseRedirect(reverse('provost-room-allot', args=[prv_id]))
            else:
                print(form.errors)
                return Http404("wrong form")
        else:
            return Http404("Not logged in")


class RoomApplicationBasicView(View):
    def get(self, request, *args, **kwargs):
        app_id = kwargs['app_id']
        if get_user(request):
            context = {}
            fill_context(request, context)

            if not context['is_provost']:
                return HttpResponseNotFound('You are not logged in')


            application = RoomAllotmentRequest.objects.get(pk=app_id)

            skills = []
            if application.sports:
                skills.append('sports')
            if application.debate:
                skills.append('debate')
            if application.other:
                skills.append('others')

            context['application'] = application
            context['skills'] = skills

            return render(request, 'RoomAllotment/see_applications.html', context)
        else:
            return HttpResponseNotFound('You are not logged in')


def assignRooms(assignments):
    for student_id, room_no in assignments.items():
        student = Student.objects.get(pk=student_id)
        old_room = student.roomNo

        application = RoomAllotmentRequest.objects.filter(stdID__exact = student, approvalStatus__exact = RoomAllotmentRequest.PENDING)[0]

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
    return
