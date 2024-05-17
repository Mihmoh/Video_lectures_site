from django import forms
from .models import Video, Course
from profiles.models import Profile



class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Здесь можно оставить комментарий"
        }))


class CourseForm(forms.ModelForm):
    queryset = Video.objects.all()

    videos = forms.ModelMultipleChoiceField(
        queryset=queryset.order_by('-date_posted'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Course
        fields = ['name', 'lector', 'subject', 'videos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lector'].queryset = Profile.objects.filter(user_type__name='Лектор')
        if self.instance.pk:
            self.fields['videos'].initial = self.instance.course_videos.values_list('pk', flat=True)

    def save(self, commit=True):
        course = super().save(commit=commit)
        if commit:
            course.course_videos.set(self.cleaned_data['videos'])
        return course
