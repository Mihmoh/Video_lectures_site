from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from .models import Profile, Subject, Group
from videos.models import Video
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.forms.models import inlineformset_factory


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    queryset = Profile.objects.all()
    context_object_name = 'profiles'


class GroupListView(ListView):
    model = Group
    template_name = 'profiles/group_list.html'
    queryset = Group.objects.all()
    context_object_name = 'groups'


class ProfileView(View):

    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        videos = Video.objects.all().filter(uploader=profile.user).order_by('-date_posted')
        groups = profile.lector_groups.all()
        user_type = str(profile.user_type)
        if profile.user == request.user:
            can_edit = True
        else:
            can_edit = False
        if profile.subjects == 'profiles.Subject.None':
            has_subjects = True
        else:
            has_subjects = False

        context = {
            'profile': profile,
            'videos': videos,
            'can_edit': can_edit,
            'has_subjects': has_subjects,
            'groups': groups,
            'user_type': user_type,
        }

        return render(request, 'profiles/profile.html', context)


class GroupView(View):

    def get(self, request, pk, *args, **kwargs):
        group = Group.objects.get(pk=pk)
        students = group.student.all()

        context = {
            'group': group,
            'students': students,
        }

        return render(request, 'profiles/group.html', context)

class UpdateProfile(UpdateView):
    model = Profile
    fields = ['name', 'surname', 'patronymic', 'subjects', 'groups', 'image']
    template_name = 'profiles/update_profile.html'

    def form_valid(self, form):
        if not form.instance.image:
            form.instance.image = 'uploads/profile_pics/default.png'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

