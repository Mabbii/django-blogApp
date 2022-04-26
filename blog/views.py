"""imports"""
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Category
from .form import CommentForm, PostForm


class PostList(generic.ListView):
    """PostList Class"""
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):
    """PostDetail Class"""
    def get(self, request, slug, *args, **kwargs):
        """function to get required data"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        return render(request, "post_detail.html",{
            "post": post,
            "comments": comments,
            "commented": False,
            "liked" : liked,
            "comment_form": CommentForm()
        },)

    def post(self, request, slug, *args, **kwargs):
        """function to get required data"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfuly")
        else:
            comment_form = CommentForm()
            messages.warning(request, "comment didnt added")
        return render(request, "post_detail.html",{
            "post": post,
            "comments": comments,
            "commented": True,
            "liked" : liked,
            "comment_form": CommentForm()
        },)

class PostLike(View):
    """PostLike Class View"""
    def post(self, request, slug):
        """post function"""
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class AddPost(generic.CreateView):
    """Create new Blog Post"""
    model = Post
    form_class = PostForm
    template_name = "Add_Post.html"


class UpdatePost(generic.UpdateView):
    """to update the blog"""
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'


class DeltePost(generic.DeleteView):
    """To Delte the Blog"""
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class AddCategory(generic.CreateView):
    """To add Categories"""
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'
