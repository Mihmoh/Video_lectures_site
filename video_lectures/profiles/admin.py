from django.contrib import admin
from .models import Subject, Group, UserType, Profile

admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(UserType)
admin.site.register(Profile)
