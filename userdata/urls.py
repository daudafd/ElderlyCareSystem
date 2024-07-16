# userdata/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),  # URL pattern for 'admin'
    path('home/', views.home, name='home'),  # URL pattern for 'user'

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('client/', views.client, name='client'),
    path('staff/', views.staff, name='staff'),
    path('user_client/', views.user_client, name='user_client'),
    # path('client-profile/', views.client_profile, name='client_profile'),
    path('client-profile/<int:client_id>/', views.client_profile, name='client_profile'),
    path('add-client/', views.add_client, name='add_client'),
    path('add_user/', views.add_user, name='add_user'),
    path('client/edit/<int:pk>/', views.edit_client, name='edit_client'),
    path('chart/', views.chart, name='chart'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]
