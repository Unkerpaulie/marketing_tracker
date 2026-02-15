from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Contact, Engagement
from posts.models import Ad, Post
from core.models import FBGroup

class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='John Doe',
            fb_url='https://facebook.com/johndoe'
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.name, 'John Doe')
        self.assertIn('facebook.com', self.contact.fb_url)

    def test_contact_str(self):
        self.assertEqual(str(self.contact), 'John Doe')

class EngagementModelTest(TestCase):
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
        self.contact = Contact.objects.create(
            name='John Doe',
            fb_url='https://facebook.com/johndoe'
        )
        self.engagement = Engagement.objects.create(
            contact=self.contact,
            post=self.post,
            content='Great post!',
            notes='Positive feedback'
        )

    def test_engagement_creation(self):
        self.assertEqual(self.engagement.contact.name, 'John Doe')
        self.assertEqual(self.engagement.content, 'Great post!')

    def test_engagement_str(self):
        self.assertIn('John Doe', str(self.engagement))
        self.assertIn('Great post', str(self.engagement))

    def test_engagement_created_at(self):
        self.assertIsNotNone(self.engagement.created_at)

class ContactsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact1 = Contact.objects.create(name='Contact 1', fb_url='https://facebook.com/contact1')
        self.contact2 = Contact.objects.create(name='Contact 2', fb_url='https://facebook.com/contact2')

    def test_contacts_list_view_status_code(self):
        response = self.client.get(reverse('engagement:contacts_list'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_list_view_template(self):
        response = self.client.get(reverse('engagement:contacts_list'))
        self.assertTemplateUsed(response, 'engagement/contacts_list.html')

    def test_contacts_list_view_context(self):
        response = self.client.get(reverse('engagement:contacts_list'))
        self.assertIn('contacts', response.context)
        contacts = response.context['contacts']
        self.assertEqual(len(contacts), 2)

class CreateContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_contact_view_get_status_code(self):
        response = self.client.get(reverse('engagement:create_contact'))
        self.assertEqual(response.status_code, 200)

    def test_create_contact_view_template(self):
        response = self.client.get(reverse('engagement:create_contact'))
        self.assertTemplateUsed(response, 'engagement/create_contact.html')

    def test_create_contact_post(self):
        data = {
            'name': 'New Contact',
            'fb_url': 'https://facebook.com/newcontact'
        }
        response = self.client.post(reverse('engagement:create_contact'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.first().name, 'New Contact')

class ViewEngagementsTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.contact = Contact.objects.create(
            name='John Doe',
            fb_url='https://facebook.com/johndoe'
        )
        self.engagement = Engagement.objects.create(
            contact=self.contact,
            post=self.post,
            content='Great post!',
            notes='Positive feedback'
        )

    def test_view_engagements_status_code(self):
        response = self.client.get(reverse('engagement:view_engagements', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_engagements_template(self):
        response = self.client.get(reverse('engagement:view_engagements', args=[self.post.id]))
        self.assertTemplateUsed(response, 'engagement/view_engagements.html')

    def test_view_engagements_context(self):
        response = self.client.get(reverse('engagement:view_engagements', args=[self.post.id]))
        self.assertIn('post', response.context)
        self.assertIn('engagements', response.context)
        engagements = response.context['engagements']
        self.assertEqual(len(engagements), 1)
