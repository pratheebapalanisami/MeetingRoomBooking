from rest_framework import serializers
from .models import Room, BookingDetail


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'room_number', 'capacity', 'av', 'projector', 'phone')

class MeetingRoomSerializer(serializers.ModelSerializer):
   class Meta:
       model = BookingDetail
       fields = ('user', 'room', 'start_time', 'end_time', 'attendees')