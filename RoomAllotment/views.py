from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from .models import *
from .forms import *
from .AuthHelper import *
from django.urls import reverse
from django.db.models import F


from django.views import View

class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {"loggedIn": is_logged_in(request) }
        if context["loggedIn"]:
            fill_context(request, context)
            user = context["user"]
            context["profileUrl"] = f'student/{user.stdID}' if user.is_student() else f'provost/{user.provostID}'
        return render(request, 'RoomAllotment/home_page.html', context)
                                                    

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
            return Http404("Not Logged in")


class ProvostHomeView(View):
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        if get_user(request):
            context = {}
            fill_context(request, context)
            return render(request, 'RoomAllotment/provost_profile.html',context)
        return Http404("You are not logged in.")


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if is_logged_in(request):
            return Http404("already logged in")
        return render(request, 'RoomAllotment/login.html')

    def post(self, request, *args, **kwargs):
        if is_logged_in(request):
            return Http404("already logged in")

        form = LoginForm(request.POST)
        if form.is_valid():
            form.clean()
            user_identifier = form.cleaned_data['userIdentifier']
            password = form.cleaned_data['password']
            try:
                student_id = int(user_identifier)
                if login_user_student(request, student_id, password):
                    student_object = get_user(request)
                    print("student login", student_object)
                    return HttpResponseRedirect(reverse('student-home', args=[student_object.stdID]))
                else:
                    print("student login fail but userID is integer", form.cleaned_data)
                    return HttpResponse("provost login fail")
            except ValueError:
                # assume that this is provost login since userID != int
                if login_user_provost(request, user_identifier, password):
                    provost_object = get_user(request)
                    print("provost login", provost_object)
                    return HttpResponseRedirect(reverse('provost-home', args=[provost_object.provostID]))
                else:
                    print("provost login fail", form.cleaned_data)
                    return HttpResponse("provost login fail")
        else:
            print("form had errors")
            return HttpResponse(form.errors)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if not is_logged_in(request):
            return Http404("not logged in")

        log_out(request)
        return HttpResponseRedirect(reverse('login'))


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
            # TODO hook rooms

            return render(request, 'RoomAllotment/room.html', context)
        else:
            return Http404("Not Logged in")


    def post(self, request, *args, **kwargs):
        # TODO validate room is empty?
        std_id = kwargs['std_id']
        context = {"loggedIn": is_logged_in(request)}
        
        if context["loggedIn"]:
            fill_context(request, context)
            if (not context["is_student"]) or (context["user"].stdID != std_id):
                return Http404("Not logged in")

            form = RoomAllotmentRequestForm(request.POST)

            if form.is_valid():
                form.stdID = std_id
                print(form.cleaned_data)

                room_request = form.save(commit=False)
                room_request.stdID = context["user"]

                room_request.save()

            else:
                print(form.errors)
                return HttpResponseRedirect(reverse('student-room-req', args=[context["user"].stdID]))

            return HttpResponseRedirect(reverse('student-home', args=[context["user"].stdID]))
            
        else:
            return Http404("Not Logged in")


class ProvostRoomAllotView(View):
    # TODO check if logged in
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        if get_user(request):
            applications = RoomAllotmentRequest.objects.all()
            return render(request, 'RoomAllotment/room_provostSide.html',{"Requests":applications})
        return Http404("You are not logged in.")
        

def request_form(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RoomAllotmentRequestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect('/RoomAllotment/requests/')
        # TODO SHOW ERROR
    else:
        form = RoomAllotmentRequestForm()
        context = {'form': form}
        return render(request, 'polls/Request-Create-Form.html', context)


def request_detail(request, request_id):
    try:
        request = RoomAllotmentRequest.objects.get(pk=request_id)
    except RoomAllotmentRequest.DoesNotExist:
        raise Http404("Request does not exist")
    return render(request, 'polls/Request-Detail.html', {'request': request})




