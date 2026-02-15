from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Ad, Post
from core.models import FBGroup

class AdModelTest(TestCase):
    def setUp(self):
        self.ad = Ad.objects.create(
            name='Test Ad',
            text='This is a test ad with **bold** and *italic* text'
        )

    def test_ad_creation(self):
        self.assertEqual(self.ad.name, 'Test Ad')
        self.assertIn('bold', self.ad.text)

    def test_ad_str(self):
        self.assertEqual(str(self.ad), 'Test Ad')

    def test_ad_created_at(self):
        self.assertIsNotNone(self.ad.created_at)

class PostModelTest(TestCase):
    def setUp(self):
        self.group = FBGroup.objects.create(
            name='Test Group',
            group_url='https://facebook.com/groups/test',
            group_set='A'
        )
        self.ad = Ad.objects.create(
            name='Test Ad',
            text='Test ad text'
        )
        self.post = Post.objects.create(
            ad=self.ad,
            fb_group=self.group,
            post_url='https://facebook.com/posts/123',
            posted_at=timezone.now()
        )

    def test_post_creation(self):
        self.assertEqual(self.post.ad.name, 'Test Ad')
        self.assertEqual(self.post.fb_group.name, 'Test Group')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Ad in Test Group')

    def test_post_engagement_count(self):
        self.assertEqual(self.post.engagement_count(), 0)

    def test_post_last_updated(self):
        self.assertIsNotNone(self.post.last_updated)

class AdsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.ad1 = Ad.objects.create(name='Ad 1', text='Text 1')
        self.ad2 = Ad.objects.create(name='Ad 2', text='Text 2')

    def test_ads_list_view_status_code(self):
        response = self.client.get(reverse('posts:ads_list'))
        self.assertEqual(response.status_code, 200)

    def test_ads_list_view_template(self):
        response = self.client.get(reverse('posts:ads_list'))
        self.assertTemplateUsed(response, 'posts/ads_list.html')

    def test_ads_list_view_context(self):
        response = self.client.get(reverse('posts:ads_list'))
        self.assertIn('ads', response.context)
        ads = response.context['ads']
        self.assertEqual(len(ads), 2)

class CreateAdViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_ad_view_get_status_code(self):
        response = self.client.get(reverse('posts:create_ad'))
        self.assertEqual(response.status_code, 200)

    def test_create_ad_view_template(self):
        response = self.client.get(reverse('posts:create_ad'))
        self.assertTemplateUsed(response, 'posts/create_ad.html')

    def test_create_ad_post(self):
        data = {
            'name': 'New Ad',
            'text': 'New ad text'
        }
        response = self.client.post(reverse('posts:create_ad'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(Ad.objects.first().name, 'New Ad')
