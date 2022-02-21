from .models import  *


def get_user(request):
    student_id = request.session.get("student_id", None)
    if student_id:
        return Student.objects.get(pk=student_id)

    provost_email = request.session.get("provost_email", None)
    if provost_email:
        return Provost.objects.get(email=provost_email)

    return None


def fill_context(request, context):
    student_id = request.session.get("student_id", None)
    if student_id:
        context["user"] = Student.objects.get(pk=student_id)
        context["notifications"] = Notification.objects.filter(studentID=student_id)
        context["is_student"] = True
        context["is_provost"] = False
    else:
        provost_email = request.session.get("provost_email", None)
        if provost_email:
            context["user"] = Provost.objects.get(email=provost_email)
            context["is_student"] = False
            context["is_provost"] = True


def log_out(request):
    print("Log out: ", str(get_user(request)))
    try:
        del request.session['student_id']
    except KeyError:
        pass

    try:
        del request.session['provost_email']
    except KeyError:
        pass

    return False


def is_logged_in(request):
    if request.session.get("student_id", None):
        return True
    if request.session.get("provost_email", None):
        return True
    return False


# return provost object if success
def login_user_provost(request, provost_email, provost_password):
    try:
        provost = Provost.objects.get(email=provost_email)
        if provost and provost.password == provost_password:
            request.session['provost_email'] = provost_email
            return provost
    except Exception as e:
        print('provost authentication error')
    return None


# return student object if success
def login_user_student(request, student_id, student_password):
    try:
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
    except Exception as e:
        print("no such student ")

    return None

