from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from .models import Profile, Subject, Group
from videos.models import Video
from .forms import GroupForm
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    queryset = Profile.objects.all()
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profiles = context['profiles']

        students = []
        lectors = []
        others = []

        for profile in profiles:
            if str(profile.user_type) == 'Студент':
                students.append(profile)
            elif str(profile.user_type) == 'Лектор':
                lectors.append(profile)
            else:
                others.append(profile)

        context['students'] = students
        context['lectors'] = lectors
        context['others'] = others

        return context


class GroupListView(ListView):
    model = Group
    template_name = 'profiles/group_list.html'
    queryset = Group.objects.all()
    context_object_name = 'groups'


class SubjectListView(ListView):
    model = Subject
    template_name = 'profiles/subject_list.html'
    queryset = Subject.objects.all()
    context_object_name = 'subjects'


class ProfileView(View):

    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        videos = Video.objects.all().filter(uploader=profile.user).order_by('title')
        groups = profile.lector_groups.all()
        subjects = profile.subjects.all()
        courses = profile.lector_courses.all()
        user_type = str(profile.user_type)
        if profile.user == request.user:
            can_edit = True
        else:
            can_edit = False

        context = {
            'profile': profile,
            'videos': videos,
            'can_edit': can_edit,
            'groups': groups,
            'user_type': user_type,
            'subjects': subjects,
            'courses': courses,
        }

        return render(request, 'profiles/profile.html', context)


class GroupView(View):

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
        group = Group.objects.get(pk=pk)
        students = group.student.all().order_by('surname', 'name')

        context = {
            'group': group,
            'students': students,
            'can_edit': can_edit,
        }

        return render(request, 'profiles/group.html', context)


class SubjectView(View):

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
        subject = Subject.objects.get(pk=pk)
        lectors = subject.profile_subjects.all().order_by('surname', 'name')
        courses = subject.subject_courses.all().order_by('name')

        context = {
            'subject': subject,
            'lectors': lectors,
            'can_edit': can_edit,
            'courses': courses,
        }

        return render(request, 'profiles/subject.html', context)


class UpdateProfile(UpdateView):
    model = Profile
    fields = ['name', 'surname', 'patronymic', 'subjects', 'image']
    template_name = 'profiles/update_profile.html'

    def form_valid(self, form):
        if not form.instance.image:
            form.instance.image = 'uploads/profile_pics/default.png'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

class UpdateGroup(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'profiles/update_group.html'

    def get_success_url(self):
        return reverse('group', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Profile.objects.all()
        return context

    def form_valid(self, form):
        group = form.save()
        students = form.cleaned_data['students']
        for student in students:
            student.student_group = group
            student.save()

        return super().form_valid(form)
