from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=50,blank=False, null=False, default=' ')
    room_number = models.IntegerField(blank=False, primary_key=True)
    capacity = models.CharField(max_length=50, default=' ')
    av = models.BooleanField()
    projector = models.BooleanField()
    phone = models.BooleanField()

    def __str__(self):
        return str(self.room_number)

class BookingDetail(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    attendees = models.CharField(max_length=1000, default=' ')

    def __str__(self):
        return str(self.room)

