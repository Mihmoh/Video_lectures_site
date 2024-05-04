from django import forms
from .models import Profile, Subject, Group, UserType
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    name = forms.CharField(label='Имя')
    surname = forms.CharField(label='Фамилия')
    patronymic = forms.CharField(label='Отчество')
    user_type = forms.ModelChoiceField(queryset=UserType.objects.all(), label='Тип пользователя')
    image = forms.ImageField(label='Фото', required=False)

    def clean(self):
        self.cleaned_data = super().clean()
        image = self.cleaned_data.get('image')
        if not image:
            self.cleaned_data['image'] = 'uploads/profile_pics/default.png'

    def signup(self, request, user):
        user.save()

        profile = Profile()
        profile.user = user
        profile.name = self.cleaned_data['name']
        profile.surname = self.cleaned_data['surname']
        profile.patronymic = self.cleaned_data['patronymic']
        profile.user_type = self.cleaned_data['user_type']
        profile.image = self.cleaned_data['image']
        profile.save()


