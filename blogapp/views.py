from django.shortcuts import render, get_object_or_404, redirect
from cms.models import BlogPage
from cms.models import BlogIndexPage

# Home view: hero + latest 3 posts
def home(request):
    latest_posts = BlogIndexPage.objects.all()[:3]
    blog_index = BlogIndexPage.objects.live().first()
    return render(request, 'blogapp/home.html', {
        'latest_posts': latest_posts,
        'show_loader': True,
        "blog_index": blog_index
    },
)

def post_detail(request, slug):
    post = get_object_or_404(BlogIndexPage, slug=slug)
    return render(request, 'blogapp/post_detail.html', {'post': post})