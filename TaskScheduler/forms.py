from django import forms

class TaskForm(forms.Form):
	name = forms.CharField(label='Task Name', max_length=100)
	priority = forms.IntegerField(label="Priority")
	span = forms.IntegerField(label="Span")
	deadline = forms.DateTimeField(label="Deadline")
	at_a_stretch = forms.IntegerField(label="At a Stretch(min)")
	done = forms.BooleanField(label="Done Status")

class BlockedForm(forms.Form):
	name = forms.CharField(label='Blocked Name', max_length=100)
	# start_time = forms.DateTimeField(label="Start Time")
	# end_time = forms.DateTimeField(label="End Time")
	