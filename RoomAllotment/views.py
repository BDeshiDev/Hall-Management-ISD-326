from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from .models import *
from .forms import *

from django.views import View



class HomeView(View):
    pass

class StudentHomeView(View):
    pass

class ProvostHomeView(View):
    pass

class LoginView(View):
    pass

class StudentRoomReqView(View):
    pass

class ProvostRoomAllotView(View):
    pass


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

