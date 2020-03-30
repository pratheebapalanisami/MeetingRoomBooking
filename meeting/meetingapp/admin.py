from django.contrib import admin

# Register your models here.
from .models import Room, BookingDetail


class RoomList(admin.ModelAdmin):
    list_display = ( 'room_number',)
    search_fields = ( 'name',)
    ordering = ['room_number']

class BookingDetailList(admin.ModelAdmin):
    list_display = (  'start_time',)
    search_fields = ( 'start_time',)
    ordering = ['attendees']

admin.site.register(Room, RoomList)
admin.site.register(BookingDetail, BookingDetailList)