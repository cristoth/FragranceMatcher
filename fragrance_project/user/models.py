from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(default=timezone.now, blank=True, null=True)
    # profile_pics: directory to store pics
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # resize image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
