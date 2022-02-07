from django.db import models


class Student(models.Model):
    stdID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    password = models.IntegerField(default=123456)# this should be hashed I guess


class Room(models.Model):
    RoomNo = models.IntegerField(primary_key=True)


class RoomAllotmentRequest(models.Model):
    RequestID = models.AutoField(primary_key=True)
    stdID = models.ForeignKey(Student, on_delete=models.CASCADE)
    requestedRoomNo = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'ID: {self.stdID}, RequestedRoomNo: {self.requestedRoomNo}'
