from django.contrib import admin
from django.urls import path
from .views import CreateVideo, DetailVideo, UpdateVideo, DeleteVideo, VideoCategoryList, SearchVideo, RegistrationChoiceView, NotLectorView, CourseView, CourseListView, UpdateCourse, CreateCourse
from profiles.views import ProfileListView, GroupListView, SubjectListView
from django.conf import settings
from django.conf.urls.static import static

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
    path('profiles/groups', GroupListView.as_view(), name='group-list'),
    path('profiles/subjects', SubjectListView.as_view(), name='subject-list'),
    path('courses/<int:pk>', CourseView.as_view(), name='course'),
    path('courses', CourseListView.as_view(), name='course-list'),
    path('courses/create', CreateCourse.as_view(), name='course-create'),
    path('courses/<int:pk>/update', UpdateCourse.as_view(), name='update-course'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)