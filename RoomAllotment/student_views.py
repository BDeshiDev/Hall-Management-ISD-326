
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render
from .models import *
from .forms import *
from .AuthHelper import *
from django.urls import reverse
from django.db.models import F
from django.views import View


class StudentHomeView(View):
    def get(self, request, *args, **kwargs):
        std_id = kwargs['std_id']
        context = {"loggedIn": is_logged_in(request)}
        
        if context["loggedIn"]:
            fill_context(request, context)
            if (not context["is_student"]) or (context["user"].stdID != std_id):
                return Http404("Not logged in")
            
            return render(request, 'RoomAllotment/student_profile.html', context)
        else:
            return HttpResponseNotFound("Not logged in")


class StudentRoomReqView(View):
    def get(self, request, *args, **kwargs):
        
        std_id = kwargs['std_id']
        context = {"loggedIn": is_logged_in(request)}
        
        if context["loggedIn"]:
            fill_context(request, context)
            if (not context["is_student"]) or (context["user"].stdID != std_id):
                return Http404("Not logged in")

            rooms = Room.objects.filter(vacantSeats__gt = 0)
            context["rooms"] = rooms

            return render(request, 'RoomAllotment/room.html', context)
        else:
            return HttpResponseNotFound("Not logged in")


    def post(self, request, *args, **kwargs):
        # TODO validate room is empty?
        std_id = kwargs['std_id']
        context = {"loggedIn": is_logged_in(request)}
        
        if context["loggedIn"]:
            fill_context(request, context)
            if (not context["is_student"]) or (context["user"].stdID != std_id):
                return HttpResponseNotFound("Not logged in")

            form = RoomAllotmentRequestForm(request.POST)

            if form.is_valid():
                form.stdID = std_id
                print(form.cleaned_data)

                room_request = form.save(commit=False)
                room_request.stdID = context["user"]

                old_request = RoomAllotmentRequest.objects.filter(stdID__exact = context["user"], approvalStatus__exact = RoomAllotmentRequest.PENDING)
                if len(old_request) > 0:
                    old_request = old_request[0]
                    old_request.requestedRoomNo = room_request.requestedRoomNo
                    old_request.attachment = room_request.attachment
                    old_request.message = room_request.message
                    old_request.sports = room_request.sports
                    old_request.debate = room_request.debate
                    old_request.other = room_request.other
                    old_request.save()
                  
                else:
                    room_request.save()

            else:
                print(form.errors)
                return HttpResponseRedirect(reverse('student-room-req', args=[context["user"].stdID]))

            return HttpResponseRedirect(reverse('student-home', args=[context["user"].stdID]))
            
        else:
            return HttpResponseNotFound("Not logged in")


class NotificationView(View):
    # TODO check if logged in
    def get(self, request, *args, **kwargs):
        std_id = kwargs['id']
        notif_id = kwargs['notifid']
        notification = Notification.objects.get(pk=notif_id)
        notification.isSeen()
        print(notification.notifURL,"--------------",notification.title)
        return HttpResponseRedirect(reverse(notification.notifURL, args=[std_id]))
