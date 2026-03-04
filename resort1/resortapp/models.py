from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Room(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Booked', 'Booked'),
    )

    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")

    def __str__(self):
        return f"Room {self.room_number}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    total_days = models.IntegerField(blank=True, null=True)
    total_amount = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date")

    def save(self, *args, **kwargs):
        self.clean()

        self.total_days = (self.check_out - self.check_in).days
        self.total_amount = self.total_days * self.room.price

        # Update room status
        self.room.status = "Booked"
        self.room.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest_name} - Room {self.room.room_number}"


class RestaurantOrder(models.Model):
    table_number = models.IntegerField()
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Table {self.table_number} - {self.item_name}"


class KitchenOrder(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Completed', 'Completed'),
    )

    order = models.ForeignKey(RestaurantOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.order} - {self.status}"