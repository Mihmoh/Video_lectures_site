from django.contrib import admin
from django.urls import path
from .views import CreateVideo, DetailVideo, UpdateVideo, DeleteVideo, VideoCategoryList, SearchVideo, RegistrationChoiceView, NotLectorView
from profiles.views import ProfileListView

urlpatterns = [
    path('create/', CreateVideo.as_view(), name='video-create'),
    path('<int:pk>/', DetailVideo.as_view(), name='video-detail'),
    path('<int:pk>/update', UpdateVideo.as_view(), name='video-update'),
    path('<int:pk>/delete', DeleteVideo.as_view(), name='video-delete'),
    path('category/<int:pk>', VideoCategoryList.as_view(), name='category-list'),
    path('search/', SearchVideo.as_view(), name='video-search'),
    path('registration-choice/', RegistrationChoiceView.as_view(), name='registration-choice'),
    path('not_lector/', NotLectorView.as_view(), name='not-lector'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),

]