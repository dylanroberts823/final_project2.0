from django.forms import ModelForm
from django.forms import forms
from users.models import Project, Tag, Request

class SearchForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']

class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'contributors', 'tags']

class CreateRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['note']

class CreateTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']
