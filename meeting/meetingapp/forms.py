
from django import forms
from .models import Room


class MeetingRoomForm(forms.ModelForm):
   class Meta:
       model = Room
       fields = ('name', 'room_number', 'capacity', 'av', 'projector', 'phone')

class MeetingRoomEditForm(forms.ModelForm):
   room_number = forms.IntegerField(disabled=True)
   class Meta:
       model = Room
       fields = ('name', 'room_number', 'capacity', 'av', 'projector', 'phone')
       widgets = {'room_number': forms.TextInput(attrs={'readonly':'readonly'})}