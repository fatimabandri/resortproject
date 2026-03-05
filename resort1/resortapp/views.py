from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.db.models import Sum
from .models import Room, Booking, RestaurantOrder
from .models import KitchenOrder
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "admin_login.html")


def admin_logout(request):
    logout(request)
    return redirect('admin_login')
    
# ---------------- HOME PAGE ----------------
def home(request):
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status="Available").count()
    booked_rooms = Room.objects.filter(status="Booked").count()
    total_bookings = Booking.objects.count()

    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'booked_rooms': booked_rooms,
        'total_bookings': total_bookings,
    }

    return render(request, 'home.html', context)

# ---------------- ROOM LIST PAGE ----------------
def rooms(request):
    all_rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': all_rooms})


# ---------------- SINGLE ROOM PAGE ----------------
def room(request, id):
    single_room = get_object_or_404(Room, id=id)
    return render(request, 'room.html', {'room': single_room})


# ---------------- BOOKING PAGE ----------------
def booking(request):

    rooms = Room.objects.filter(status="Available")

    if request.method == "POST":

        room_id = request.POST.get('room')
        check_in = datetime.strptime(request.POST.get('check_in'), "%Y-%m-%d").date()
        check_out = datetime.strptime(request.POST.get('check_out'), "%Y-%m-%d").date()

        room = Room.objects.get(id=room_id)

        Booking.objects.create(
            room=room,
            guest_name=request.POST.get('guest_name'),
            check_in=check_in,
            check_out=check_out,
        )

        messages.success(request, "Room Booked Successfully!")
        return redirect('booking')

    return render(request, 'booking.html', {'rooms': rooms})

# ---------------- REPORT PAGE ----------------
@login_required
def report(request):
    total_rooms = Room.objects.count()
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = RestaurantOrder.objects.count()

    today = now().date()
    today_bookings = Booking.objects.filter(check_in=today).count()
    today_revenue = Booking.objects.filter(check_in=today).aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0

    context = {
        'total_rooms': total_rooms,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'today_bookings': today_bookings,
        'today_revenue': today_revenue,
    }

    return render(request, 'report.html', context)

# ---------------- RESTAURANT PAGE ----------------
def restaurant(request):
    return render(request, 'restaurant.html')

def dashboard(request):
    return render(request, 'dashboard.html')


# ---------------- KITCHEN PAGE ----------------
def kitchen(request):
    return render(request, 'kitchen.html')


@login_required
def kitchen_dashboard(request):
    pending_orders = KitchenOrder.objects.filter(status='Pending')
    preparing_orders = KitchenOrder.objects.filter(status='Preparing')
    completed_orders = KitchenOrder.objects.filter(status='Completed')

    context = {
        'pending_orders': pending_orders,
        'preparing_orders': preparing_orders,
        'completed_orders': completed_orders,
        'pending_count': pending_orders.count(),
        'preparing_count': preparing_orders.count(),
        'completed_count': completed_orders.count(),
    }

    return render(request, 'kitchen_dashboard.html', context)


@login_required
def update_kitchen_status(request, id, status):
    order = get_object_or_404(KitchenOrder, id=id)

    if status in ['Pending', 'Preparing', 'Completed']:
        order.status = status
        order.save()

    return redirect('kitchen_dashboard')
def contact(request):
    return render(request, 'contact.html')

def booking_history(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking_history.html', {'bookings': bookings})


def cancel_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    
    # Room ko wapas Available karo
    room = booking.room
    room.status = "Available"
    room.save()

    booking.delete()
    return redirect('booking_history')


def dashboard(request):

    total_rooms = Room.objects.count()

    available_rooms = Room.objects.filter(status="Available").count()

    booked_rooms = Room.objects.filter(status="Booked").count()

    total_bookings = Booking.objects.count()

    total_revenue = Booking.objects.aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0

    restaurant_orders = RestaurantOrder.objects.count()

    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'booked_rooms': booked_rooms,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'restaurant_orders': restaurant_orders,
    }

    return render(request, "dashboard.html", context)