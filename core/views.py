from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from core.models import FBGroup
from posts.models import Post

# Create your views here.

def get_today_set():
    """
    Determine which set (A or B) should be posted to today.
    Monday, Wednesday, Friday = A
    Tuesday, Thursday, Saturday = B
    Sunday = None
    """
    weekday = datetime.now().weekday()  # 0=Monday, 6=Sunday
    if weekday in [0, 2, 4]:  # Monday, Wednesday, Friday
        return 'A'
    elif weekday in [1, 3, 5]:  # Tuesday, Thursday, Saturday
        return 'B'
    return None

def home(req):
    today = timezone.now().date()
    today_set = get_today_set()

    # Get groups for today's set
    if today_set:
        today_groups = FBGroup.objects.filter(group_set=today_set)
    else:
        today_groups = FBGroup.objects.none()

    # Get post history ordered by last_updated descending
    post_history = Post.objects.all().order_by('-last_updated')

    context = {
        'today': today,
        'today_set': today_set,
        'today_groups': today_groups,
        'post_history': post_history,
    }
    return render(req, 'index.html', context)


def group_detail(req, group_id):
    group = FBGroup.objects.get(id=group_id)
    context = {'group': group}
    return render(req, 'group_detail.html', context)


def test_lexical(req):
    """Test page for Lexical editor"""
    return render(req, 'test_lexical.html')