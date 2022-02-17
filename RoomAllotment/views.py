from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from .models import *
from .forms import *

from django.views import View

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Home view')

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

