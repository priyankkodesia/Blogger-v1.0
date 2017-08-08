from Posts.models import PostModel,AuthorDetailModel,CommentsModel
from pagedown.widgets import PagedownWidget
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    class Meta:
        model=PostModel
        fields=['title','content','image']

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields=['username','password1','password2','first_name','last_name','email']
# 
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','password',]

class UserBioForm(forms.ModelForm):
    class Meta:
        model=AuthorDetailModel
        fields=['work','address','profile_pic','author_bio']

class CommentForm(forms.ModelForm):
    class Meta:
        model   =CommentsModel
        fields  =['content']
