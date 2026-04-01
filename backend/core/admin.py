from django.contrib import admin
from .models import Room, Reservation, Guest

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["room_number", "room_type", "floor", "rate_per_night", "status", "created_at"]
    list_filter = ["room_type", "status"]
    search_fields = ["room_number"]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["guest_name", "guest_email", "room_number", "check_in", "check_out", "created_at"]
    list_filter = ["status", "payment"]
    search_fields = ["guest_name", "guest_email", "room_number"]

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "id_type", "id_number", "created_at"]
    list_filter = ["id_type"]
    search_fields = ["name", "email", "phone"]
