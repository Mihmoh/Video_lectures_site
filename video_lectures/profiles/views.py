from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from .models import Profile
from videos.models import Video
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic import FormView
from allauth.account.views import SignupView


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    queryset = Profile.objects.all()
    context_object_name = 'profiles'


class ProfileView(View):

    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        videos = Video.objects.all().filter(uploader=profile.user).order_by('-date_posted')
        if profile.user == request.user:
            can_edit = True
        else:
            can_edit = False

        context = {
            'profile': profile,
            'videos': videos,
            'can_edit': can_edit,
        }

        return render(request, 'profiles/profile.html', context)


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


# class LectorView(View):
#
#     def get(self, request, pk, *args, **kwargs):
#         lector = get_object_or_404(Lector, pk=pk)
#         videos = Video.objects.all().filter(uploader=lector.user).order_by('-date_posted')
#         if lector.user == request.user:
#             can_edit = True
#         else:
#             can_edit = False
#
#         context = {
#             'lector': lector,
#             'videos': videos,
#             'can_edit': can_edit,
#         }
#
#         return render(request, 'profiles/lector.html', context)
#
#
# class UpdateLector(UpdateView):
#     model = Lector
#     fields = ['name', 'surname', 'patronymic', 'image']
#     template_name = 'profiles/update_lector.html'
#
#     def form_valid(self, form):
#         if not form.instance.image:
#             form.instance.image = 'uploads/profile_pics/default.png'
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('lector', kwargs={'pk': self.object.pk})


# class DynamicSignupView(SignupView):
#     def get_form_class(self):
#         user_type = self.request.GET.get('user_type')
#         if user_type == 'student':
#             return StudentRegistrationForm
#         elif user_type == 'lector':
#             return LectorRegistrationForm
#         else:
#             return super().get_form_class()
