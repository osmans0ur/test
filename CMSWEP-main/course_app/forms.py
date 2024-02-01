# course_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Discussion, Comment

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    class Meta:
        model = CustomUser 
        fields = ['username', 'password']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']

    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField(required=False)

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'file']

class YourForm(forms.Form):
    topic = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
