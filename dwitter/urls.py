from django.urls import path
from .views import home, profile_list, profile

urlpatterns =[
    path('', home, name='home'),
    path('profile_list', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile, name='profile')
]

