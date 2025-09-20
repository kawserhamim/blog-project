from django import forms
from . import models

class PostForm(forms.Form):
    class Meta:
        model = models.Post
        fields = ['content','title','tag','category']

class CommentForm(forms.Form):
    class Meta:
        model = models.Comment
        fields = ['content']