from django.db import models
from django.utils import timezone


class Room(models.Model):
    RoomNo = models.IntegerField(primary_key=True)
    totalSeats = models.IntegerField(default=4)
    vacantSeats = models.IntegerField(default=4)


class Student(models.Model):
    stdID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    password = models.IntegerField(default=123456)
    roomNo = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)


class RoomAllotmentRequest(models.Model):
    RequestID = models.AutoField(primary_key=True)
    stdID = models.ForeignKey(Student, on_delete=models.CASCADE)
    requestedRoomNo = models.ForeignKey(Room, on_delete=models.CASCADE)
    attachment = models.FileField(null=True, blank=True)
    message = models.CharField(max_length=200, null=True, blank=True)
    skill = models.CharField(max_length=200, null=True, blank=True)
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
    password = models.IntegerField(default=123456)


class Notification(models.Model):
    notifID = models.IntegerField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    details = models.CharField(max_length=200, null=True, blank=True)
    seen = models.BooleanField(default=False)
