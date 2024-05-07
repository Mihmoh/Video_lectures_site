from .views import ProfileView, UpdateProfile, ProfileListView, GroupView, GroupListView
from django.urls import path

urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/update', UpdateProfile.as_view(), name='update-profile'),
    path('', ProfileListView.as_view(), name='profile-list'),
    path('groups/<int:pk>/', GroupView.as_view(), name='group'),
    path('groups/', GroupListView.as_view(), name='group-list'),

]