from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Ad, Post
from .forms import AdForm, PostForm

def ads_list(request):
    """List all ads ordered by date created descending"""
    ads = Ad.objects.all()
    context = {'ads': ads}
    return render(request, 'posts/ads_list.html', context)

def create_ad(request):
    """Create a new ad"""
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:ads_list')
    else:
        form = AdForm()
    context = {'form': form}
    return render(request, 'posts/create_ad.html', context)

def add_post(request, group_id):
    """Add a post for a specific group"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.fb_group_id = group_id
            post.save()
            return redirect('core:home')
    else:
        form = PostForm()
    context = {'form': form, 'group_id': group_id}
    return render(request, 'posts/add_post.html', context)
