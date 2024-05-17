from .models import Video, Category, Course, Comment
from profiles.models import Profile
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from .views import DetailVideo
from .forms import CommentForm


class VideoModelTestCase(TestCase):
    def setUp(self):

        user = User.objects.create(username='testuser')
        profile = Profile.objects.create(user=user, name='test_profile')

        category = Category.objects.create(name='Test Category')
        course = Course.objects.create(name='Test Course')

        video_file = SimpleUploadedFile('video.mp4', b'mock video content')
        thumbnail = SimpleUploadedFile('thumbnail.jpg', b'mock thumbnail content')
        pdf_file = SimpleUploadedFile('file.pdf', b'mock PDF content')

        self.video = Video.objects.create(
            uploader=user,
            lector=profile,
            title='Test Video',
            description='Test Description',
            video_file=video_file,
            thumbnail=thumbnail,
            date_posted=timezone.now(),
            category=category,
            course=course,
            pdf_file=pdf_file
        )

    def test_video_str_representation(self):

        expected_str = 'Test Video'
        self.assertEqual(str(self.video), expected_str)

    def test_video_fields(self):

        self.assertEqual(self.video.uploader.username, 'testuser')
        self.assertEqual(self.video.lector.name, 'test_profile')
        self.assertEqual(self.video.title, 'Test Video')
        self.assertEqual(self.video.description, 'Test Description')
        self.assertEqual(self.video.category.name, 'Test Category')
        self.assertEqual(self.video.course.name, 'Test Course')


class CommentModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')

        video = Video.objects.create(
            uploader=user,
            title='Test Video',
            description='Test Description',
            video_file='path/to/video.mp4',
            thumbnail='path/to/thumbnail.jpg',
            date_posted=timezone.now()
        )

        self.comment = Comment.objects.create(
            user=user,
            video=video,
            comment='Test Comment',
            created_on=timezone.now()
        )

    def test_comment_str_representation(self):
        expected_str = f'User: testuser | Created on: {self.comment.created_on.strftime("%b %d %Y %I:%M %p")}'
        self.assertEqual(str(self.comment), expected_str)

    def test_comment_fields(self):
        self.assertEqual(self.comment.user.username, 'testuser')
        self.assertEqual(self.comment.video.title, 'Test Video')
        self.assertEqual(self.comment.comment, 'Test Comment')
        self.assertIsNotNone(self.comment.created_on)


class DetailVideoViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create(username='testuser')

        self.video = Video.objects.create(
            uploader=self.user,
            title='Test Video',
            description='Test Description',
            video_file='path/to/video.mp4',
            thumbnail='path/to/thumbnail.jpg'
        )

    def test_get_request(self):

        request = self.factory.get('/videos/1/')
        request.user = self.user

        response = DetailVideo.as_view()(request, pk=self.video.pk)

        self.assertEqual(response.status_code, 200)

    def test_post_request(self):

        request = self.factory.post('/videos/1/', {'comment': 'Test Comment'})
        request.user = self.user

        response = DetailVideo.as_view()(request, pk=self.video.pk)

        self.assertEqual(response.status_code, 200)

        comments = Comment.objects.filter(video=self.video)
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments[0].comment, 'Test Comment')
