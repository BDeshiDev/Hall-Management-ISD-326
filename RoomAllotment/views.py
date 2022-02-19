from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from .models import *
from .forms import *
from .AuthHelper import *
from django.urls import reverse

from django.views import View

class HomeView(View):
    def get(self, request, *args, **kwargs):

        context = {"loggedIn": is_logged_in(request) }
        if context["loggedIn"]:
            user = get_user(request)
            context["profileUrl"] = f'student/{user.stdID}' if user.is_student() else f'provost/{user.provostID}'

        return render(request, 'RoomAllotment/home_page.html', context)

class StudentHomeView(View):
    def get(self, request, *args, **kwargs):
        if not is_logged_in(request):
            return HttpResponseRedirect(reverse('home'))
        
        user = get_user(request)
        if not user.is_student():
            return HttpResponseRedirect(reverse('home'))

        std_id = kwargs['std_id']

        if user.stdID != std_id:
            return HttpResponseRedirect(reverse('home'))


        context = {
            "name" : user.name,
            "cgpa" : user.cgpa,
            "student_id" : user.stdID,
            "mobile_no" : user.mobile_no,
            "level" : user.level,
            "term" : user.term,
            "present_address" : user.present_address,
            "permanent_address" : user.permanent_address,
            "email" : user.email,
            "department" : user.department,
            "roomNo" : user.roomNo,
        }

        return render(request, 'RoomAllotment/student_profile.html', context)

class ProvostHomeView(View):
    # TODO check if logged in
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        return render(request, 'RoomAllotment/provost_profile.html')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if is_logged_in(request):
            return HttpResponse("Already logged in")
        return render(request, 'RoomAllotment/login.html')

    def post(self, request, *args, **kwargs):
        if is_logged_in(request):
            return HttpResponse("Already logged in")
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
            return HttpResponseRedirect('home')

        log_out(request)
        return HttpResponseRedirect(reverse('login'))


class StudentRoomReqView(View):
    def get(self, request, *args, **kwargs):
        if not is_logged_in(request):
            return HttpResponseRedirect(reverse('home'))
        
        user = get_user(request)
        if not user.is_student():
            return HttpResponseRedirect(reverse('home'))

        std_id = kwargs['std_id']

        if user.stdID != std_id:
            return HttpResponseRedirect(reverse('home'))
        std_id = kwargs['std_id']

        # TODO get free rooms and return them

        return render(request, 'RoomAllotment/room.html');


    def post(self, request, *args, **kwargs):
        if not is_logged_in(request):
            return HttpResponseRedirect(reverse('home'))
        
        user = get_user(request)
        if not user.is_student():
            return HttpResponseRedirect(reverse('home'))

        std_id = kwargs['std_id']

        if user.stdID != std_id:
            return HttpResponseRedirect(reverse('home'))
        std_id = kwargs['std_id']


        # TODO create request

        return 
        

class ProvostRoomAllotView(View):
    # TODO check if logged in
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        return render(request, 'RoomAllotment/room_provostSide.html')


#def view_requests(request):
#    requests = RoomAllotmentRequest.objects.all()
#    context = {'requests': requests}
#    return render(request, 'polls/View-Requests.html', context)
#
#
#def request_form(request):
#    if request.method == 'POST':
#        # create a form instance and populate it with data from the request:
#        form = RoomAllotmentRequestForm(request.POST)
#        # check whether it's valid:
#        if form.is_valid():
#            print(form.cleaned_data)
#            form.save()
#            return HttpResponseRedirect('/RoomAllotment/requests/')
#        # TODO SHOW ERROR
#    else:
#        form = RoomAllotmentRequestForm()
#        context = {'form': form}
#        return render(request, 'polls/Request-Create-Form.html', context)
#
#
#def request_detail(request, request_id):
#    try:
#        request = RoomAllotmentRequest.objects.get(pk=request_id)
#    except RoomAllotmentRequest.DoesNotExist:
#        raise Http404("Request does not exist")
#    return render(request, 'polls/Request-Detail.html', {'request': request})

