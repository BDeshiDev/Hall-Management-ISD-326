
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


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if is_logged_in(request):
            return Http404("already logged in")
        return render(request, 'RoomAllotment/login.html')

    def post(self, request, *args, **kwargs):
        if is_logged_in(request):
            return Http404("already logged in")

        form = LoginForm(request.POST)
        isStudentLogin = request.POST["loginType"] == "Student"
        # print(request.POST)
        context = {}
        if form.is_valid():
            form.clean()
            print(form.cleaned_data)
            user_identifier = form.cleaned_data['userIdentifier']
            password = form.cleaned_data['password']

            # assume that this is provost login since userID != int
            if isStudentLogin:
                try:
                    student_id = int(user_identifier)
                    if login_user_student(request, student_id, password):
                        student_object = get_user(request)
                        print("student login", student_object)
                        return HttpResponseRedirect(reverse('student-home', args=[student_object.stdID]))
                    else:
                        context["Error"] = "Student Authentication Error"
                        # return HttpResponse(form.errors)
                        return render(request, 'RoomAllotment/login.html', context)
                except ValueError:
                    context["Error"] = "Student ID Error"
                    # return HttpResponse(form.errors)
                    return render(request, 'RoomAllotment/login.html', context)
            else:
                if login_user_provost(request, user_identifier, password):
                    provost_object = get_user(request)
                    print("provost login", provost_object)
                    return HttpResponseRedirect(reverse('provost-home', args=[provost_object.provostID]))
                else:
                    context["Error"] = "Provost Authentication Error"
                    # return HttpResponse(form.errors)
                    return render(request, 'RoomAllotment/login.html', context)

        else:
            print("form had errors")
            context["Error"] = "Authentication Error"
            # return HttpResponse(form.errors)
            return render(request, 'RoomAllotment/login.html', context)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if not is_logged_in(request):
            return Http404("not logged in")

        log_out(request)
        return HttpResponseRedirect(reverse('login'))
