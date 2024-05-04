from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field, user_email
from allauth.utils import generate_unique_username
from django.conf import settings
from .models import Lector


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        # Создаем профиль лектора
        lector = Lector()
        lector.user = user
        lector.name = form.cleaned_data['name']
        lector.surname = form.cleaned_data['surname']
        lector.patronymic = form.cleaned_data['patronymic']
        lector.save()

        return user