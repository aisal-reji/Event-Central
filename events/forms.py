from django import forms
from django.forms import ModelForm
from .models import Venue, Event ,ApplyEvent

# Admin SuperUser Event Form
class EventFormAdmin(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'event_date', 'venue', 'manager', 'description','event_image')
		labels = {
			'name': '',
			'event_date': 'YYYY-MM-DD HH:MM:SS',
			'venue': 'Department',
			'manager': 'Manager',
			'description': '',	
			'event_image': 'Add Display Image (Not Required)',		
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
			'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Department'}),
			'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
		}

# User Event Form
class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'event_date', 'venue', 'description','event_image',)
		labels = {
			'name': '',
			'event_date': 'YYYY-MM-DD HH:MM:SS',
			'venue': 'Club/Department',
			'description': '',	
			'event_image': 'Add Display Image (Not Required)',		
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
			'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Department'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
		}


# Create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('name', )
		labels = {
			'name': '',		
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dept Name'}),
		}


class ApplicationForm(ModelForm):
	mgitsid=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	class Meta:
		model=ApplyEvent
		fields =('name','mgitsid','event',)
		labels = {
			'name' : '',
			'mgitsid' : 'Mgits ID',
			'event': 'Event'
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
			'event' : forms.Select(attrs={'class':'form-select', 'placeholder':'Events'}),
		}