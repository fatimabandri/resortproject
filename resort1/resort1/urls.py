from django.contrib import admin
from django.urls import path
from resortapp import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resortapp.urls')),
    

    # Main Pages
    path('', views.home, name='home'),
    path('rooms/', views.rooms, name='rooms'),
    path('room/<int:id>/', views.room, name='room'),   # Better single room URL

    # Booking & Reports
    path('booking/', views.booking, name='booking'),
    path('report/', views.report, name='report'),

    # Restaurant Section
    path('restaurant/', views.restaurant, name='restaurant'),
    path('kitchen/', views.kitchen, name='kitchen'),

    path('kitchen-dashboard/', views.kitchen_dashboard, name='kitchen_dashboard'),
    path('update-kitchen-status/<int:id>/<str:status>/', views.update_kitchen_status, name='update_kitchen_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    
]