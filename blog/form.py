"""imports"""
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """CommentForm class"""
    class Meta:
        """Meta Class"""
        model = Comment
        fields = ('body',)
