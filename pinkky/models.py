from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location ({self.latitude}, {self.longitude})"
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  
    content = models.TextField()
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
