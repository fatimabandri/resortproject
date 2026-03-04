from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('cancel-booking/<int:id>/', views.cancel_booking, name='cancel_booking'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('booking/', views.booking, name='booking'),
    path('kitchen-dashboard/', views.kitchen_dashboard, name='kitchen_dashboard'),
    path('update-kitchen-status/<int:id>/<str:status>/', views.update_kitchen_status, name='update_kitchen_status'),
]