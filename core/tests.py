from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from .models import FBGroup
from posts.models import Ad, Post
from engagement.models import Contact, Engagement

class FBGroupModelTest(TestCase):
    def setUp(self):
        self.group_a = FBGroup.objects.create(
            name='Test Group A',
            group_url='https://facebook.com/groups/test-a',
            group_set='A'
        )
        self.group_b = FBGroup.objects.create(
            name='Test Group B',
            group_url='https://facebook.com/groups/test-b',
            group_set='B'
        )

    def test_fbgroup_creation(self):
        self.assertEqual(self.group_a.name, 'Test Group A')
        self.assertEqual(self.group_a.group_set, 'A')

    def test_fbgroup_str(self):
        self.assertEqual(str(self.group_a), 'Test Group A (A)')

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.group_a = FBGroup.objects.create(
            name='Test Group A',
            group_url='https://facebook.com/groups/test-a',
            group_set='A'
        )
        self.ad = Ad.objects.create(
            name='Test Ad',
            text='Test ad text'
        )
        self.post = Post.objects.create(
            ad=self.ad,
            fb_group=self.group_a,
            post_url='https://facebook.com/posts/123',
            posted_at=timezone.now()
        )

    def test_home_view_status_code(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_home_view_context(self):
        response = self.client.get(reverse('core:home'))
        self.assertIn('today', response.context)
        self.assertIn('today_set', response.context)
        self.assertIn('today_groups', response.context)
        self.assertIn('post_history', response.context)

    def test_home_view_post_history(self):
        response = self.client.get(reverse('core:home'))
        posts = response.context['post_history']
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].ad.name, 'Test Ad')
