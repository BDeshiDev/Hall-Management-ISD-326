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
        #return HttpResponse('Home view')
        return render(request, 'RoomAllotment/home_page.html')

class StudentHomeView(View):
    def get(self, request, *args, **kwargs):
        std_id = kwargs['std_id']
        return HttpResponse(f'Studnet home view {std_id}')

class ProvostHomeView(View):
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        return HttpResponse(f'provost home view {prv_id}')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('login view')

class StudentRoomReqView(View):
    def get(self, request, *args, **kwargs):
        std_id = kwargs['std_id']
        return HttpResponse(f'student room request view {std_id}')

class ProvostRoomAllotView(View):
    def get(self, request, *args, **kwargs):
        prv_id = kwargs['prv_id']
        return HttpResponse(f'provost room allotment view {prv_id}' )

def view_requests(request):
    requests = RoomAllotmentRequest.objects.all()
    context = {'requests': requests}
    return render(request, 'polls/View-Requests.html', context)


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


def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.clean()
            print("login form: " + str(form.cleaned_data))

            user_identifier = form.cleaned_data['userIdentifier']
            password = form.cleaned_data['password']

            try:
                student_id = int(user_identifier)
                if login_user_student(request, student_id, password):
                    print("student login", get_user(request))

                    return HttpResponseRedirect(reverse('home'))
                else:
                    print("student login fail but userID is integer", form.cleaned_data)
                    return HttpResponse("provost login fail")
            except ValueError:
                # assume that this is provost login since userID != int
                if login_user_provost(request, user_identifier, password):
                    print("provost login",  get_user(request))
                    return HttpResponseRedirect(reverse('home'))
                else:
                    print("provost login fail", form.cleaned_data)
                    return HttpResponse("provost login fail")
        else:
            print("form fail")
            print(form.errors)
            return HttpResponse(form.errors)
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'polls/login.html', context)


def logout(request):
    log_out(request)
    return HttpResponseRedirect('/login')


def home(request):
    user = get_user(request)

    if user:
        context = {}
        fill_context(request, context)
        return render(request, 'polls/home.html', context)
    else:
        HttpResponseRedirect('/login')





