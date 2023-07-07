from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue, ApplyEvent
# Import User Model From Django
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin, ApplicationForm
from django.http import HttpResponse
import csv
from django.contrib import messages

# Import PDF Stuff
from django.http import FileResponse
import io

def show_attendees(request,event_id):
	attendees=ApplyEvent.objects.filter(event=event_id)
	return render(request,'events/show_attendees.html', {'attendees': attendees})


def my_events(request):
	events=Event.objects.filter(manager=request.user.id)
	return render(request,'events/my_events.html',{ 'events' : events})

# Show Event
def show_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	return render(request, 'events/show_event.html', {
			"event":event
			})

# Show Events In A Venue
def venue_events(request, venue_id):
	# Grab the venue
	venue = Venue.objects.get(id=venue_id)	
	# Grab the events from that venue
	events = venue.event_set.all()
	if events:
		return render(request, 'events/venue_events.html', {
			"events":events
			})
	else:
		messages.success(request, ("That Department Has No Events At This Time..."))
		return redirect('admin_approval')


# Create Admin Event Approval Page
def admin_approval(request):
	# Get The Venues
	venue_list = Venue.objects.all()
	# Get Counts
	event_count = Event.objects.all().count()
	venue_count = Venue.objects.all().count()
	user_count = User.objects.all().count()
	current=request.user.id
	venuelist=Venue.objects.filter(owner=current).values_list('id')
	event_list = Event.objects.filter(venue__in=venuelist).order_by('-event_date')
	if request.method == "POST":
		# Get list of checked box id's
		id_list = request.POST.getlist('boxes')

		# Uncheck all events
		event_list.update(approved=False)

		# Update the database
		for x in id_list:
			Event.objects.filter(pk=int(x)).update(approved=True)
			
		# Show Success Message and Redirect
		messages.success(request, ("Event List Approval Has Been Updated!"))
		return redirect('list-events')



	else:
		return render(request, 'events/admin_approval.html',
				{"event_list": event_list,
				"event_count":event_count,
				"venue_count":venue_count,
				"user_count":user_count,
				"venue_list":venue_list})

	return render(request, 'events/admin_approval.html')

def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venues')		


# Delete an Event
def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user == event.manager:
		event.delete()
		messages.success(request, ("Event Deleted!!"))
		return redirect('list-events')		
	else:
		messages.success(request, ("You Aren't Authorized To Delete This Event!"))
		return redirect('list-events')		

def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST, request.FILES)
			if form.is_valid():
					form.save()
					return 	HttpResponseRedirect('/add_event?submitted=True')	
		else:
			form = EventForm(request.POST, request.FILES)
			if form.is_valid():
				#form.save()
				event = form.save(commit=False)
				event.manager = request.user # logged in user
				event.save()
				return 	HttpResponseRedirect('/add_event?submitted=True')	
	else:
		# Just Going To The Page, Not Submitting 
		if request.user.is_superuser:
			form = EventFormAdmin
		else:
			form = EventForm

		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})


def apply_event(request):
	form=ApplicationForm
	submitted = False
	if request.method == "POST":
		form = ApplicationForm(request.POST, request.FILES)
		if form.is_valid():
			#form.save()
			event = form.save(commit=False)
			event.manager = request.user # logged in user
			event.save()
			return 	HttpResponseRedirect('/apply_event?submitted=True')	
	else:
		form = ApplicationForm
	if 'submitted' in request.GET:
		submitted = True

	return render(request, 'events/apply_event.html', {'form':form, 'submitted':submitted})


def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance=event)	
	else:
		form = EventForm(request.POST or None, instance=event)
	
	if form.is_valid():
		form.save()
		return redirect('list-events')

	return render(request, 'events/update_event.html', 
		{'event': event,
		'form':form})


def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
	if form.is_valid():
		form.save()
		return redirect('list-venues')

	return render(request, 'events/update_venue.html', 
		{'venue': venue,
		'form':form})

def search_venues(request):
	if request.method == "POST":
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)
	
		return render(request, 
		'events/search_venues.html', 
		{'searched':searched,
		'venues':venues})
	else:
		return render(request, 
		'events/search_venues.html', 
		{})


def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue_owner = User.objects.get(pk=venue.owner)

	# Grab the events from that venue
	events = venue.event_set.all()

	return render(request, 'events/show_venue.html', 
		{'venue': venue,
		'venue_owner':venue_owner,
		'events':events})

def list_venues(request):
	#venue_list = Venue.objects.all().order_by('?')
	venue_list = Venue.objects.all()
	return render(request, 'events/venue.html', 
		{'venue_list': venue_list,}
		)

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			venue = form.save(commit=False)
			venue.owner = request.user.id # logged in user
			venue.save()
			#form.save()
			return 	HttpResponseRedirect('/add_venue?submitted=True')	
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})

def all_events(request):
	event_list = Event.objects.all().order_by('-event_date')
	return render(request, 'events/event_list.html', 
		{'event_list': event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = request.user
	month = month.capitalize()
	# Convert month from name to number
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	# create a calendar
	cal = HTMLCalendar().formatmonth(
		year, 
		month_number)
	# Get current year
	now = datetime.now()
	current_year = now.year
	
	# Query the Events Model For Dates
	event_list = Event.objects.filter(
		event_date__year = year,
		event_date__month = month_number
		)

	# Get current time
	time = now.strftime('%I:%M %p')
	return render(request, 
		'events/home.html', {
		"name": name,
		"year": year,
		"month": month,
		"month_number": month_number,
		"cal": cal,
		"current_year": current_year,
		"time":time,
		"event_list": event_list,
		})

