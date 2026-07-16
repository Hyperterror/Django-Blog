from django import forms

from .models import Post, User
class CustomForm:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'
class PostForm(CustomForm,forms.ModelForm):

    class Meta:
        model = Post
        fields = ('featured','thumbnail','title', 'text','category','tag')

class UserForm(CustomForm,forms.ModelForm):
    class Meta:
        model=User

        fields=["first_name","last_name","email",'phone_number','city','state','password','image']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(CustomForm,forms.ModelForm):
    class Meta:
        model=User
        fields=['email','password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProfileForm(CustomForm,forms.ModelForm):
    class Meta:
        model=User
        fields=["first_name","last_name","email",'phone_number','city','state','image']
    
