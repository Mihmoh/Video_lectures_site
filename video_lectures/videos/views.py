from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Video, Comment, Category, Course
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.list import ListView
from django.views import View
from .forms import CommentForm, CourseForm
from django.db.models import Q
from profiles.models import Profile, Group, Subject


class Index(ListView):
    model = Video
    template_name = 'videos/index.html'
    order_by = '-date_posted'


class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'lector', 'video_file', 'thumbnail', 'category']
    template_name = 'videos/create_video.html'

    def dispatch(self, request, *args, **kwargs):
        user_type = str(request.user.profile.user_type)
        if user_type != 'Лектор':
            return redirect('not-lector')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.pk})


class DetailVideo(View):
    def get(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:15]
        course_videos = Video.objects.filter(course=video.course)[:15]
        context = {
            'object': video,
            'comments': comments,
            'form': form,
            'categories': categories,
            'course_videos': course_videos,
        }
        return render(request, 'videos/detail_video.html', context)

    def post(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(user=self.request.user,
                              comment=form.cleaned_data['comment'],
                              video=video)
            comment.save()
        else:
            print("not valid")

        comments = Comment.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:15]
        course_videos = Video.objects.filter(course=video.course)[:15]
        context = {
            'object': video,
            'comments': comments,
            'form': form,
            'categories': categories,
            'course_videos': course_videos,
        }
        return render(request, 'videos/detail_video.html', context)


class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    template_name = 'videos/create_video.html'
    fields = ['title', 'description', 'lector']

    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class DeleteVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'

    def get_success_url(self):
        return reverse('index')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class VideoCategoryList(View):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        videos = Video.objects.filter(category=pk).order_by('-date_posted')
        context = {
            'category': category,
            'videos': videos,
        }

        return render(request, 'videos/video_category.html', context)


class SearchVideo(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        query_video = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(uploader__username__icontains=query)
        )
        query_courses = Course.objects.filter(
            Q(name__icontains=query)
        )
        query_profiles = Profile.objects.filter(
            Q(surname__icontains=query) |
            Q(name__icontains=query) |
            Q(patronymic__icontains=query)
        )
        query_subjects = Subject.objects.filter(
            Q(name__icontains=query)
        )
        query_groups = Group.objects.filter(
            Q(name__icontains=query)
        )

        context = {
            'query_video': query_video,
            'query_courses': query_courses,
            'query_profiles': query_profiles,
            'query_subjects': query_subjects,
            'query_groups': query_groups,

        }

        return render(request, 'videos/search.html', context)


class RegistrationChoiceView(View):
    def get(self, request):

        return render(request, 'videos/registration_choice.html')


class NotLectorView(TemplateView):
    template_name = 'videos/not_lector.html'


class CourseView(View):

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        can_edit = False
        if hasattr(user, 'profile'):
            profile = user.profile
            user_type = str(profile.user_type)
            if user_type == 'Лектор':
                can_edit = True
        else:
            can_edit = False
        course = Course.objects.get(pk=pk)
        videos = course.course_videos.all().order_by('title')

        context = {
            'course': course,
            'videos': videos,
            'can_edit': can_edit,
        }

        return render(request, 'videos/course.html', context)


class CourseListView(ListView):
    model = Course
    template_name = 'videos/course_list.html'
    queryset = Course.objects.all()
    context_object_name = 'courses'


class UpdateCourse(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'videos/update_course.html'

    def get_success_url(self):
        return reverse('course', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context

    def form_valid(self, form):
        course = form.save()
        videos = form.cleaned_data['videos']
        for video in videos:
            video.course = course
            video.save()

        return super().form_valid(form)


class CreateCourse(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'videos/create_course.html'

    def get_success_url(self):
        return reverse('course', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context

    def form_valid(self, form):
        course = form.save()
        videos = form.cleaned_data['videos']
        for video in videos:
            video.course = course
            video.save()

        return super().form_valid(form)
