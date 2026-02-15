from django.db import models

class FBGroup(models.Model):
    SET_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
    )
    name = models.CharField(max_length=200)
    group_url = models.URLField()
    group_set = models.CharField(max_length=1, choices=SET_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.group_set})"
    
