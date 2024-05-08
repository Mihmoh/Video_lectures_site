from django import forms
from .models import Profile, Subject, Group, UserType
from django.contrib.auth.models import User
from django.db.models import Q


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


# class GroupForm(forms.ModelForm):
#
#     search_query = forms.CharField(
#         label='Поиск студентов',
#         required=False,
#         widget=forms.TextInput(attrs={'placeholder': 'Введите имя или фамилию студента'})
#     )
#
#     queryset = Profile.objects.filter(user_type__name='Студент')
#
#     students = forms.ModelMultipleChoiceField(
#         queryset=queryset,
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#
#     apply_search = forms.BooleanField(
#         label='Применить поиск',
#         required=False
#     )
#
#     class Meta:
#         model = Group
#         fields = ['name', 'lector', 'students', 'apply_search']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['students'].queryset = Profile.objects.filter(user_type__name='Студент')
#
#         search_query = self.data.get('search_query')
#         apply_search = self.data.get('apply_search')
#
#         if apply_search and search_query:
#             self.fields['students'].queryset = self.fields['students'].queryset.filter(
#                 Q(surname__icontains=search_query) | Q(name__icontains=search_query)
#             )


class GroupForm(forms.ModelForm):
    queryset = Profile.objects.filter(user_type__name='Студент')

    students = forms.ModelMultipleChoiceField(
        queryset=queryset.order_by('student_group', 'surname', 'name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'lector', 'students']

