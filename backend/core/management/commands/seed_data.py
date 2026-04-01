from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Room, Reservation, Guest
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusHotelPMS with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexushotelpms.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Room.objects.count() == 0:
            for i in range(10):
                Room.objects.create(
                    room_number=f"Sample {i+1}",
                    room_type=random.choice(["single", "double", "suite", "deluxe", "presidential"]),
                    floor=random.randint(1, 100),
                    rate_per_night=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["available", "occupied", "maintenance", "reserved"]),
                    amenities=f"Sample amenities for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Room records created'))

        if Reservation.objects.count() == 0:
            for i in range(10):
                Reservation.objects.create(
                    guest_name=f"Sample Reservation {i+1}",
                    guest_email=f"demo{i+1}@example.com",
                    room_number=f"Sample {i+1}",
                    check_in=date.today() - timedelta(days=random.randint(0, 90)),
                    check_out=date.today() - timedelta(days=random.randint(0, 90)),
                    nights=random.randint(1, 100),
                    total=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["confirmed", "checked_in", "checked_out", "cancelled"]),
                    payment=random.choice(["paid", "pending"]),
                )
            self.stdout.write(self.style.SUCCESS('10 Reservation records created'))

        if Guest.objects.count() == 0:
            for i in range(10):
                Guest.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    id_type=random.choice(["passport", "aadhar", "drivinglicense"]),
                    id_number=f"Sample {i+1}",
                    visits=random.randint(1, 100),
                    total_spent=round(random.uniform(1000, 50000), 2),
                    vip=random.choice([True, False]),
                    nationality=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Guest records created'))
