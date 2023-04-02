from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    # any other fields you may want to add, like phone number, address, etc.

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    weekdays = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    weekday = models.CharField(choices=weekdays, max_length=3)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.doctor.name} - {self.weekday} {self.start_time} to {self.end_time}'


class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.patient_name} - {self.doctor.name} ({self.time_slot.weekday} {self.time_slot.start_time} to {self.time_slot.end_time})'

