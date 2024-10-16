from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full h-40 border border-gray-300 rounded-lg p-2',
            'placeholder': 'Write your post...'
        })
    )

    class Meta:
        model = Post
        fields = ['image', 'content']
        

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
