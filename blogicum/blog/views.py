from .models import Post, Category
from .constants import N_POSTS_LIMIT

from django.http import HttpResponseNotFound
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


def index(request):
    posts = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('category').order_by('-pub_date')[:N_POSTS_LIMIT]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('category'),
        id=post_id,
        is_published=True
    )
    if post.pub_date > timezone.now():
        return HttpResponseNotFound('Этот пост еще не опубликован.')
    if post.category and not post.category.is_published:
        return HttpResponseNotFound('Категория этого поста не опубликована.')
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).select_related('category').order_by('-pub_date')

    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'posts': posts
        }
    )
