from django import forms
from .models import Doctor, TimeSlot, Appointment

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name']
        # any other fields you want to include in the form

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['doctor', 'weekday', 'start_time', 'end_time']
        # any other fields you want to include in the form

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'doctor', 'time_slot']
        # any other fields you want to include in the form
