import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Room, Reservation, Guest


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['room_count'] = Room.objects.count()
    ctx['room_single'] = Room.objects.filter(room_type='single').count()
    ctx['room_double'] = Room.objects.filter(room_type='double').count()
    ctx['room_suite'] = Room.objects.filter(room_type='suite').count()
    ctx['room_total_rate_per_night'] = Room.objects.aggregate(t=Sum('rate_per_night'))['t'] or 0
    ctx['reservation_count'] = Reservation.objects.count()
    ctx['reservation_confirmed'] = Reservation.objects.filter(status='confirmed').count()
    ctx['reservation_checked_in'] = Reservation.objects.filter(status='checked_in').count()
    ctx['reservation_checked_out'] = Reservation.objects.filter(status='checked_out').count()
    ctx['reservation_total_total'] = Reservation.objects.aggregate(t=Sum('total'))['t'] or 0
    ctx['guest_count'] = Guest.objects.count()
    ctx['guest_passport'] = Guest.objects.filter(id_type='passport').count()
    ctx['guest_aadhar'] = Guest.objects.filter(id_type='aadhar').count()
    ctx['guest_drivinglicense'] = Guest.objects.filter(id_type='drivinglicense').count()
    ctx['guest_total_total_spent'] = Guest.objects.aggregate(t=Sum('total_spent'))['t'] or 0
    ctx['recent'] = Room.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def room_list(request):
    qs = Room.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(room_number__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(room_type=status_filter)
    return render(request, 'room_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def room_create(request):
    if request.method == 'POST':
        obj = Room()
        obj.room_number = request.POST.get('room_number', '')
        obj.room_type = request.POST.get('room_type', '')
        obj.floor = request.POST.get('floor') or 0
        obj.rate_per_night = request.POST.get('rate_per_night') or 0
        obj.status = request.POST.get('status', '')
        obj.amenities = request.POST.get('amenities', '')
        obj.save()
        return redirect('/rooms/')
    return render(request, 'room_form.html', {'editing': False})


@login_required
def room_edit(request, pk):
    obj = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        obj.room_number = request.POST.get('room_number', '')
        obj.room_type = request.POST.get('room_type', '')
        obj.floor = request.POST.get('floor') or 0
        obj.rate_per_night = request.POST.get('rate_per_night') or 0
        obj.status = request.POST.get('status', '')
        obj.amenities = request.POST.get('amenities', '')
        obj.save()
        return redirect('/rooms/')
    return render(request, 'room_form.html', {'record': obj, 'editing': True})


@login_required
def room_delete(request, pk):
    obj = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/rooms/')


@login_required
def reservation_list(request):
    qs = Reservation.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(guest_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'reservation_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def reservation_create(request):
    if request.method == 'POST':
        obj = Reservation()
        obj.guest_name = request.POST.get('guest_name', '')
        obj.guest_email = request.POST.get('guest_email', '')
        obj.room_number = request.POST.get('room_number', '')
        obj.check_in = request.POST.get('check_in') or None
        obj.check_out = request.POST.get('check_out') or None
        obj.nights = request.POST.get('nights') or 0
        obj.total = request.POST.get('total') or 0
        obj.status = request.POST.get('status', '')
        obj.payment = request.POST.get('payment', '')
        obj.save()
        return redirect('/reservations/')
    return render(request, 'reservation_form.html', {'editing': False})


@login_required
def reservation_edit(request, pk):
    obj = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        obj.guest_name = request.POST.get('guest_name', '')
        obj.guest_email = request.POST.get('guest_email', '')
        obj.room_number = request.POST.get('room_number', '')
        obj.check_in = request.POST.get('check_in') or None
        obj.check_out = request.POST.get('check_out') or None
        obj.nights = request.POST.get('nights') or 0
        obj.total = request.POST.get('total') or 0
        obj.status = request.POST.get('status', '')
        obj.payment = request.POST.get('payment', '')
        obj.save()
        return redirect('/reservations/')
    return render(request, 'reservation_form.html', {'record': obj, 'editing': True})


@login_required
def reservation_delete(request, pk):
    obj = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/reservations/')


@login_required
def guest_list(request):
    qs = Guest.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(id_type=status_filter)
    return render(request, 'guest_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def guest_create(request):
    if request.method == 'POST':
        obj = Guest()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.id_type = request.POST.get('id_type', '')
        obj.id_number = request.POST.get('id_number', '')
        obj.visits = request.POST.get('visits') or 0
        obj.total_spent = request.POST.get('total_spent') or 0
        obj.vip = request.POST.get('vip') == 'on'
        obj.nationality = request.POST.get('nationality', '')
        obj.save()
        return redirect('/guests/')
    return render(request, 'guest_form.html', {'editing': False})


@login_required
def guest_edit(request, pk):
    obj = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.id_type = request.POST.get('id_type', '')
        obj.id_number = request.POST.get('id_number', '')
        obj.visits = request.POST.get('visits') or 0
        obj.total_spent = request.POST.get('total_spent') or 0
        obj.vip = request.POST.get('vip') == 'on'
        obj.nationality = request.POST.get('nationality', '')
        obj.save()
        return redirect('/guests/')
    return render(request, 'guest_form.html', {'record': obj, 'editing': True})


@login_required
def guest_delete(request, pk):
    obj = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/guests/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['room_count'] = Room.objects.count()
    data['reservation_count'] = Reservation.objects.count()
    data['guest_count'] = Guest.objects.count()
    return JsonResponse(data)
