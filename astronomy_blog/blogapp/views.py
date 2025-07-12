from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CommentForm
from wagtail.models import Page
from cms.models import BlogIndexPage

# Home view: hero + latest 3 posts
def home(request):
    latest_posts = Post.objects.all()[:3]
    blog_index = BlogIndexPage.objects.live().first()
    return render(request, 'blogapp/home.html', {
        'latest_posts': latest_posts,
        'show_loader': True,
        "blog_index": blog_index
    },
    )



def about_view(request):
    return render(request, 'blogapp/about.html')
