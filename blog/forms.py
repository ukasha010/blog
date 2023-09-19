from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post , comment

"""class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title' , 'content'] """

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput({'placeholder' : 'Comment'}))
    class Meta:
        model = comment
        fields = ['comment'] 