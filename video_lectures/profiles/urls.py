from .views import ProfileView, UpdateProfile, ProfileListView, GroupView, GroupListView, UpdateGroup, SubjectView, SubjectListView
from django.urls import path

urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/update', UpdateProfile.as_view(), name='update-profile'),
    path('', ProfileListView.as_view(), name='profile-list'),
    path('groups/<int:pk>/', GroupView.as_view(), name='group'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/<int:pk>/update', UpdateGroup.as_view(), name='update-group'),
    path('subjects/<int:pk>', SubjectView.as_view(), name='subject'),
    path('subjects/', SubjectListView.as_view(), name='subject-list'),


]