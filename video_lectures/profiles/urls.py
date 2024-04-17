from .views import ProfileView, UpdateProfile
from django.urls import path

urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/update', UpdateProfile.as_view(), name='update-profile'),

]