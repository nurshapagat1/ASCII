from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class AsciiArt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="My ASCII Art")
    ascii_text = models.TextField()
    is_public = models.BooleanField(default=False) # For the "upload/post" feature
    created_at = models.DateTimeField(auto_now_add=True)

    def __clstr__(self):
        return f"{self.title} by {self.user.username}"