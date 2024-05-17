from django.test import TestCase, RequestFactory
from .models import Profile, User, UserType, Group, Subject
from .views import ProfileView
from videos.models import Video, Course
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.response import TemplateResponse
from django.urls import reverse


class ProfileModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):

        user_type = UserType.objects.create(name='Student')

        group = Group.objects.create(name='Group 1')

        subject = Subject.objects.create(name='Math')

        user = User.objects.create_user(username='testuser', password='testpassword')

        profile = Profile.objects.create(
            user=user,
            user_type=user_type,
            name='John',
            surname='Doe',
            patronymic='Smith',
            student_group=group,
        )
        profile.subjects.add(subject)

    def test_profile_str_representation(self):
        profile = Profile.objects.get(id=1)
        expected_str = ' Doe  John  Smith | Student | Group 1'
        self.assertEqual(str(profile), expected_str)

    def test_profile_fields(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.user_type.name, 'Student')
        self.assertEqual(profile.name, 'John')
        self.assertEqual(profile.surname, 'Doe')
        self.assertEqual(profile.patronymic, 'Smith')
        self.assertEqual(profile.student_group.name, 'Group 1')
        self.assertIsNotNone(profile.image)
        self.assertEqual(profile.subjects.count(), 1)
        self.assertEqual(profile.subjects.first().name, 'Math')


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user_type = UserType.objects.create(name='Student')

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.profile = Profile.objects.create(
            user=self.user,
            user_type=self.user_type,
            name='John',
            surname='Doe',
            patronymic='Smith',
            image=0
        )

        self.video1 = Video.objects.create(
            uploader=self.user,
            title='Video 1',
        )
        self.video2 = Video.objects.create(
            uploader=self.user,
            title='Video 2',
        )

        self.group = Group.objects.create(name='Group 1')

        self.subject = Subject.objects.create(name='Math')

        self.course = Course.objects.create(name='Course 1')

        self.profile.lector_groups.add(self.group)
        self.profile.subjects.add(self.subject)
        self.profile.lector_courses.add(self.course)

    def test_get_request(self):

        url = reverse('profile', args=[self.profile.pk])
        request = self.factory.get(url)
        request.user = self.user

        response = ProfileView.as_view()(request, pk=self.profile.pk)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.profile.name)
        self.assertContains(response, self.profile.surname)
