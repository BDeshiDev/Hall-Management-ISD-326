from .models import  *


def get_user(request):
    student_id = request.session.get("student_id", None)
    if student_id:
        return Student.objects.get(pk=student_id)

    provost_name = request.session.get("provost_name", None)
    if provost_name:
        return Provost.objects.get(name=provost_name)

    return None


def fill_context(request, context):
    student_id = request.session.get("student_id", None)
    if student_id:
        context["user"] = Student.objects.get(pk=student_id)
        context["notifications"] = Notification.objects.filter(studentID=student_id)
        context["is_student"] = True
        context["is_provost"] = False
    else:
        provost_name = request.session.get("provost_name", None)
        if provost_name:
            context["user"] = Provost.objects.get(name=provost_name)
            context["is_student"] = False
            context["is_provost"] = True


def log_out(request):
    print("Log out: ", str(get_user(request)))
    try:
        del request.session['student_id']
    except KeyError:
        pass

    try:
        del request.session['provost_name']
    except KeyError:
        pass

    return False


def is_logged_in(request):
    if request.session.get("student_id", None):
        return True
    if request.session.get("provost_name", None):
        return True
    return False


# return provost object if success
def login_user_provost(request, provost_name, provost_password):
    provost = Provost.objects.get(name=provost_name)
    if provost and provost.password == provost_password:
        request.session['provost_name'] = provost_name
        return provost
    return None


# return student object if success
def login_user_student(request, student_id, student_password):
    student = Student.objects.get(pk=student_id)
    if student:
        if student.password == student_password:
            # model is a db thing
            # can't store in this dictionary
            # store id instead
            request.session['student_id'] = student_id
            return student
        else:
            print("Student Password mismatch ", student.password, str(student.password))
    else:
        print("no such student ")

    return None

