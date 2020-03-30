from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from meeting import settings
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from meeting.settings import TIME_ZONE
from rest_framework.views import APIView
from rest_framework.response import Response
import pytz

from xhtml2pdf import pisa

# Create your views here.
from meetingapp.forms import MeetingRoomEditForm, MeetingRoomForm
from meetingapp.models import Room, BookingDetail
from meetingapp.decorators import employee_required, manager_required
from .serializers import MeetingRoomSerializer, RoomSerializer

@login_required
def home(request):
    current_user = request.user
    if(current_user.is_superuser):
        return render(request, 'meetingapp/home.html')
    elif(current_user.profile.is_manager):
        room = Room.objects.filter()
        return render(request, 'meetingapp/room_list.html',{'room': room})
    elif(current_user.profile.is_employee):
        bookingdetail = BookingDetail.objects.filter(user=request.user)
        return render(request, 'meetingapp/meeting_list.html',
                      {'bookingdetail': bookingdetail})

@login_required
@manager_required
def room_list(request):
    room = Room.objects.filter()
    return render(request, 'meetingapp/room_list.html',
                  {'room': room})

@login_required
@manager_required
def add_room(request):
    if request.method == "POST":
        form = MeetingRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_date = timezone.now()
            room.save()
            room = Room.objects.filter()
            return render(request, 'meetingapp/room_list.html',
                          {'room': room})
    else:
        form = MeetingRoomForm()
    return render(request, 'meetingapp/add_room.html', {'form': form})

@login_required
@manager_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        # update
        form = MeetingRoomEditForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.updated_date = timezone.now()
            room.save()
            room = Room.objects.filter()
            return render(request, 'meetingapp/room_list.html',
                          {'room': room})
    else:
        # edit
        form = MeetingRoomEditForm(instance=room)
    return render(request, 'meetingapp/room_edit.html', {'form': form})

@login_required
@employee_required
def meeting_cancel(request, pk):
    print(pk)
    bookingdetail = get_object_or_404(BookingDetail, pk=pk)
    bookingdetail.delete()
    emailbody = "Meeting has been cancelled by " + str(request.user) + " from " + str(bookingdetail.start_time) + " to " + str(
        bookingdetail.end_time) + " at meeting room " + str(bookingdetail.room.name) + " " + str(bookingdetail.room.room_number)
    mail = EmailMessage("Meeting Details", emailbody, settings.EMAIL_HOST_USER, [bookingdetail.attendees])
    mail.send()
    bookingdetail = BookingDetail.objects.filter()
    return render(request, 'meetingapp/meeting_list.html', {'bookingdetail': bookingdetail})

@login_required
@employee_required
def search(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        startTime= request.GET.get('startTime')
        endTime= request.GET.get('endTime')
        submitbutton= request.GET.get('submit')
        sttime = datetime.strptime(date+ " " + startTime, '%Y-%m-%d %H:%M')
        ettime = datetime.strptime(date+ " " + endTime, '%Y-%m-%d %H:%M')
        booking = BookingDetail.objects.filter(Q(start_time__gte = sttime) & Q(start_time__lte = ettime) | Q(end_time__gte = sttime)  & Q(end_time__lte = ettime)).distinct().values_list('room__room_number',flat=True)
        room = Room.objects.exclude(room_number__in=booking)
        return render(request, 'meetingapp/search.html',{'room': room, 'date': date, 'startTime': startTime, 'endTime': endTime, 'attendees': request.GET.get('attendees') })
    else:
        return render(request, 'meetingapp/search.html')

@login_required
@employee_required
def book(request):
    if request.method == "GET":
        date = request.GET.get('date')
        startTime = request.GET.get('startTime')
        endTime = request.GET.get('endTime')
        room_no = request.GET.get('room_no')
        submitbutton = request.GET.get('submit')
        sttime = datetime.strptime(date + " " + startTime, '%Y-%m-%d %H:%M')
        ettime = datetime.strptime(date + " " + endTime, '%Y-%m-%d %H:%M')
        room = Room.objects.get(pk=room_no)
        bookingdetail = BookingDetail(user=request.user,start_time=sttime, end_time=ettime, room=room, attendees= request.GET.get('attendees'))
        bookingdetail.save()
        bookingdetail = BookingDetail.objects.filter(user=request.user)
        emailbody = "Meeting has been scheduled by " + str(request.user) + " from " + str(sttime) + " to " + str(ettime) + " at meeting room " + str(
            room.name) + " " + str(room.room_number)
        mail = EmailMessage("Meeting Details", emailbody, settings.EMAIL_HOST_USER, [request.GET.get('attendees'),request.user.email])
        mail.send()
        return render(request, 'meetingapp/meeting_list.html',
                          {'bookingdetail': bookingdetail})
    return render(request, 'meetingapp/search.html')

@login_required
@employee_required
def meeting_list(request):
    bookingdetail = BookingDetail.objects.filter(user=request.user)
    return render(request, 'meetingapp/meeting_list.html',
                  {'bookingdetail': bookingdetail})
@login_required
@employee_required
def book_meeting(request):
    date = datetime.now().isoformat().split('T')[0]
    return render(request,'meetingapp/search.html', {'curdate':date})

@login_required
@manager_required
def all_meeting(request):
    bookingdetail = BookingDetail.objects.filter()
    return render(request, 'meetingapp/all_meeting.html',
                  {'bookingdetail': bookingdetail})

@login_required
@manager_required
def render_to_pdf(request):
    bookingdetail = BookingDetail.objects.filter()
    template = get_template('meetingapp/download.html')
    html  = template.render({'bookingdetail': bookingdetail})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    mail = EmailMessage("Meeting List", "", settings.EMAIL_HOST_USER, [request.user.email])
    mail.attach("Report", result.getvalue(), 'application/pdf')
    mail.send()
    return render(request, 'meetingapp/report_success.html')

# Lists all rooms
class RoomList(APIView):
    def get(self,request):
        rooms_json = Room.objects.all()
        serializer = RoomSerializer(rooms_json, many=True)
        return Response(serializer.data)

# Lists all meetings
class MeetingList(APIView):
    def get(self,request):
        meetings_json = BookingDetail.objects.all()
        serializer = MeetingRoomSerializer(meetings_json, many=True)
        return Response(serializer.data)