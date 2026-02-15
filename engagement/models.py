from django.db import models
from posts.models import Post

class Contact(models.Model):
    name = models.CharField(max_length=200)
    fb_url = models.URLField()

    def __str__(self):
        return self.name
    
class Engagement(models.Model):
    contact = models.ForeignKey(Contact, related_name='engagements', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='engagements', on_delete=models.CASCADE)
    content = models.TextField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    message_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.contact.name} - {self.content[:20]}..."
