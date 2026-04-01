from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=255)
    room_type = models.CharField(max_length=50, choices=[("single", "Single"), ("double", "Double"), ("suite", "Suite"), ("deluxe", "Deluxe"), ("presidential", "Presidential")], default="single")
    floor = models.IntegerField(default=0)
    rate_per_night = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("available", "Available"), ("occupied", "Occupied"), ("maintenance", "Maintenance"), ("reserved", "Reserved")], default="available")
    amenities = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.room_number

class Reservation(models.Model):
    guest_name = models.CharField(max_length=255)
    guest_email = models.EmailField(blank=True, default="")
    room_number = models.CharField(max_length=255, blank=True, default="")
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    nights = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("confirmed", "Confirmed"), ("checked_in", "Checked In"), ("checked_out", "Checked Out"), ("cancelled", "Cancelled")], default="confirmed")
    payment = models.CharField(max_length=50, choices=[("paid", "Paid"), ("pending", "Pending")], default="paid")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.guest_name

class Guest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    id_type = models.CharField(max_length=50, choices=[("passport", "Passport"), ("aadhar", "Aadhar"), ("drivinglicense", "DrivingLicense")], default="passport")
    id_number = models.CharField(max_length=255, blank=True, default="")
    visits = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vip = models.BooleanField(default=False)
    nationality = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
