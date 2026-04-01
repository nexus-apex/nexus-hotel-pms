from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/create/', views.reservation_create, name='reservation_create'),
    path('reservations/<int:pk>/edit/', views.reservation_edit, name='reservation_edit'),
    path('reservations/<int:pk>/delete/', views.reservation_delete, name='reservation_delete'),
    path('guests/', views.guest_list, name='guest_list'),
    path('guests/create/', views.guest_create, name='guest_create'),
    path('guests/<int:pk>/edit/', views.guest_edit, name='guest_edit'),
    path('guests/<int:pk>/delete/', views.guest_delete, name='guest_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
