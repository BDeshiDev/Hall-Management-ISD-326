from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from .models import *


def view_requests(request):
    requests = RoomAllotmentRequest.objects.all()
    context = {'requests': requests}
    return render(request, 'polls/View-Requests.html', context)


def request_detail(request, request_id):
    try:
        request = RoomAllotmentRequest.objects.get(pk=request_id)
    except RoomAllotmentRequest.DoesNotExist:
        raise Http404("Request does not exist")
    return render(request, 'polls/Request-Detail.html', {'request': request})

