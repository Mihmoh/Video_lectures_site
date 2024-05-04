from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    patronymic = models.CharField(max_length=100, blank=True)
    subjects = models.ManyToManyField('Subject')
    groups = models.ManyToManyField('Group')
    image = models.ImageField(upload_to='uploads/profile_pics', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


# class Lector(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, blank=True)
#     surname = models.CharField(max_length=100, blank=True)
#     patronymic = models.CharField(max_length=100, blank=True)
#     subjects = models.ManyToManyField('Subject')
#     groups = models.ManyToManyField('Group')
#     image = models.ImageField(upload_to='uploads/profile_pics', blank=True)
#
#     def __str__(self):
#         return f'{self.user.username} Лектор'


class Group(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name





# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, blank=True)
#     surname = models.CharField(max_length=100, blank=True)
#     patronymic = models.CharField(max_length=100, blank=True)
#     subjects = models.ManyToManyField('Subject')
#     groups = models.ManyToManyField('Group')
#     image = models.ImageField(upload_to='uploads/profile_pics', blank=True)
#
#     def __str__(self):
#         return f'{self.user.username} Студент'
