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
    student_group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, related_name='student', blank=True)
    image = models.ImageField(upload_to='uploads/profile_pics', blank=True)
    subjects = models.ManyToManyField('Subject', related_name='profile_subjects', blank=True)

    def __str__(self):
        if self.student_group:
            return f' {self.surname}  {self.name}  {self.patronymic} | {self.user_type} | {self.student_group}'
        else:
            return f' {self.surname}  {self.name}  {self.patronymic} | {self.user_type} '


class Group(models.Model):
    name = models.CharField(max_length=100)
    lector = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='lector_groups', blank=True)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    lectors = models.ManyToManyField(Profile, related_name='subject_profiles', blank=True)


    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name

