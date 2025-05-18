from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CommentForm

# Home view: hero + latest 3 posts
def home(request):
    latest_posts = Post.objects.all()[:3]
    return render(request, 'blogapp/home.html', {'latest_posts': latest_posts})

# Posts list view
def posts(request):
    all_posts = Post.objects.all()
    return render(request, 'blogapp/posts.html', {'posts': all_posts})

# Post detail & comment handling
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(post=post).order_by('-created')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blogapp/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })