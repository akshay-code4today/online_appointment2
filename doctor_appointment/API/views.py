from django.shortcuts import render, get_object_or_404
from datetime import datetime, time, timedelta
from .models import Doctor, TimeSlot, Appointment
from .serializers import DoctorSerializer, TimeSlotSerializer, AppointmentSerializer


def index(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'index.html', context)


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    date_str = request.GET.get('date')
    if not date_str:
        date = datetime.now().date()
    else:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'error.html', {'message': 'Invalid date format'})
    time_slots = TimeSlot.objects.filter(doctor=doctor, weekday=date.strftime('%a').lower(), start_time__date=date)
    appointments = Appointment.objects.filter(time_slot__in=time_slots)
    slots_data = TimeSlotSerializer(time_slots, many=True).data
    appointments_data = AppointmentSerializer(appointments, many=True).data
    context = {'doctor': doctor, 'date': date, 'slots': slots_data, 'appointments': appointments_data}
    return render(request, 'doctor_detail.html', context)


def save_availability(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        serializer = TimeSlotSerializer(data=request.POST, many=True)
        if serializer.is_valid():
            time_slots = []
            for ts_data in serializer.validated_data:
                time_slots.append(TimeSlot(doctor=doctor, **ts_data))
            TimeSlot.objects.bulk_create(time_slots)
            return render(request, 'success.html', {'message': 'Availability saved successfully'})
        else:
            return render(request, 'error.html', {'message': 'Invalid data'})
    else:
        return render(request, 'error.html', {'message': 'Method not allowed'})


def update_availability(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if not start_date or not end_date:
            return render(request, 'error.html', {'message': 'Start date and end date are required'})
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'error.html', {'message': 'Invalid date format'})
        if start_date > end_date:
            return render(request, 'error.html', {'message': 'Start date must be before end date'})
        time_slots = TimeSlot.objects.filter(doctor=doctor, start_time__date__gte=start_date,
                                             end_time__date__lte=end_date)
        serializer = TimeSlotSerializer(time_slots, data=request.POST, many=True)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'success.html', {'message': 'Availability updated successfully'})
        else:
            return render(request, 'error.html', {'message': 'Invalid data'})
    else:
        return render(request, 'error.html', {'message': 'Method not allowed'})


def list_availability(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    date_str = request.GET.get('date')
    if not date_str:
        date = datetime.now().date()
    else:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'error.html', {'message': 'Invalid date format'})
    time_slots = TimeSlot.objects.filter(doctor=doctor, start_time__date=date).order_by('start_time')
    available_slots = []
    start_time = datetime.combine(date, time(hour=9))
    end_time = datetime.combine(date, time(hour=17))
    while start_time < end_time:
        if not TimeSlot.objects.filter(doctor=doctor, start_time=start_time).exists():
            available_slots.append(start_time)
        start_time += timedelta(minutes=30)
    context = {'doctor': doctor, 'date': date, 'time_slots': time_slots, 'available_slots': available_slots}
    return render(request, 'list_availability.html', context)

