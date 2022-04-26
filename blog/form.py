"""imports"""
from django import forms
from .models import Comment, Post, Category

# class CategoryForm(forms.ModelForm):

choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):
    """to create post"""
    class Meta:
        """Meta Class"""
        model = Post
        fields = (
            'title',
            'slug',
            'author',
            'featured_image',
            'category',
            'content',
            'status'
        )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(
                choices=choice_list,
                attrs={'class': 'form-control'}
                ),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),

        }


class CommentForm(forms.ModelForm):
    """CommentForm class"""
    class Meta:
        """Meta Class"""
        model = Comment
        fields = ('body',)
