from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post
from .models import Contact, Engagement
from .forms import ContactForm, EngagementForm

def view_engagements(request, post_id):
    """View all engagements for a specific post"""
    post = get_object_or_404(Post, id=post_id)
    engagements = post.engagements.all().order_by('-created_at')
    context = {'post': post, 'engagements': engagements}
    return render(request, 'engagement/view_engagements.html', context)

def add_engagement(request, post_id):
    """Add a new engagement for a post"""
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = EngagementForm(request.POST)
        if form.is_valid():
            engagement = form.save(commit=False)
            engagement.post = post
            engagement.save()
            return redirect('engagement:view_engagements', post_id=post_id)
    else:
        form = EngagementForm()
    context = {'form': form, 'post': post}
    return render(request, 'engagement/add_engagement.html', context)

def contacts_list(request):
    """List all contacts ordered by last engagement"""
    contacts = Contact.objects.all()
    context = {'contacts': contacts}
    return render(request, 'engagement/contacts_list.html', context)

def create_contact(request):
    """Create a new contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('engagement:contacts_list')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'engagement/create_contact.html', context)
