from django import forms

from .models import Post, User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('featured','thumbnail','title', 'text','category','tag')

class UserForm(forms.ModelForm):
    class Meta:
        model=User

        fields=["first_name","last_name","email",'phone_number','city','state','password','image']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["first_name","last_name","email",'phone_number','city','state','image']
    
