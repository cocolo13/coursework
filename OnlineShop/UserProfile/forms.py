from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    last_name = forms.CharField(label='Имя')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = UserProfile
        fields = ['gender']
        widgets = {
            'gender': forms.RadioSelect(choices=[("Мужской", "Мужской"), ("Женский", "Женский")])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile