from django.urls import path, re_path
from accounts.views import user_login
from meetingapp.views import home, search, add_room, book, room_list, meeting_list, book_meeting, render_to_pdf, all_meeting, room_edit, RoomList, MeetingList
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

from . import views

app_name = 'meetingapp'

urlpatterns = [
    path('', user_login, name='login'),
    re_path(r'^home/$', home, name='home'),
    path('room_list', room_list, name='room_list'),
    path('add_room', add_room, name='add_room'),
    path('<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('<int:pk>/cancel/', views.meeting_cancel, name='meeting_cancel'),
    path('search', search, name='search'),
    path('book', book, name='book'),
    path('meeting_list', meeting_list, name='meeting_list'),
    path('all_meeting', all_meeting, name='all_meeting'),
    path('book_meeting', book_meeting, name='book_meeting'),
    path('render_to_pdf', render_to_pdf, name='render_to_pdf'),
    url(r'^rooms_json/', views.RoomList.as_view()),
    url(r'^meetings_json/', views.MeetingList.as_view()),
    ]
urlpatterns = format_suffix_patterns(urlpatterns)