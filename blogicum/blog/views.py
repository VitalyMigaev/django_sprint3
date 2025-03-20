from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import N_POSTS_LIMIT
from .models import Category, Post


def get_published_posts(category=None, author=None, location=None):
    queryset = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('category', 'author', 'location')

    if category:
        queryset = queryset.filter(category=category)

    if author:
        queryset = queryset.filter(author=author)

    if location:
        queryset = queryset.filter(location=location)

    return queryset.order_by('-pub_date')


def index(request):
    author = request.GET.get('author')
    location = request.GET.get('location')
    posts = get_published_posts(
        author=author,
        location=location)[:N_POSTS_LIMIT]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        get_published_posts(),
        id=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    author = request.GET.get('author')
    location = request.GET.get('location')
    posts = get_published_posts(
        category=category,
        author=author,
        location=location
    )
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'posts': posts
        }
    )
