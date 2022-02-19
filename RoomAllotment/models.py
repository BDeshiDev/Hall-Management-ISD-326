from pyexpat import model
from django.db import models
from django.utils import timezone


class Room(models.Model):
    RoomNo = models.IntegerField(primary_key=True)
    totalSeats = models.IntegerField(default=4)
    vacantSeats = models.IntegerField(default=4)


class Student(models.Model):
    stdID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100,default=123456)
    cgpa = models.FloatField(null=True)
    mobile_no = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(default=3)
    term = models.IntegerField(default=2)
    present_address = models.CharField(max_length=200,null=True, blank=True)
    permanent_address = models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(max_length=100,null=True, blank=True)
    department = models.CharField(max_length=100,default="CSE")  
    roomNo = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)
    

    # not sure if normal fields are okay in models
    # seems kinda pointless to store these in DB, hence functions
    # mainly for ease of use after get_user() is used.
    @staticmethod
    def is_provost():
        return False

    @staticmethod
    def is_student():
        return True


class RoomAllotmentRequest(models.Model):
    RequestID = models.AutoField(primary_key=True)
    stdID = models.ForeignKey(Student, on_delete=models.CASCADE)
    requestedRoomNo = models.ForeignKey(Room, on_delete=models.CASCADE,null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)
    message = models.CharField(max_length=200, null=True, blank=True)
    sports = models.BooleanField(default=False)
    debate = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    other_skill = models.CharField(max_length=200, null=True, blank=True)

    PENDING = 1
    ACCEPTED = 2
    DECLINED = 3
    APPROVAL_STATUS = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    )
    approvalStatus = models.IntegerField(choices=APPROVAL_STATUS, default=PENDING)


    def __str__(self):
        return f'ID: {self.stdID}, RequestedRoomNo: {self.requestedRoomNo}'


class Provost(models.Model):
    provostID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100,default=123456)
    mobile_no = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100,null=True, blank=True)
    department = models.CharField(max_length=100,default="CSE")
    post = models.CharField(max_length=100,default="Professor") 
    start_timestamp = models.DateTimeField(default=timezone.now)
    end_timestamp = models.DateTimeField(null=True)

    # not sure if normal fields are okay in models
    # seems kinda pointless to store these in DB, hence functions
    # mainly for ease of use after get_user() is used.
    @staticmethod
    def is_provost():
        return True

    @staticmethod
    def is_student():
        return False


class Notification(models.Model):
    notifID = models.IntegerField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    details = models.CharField(max_length=200, null=True, blank=True)
    seen = models.BooleanField(default=False)
    notifURL = models.CharField(max_length=200, null=True, blank=True)

    def isSeen(self):
        self.seen=True
        self.save()

    def getURL(self):
        return self.notifURL
