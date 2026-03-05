from django.contrib import admin
from .models import Room, Booking, RestaurantOrder, KitchenOrder


# Room Admin
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price', 'status')
    list_filter = ('status', 'room_type')
    search_fields = ('room_number',)


# Booking Admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'check_in', 'check_out', 'total_days', 'total_amount', 'created_at')
    list_filter = ('check_in', 'check_out')
    search_fields = ('guest_name',)
    ordering = ('-created_at',)


# Restaurant Order Admin
class RestaurantOrderAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'item_name', 'quantity', 'order_date')
    list_filter = ('order_date',)
    search_fields = ('item_name',)


# Kitchen Dashboard Admin
class KitchenOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'status')
    list_filter = ('status',)
    search_fields = ('order__item_name',)


# Register Models
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(RestaurantOrder, RestaurantOrderAdmin)
admin.site.register(KitchenOrder, KitchenOrderAdmin)