from django.db import models
from core.models import FBGroup

class Ad(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
    
class Post(models.Model):
    ad = models.ForeignKey(Ad, related_name='posts', on_delete=models.CASCADE)
    fb_group = models.ForeignKey(FBGroup, on_delete=models.CASCADE)
    post_url = models.URLField()
    posted_at = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ad.name} in {self.fb_group.name}"

    def engagement_count(self):
        return self.engagements.count()
