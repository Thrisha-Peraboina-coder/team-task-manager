from django import forms
from django.contrib.auth.models import User
from .models import Project, Membership

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=150)
    role = forms.ChoiceField(choices=Membership.ROLE_CHOICES)

    def clean_username(self):
        u = self.cleaned_data['username']
        if not User.objects.filter(username=u).exists():
            raise forms.ValidationError("User does not exist.")
        return u
