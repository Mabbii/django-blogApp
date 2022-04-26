"""imports"""
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Category(models.Model):
    """To categorize post accourdingly"""
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """retrn back to home"""
        return reverse('home')


class Post(models.Model):
    """Post Model"""
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    category = models.CharField(max_length=250, default='default')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        """to get data"""
        ordering = ['-created_on']

    def __str__(self):
        return str(self.title)

    def number_of_likes(self):
        """to count total number of likes"""
        return self.likes.count()

    def get_absolute_url(self):
        """return to required page"""
        return reverse('post_detail', args=[str(self.slug)])


class Comment(models.Model):
    """Comment class"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """to get data"""
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
