from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from PIL import Image

# Create your models here.
class Fragrance(models.Model):
    name = models.CharField(max_length=255, unique=True)
   
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Perfume(models.Model):
    TARGET_CHOICES = [
        ('men', 'men'),
        ('women', 'women'),
        ('unisex', 'unisex'),
    ]

    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_posted = models.DateField(default=timezone.now)
    target = models.CharField(max_length=15, choices=TARGET_CHOICES, null=True)

    image = models.ImageField(
        default='default_perfume.png', upload_to='perfume_pics')

    fragrances = models.ManyToManyField(
        Fragrance, through="Perfume_Fragrance")

    
    # hit_count_generic = GenericRelation(HitCount,
    #                                     object_id_field='object_pk',
    #                                     related_query_name='hit_count_generic_relation')  # nr. views

    class Meta:
        ordering = ['-date_posted', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # returns full-path as a string
        return reverse('perfume-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # resize image
        img = Image.open(self.image.path)
        if img.height > 350 or img.width > 400:
            output_size = (350, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)




class Perfume_Fragrance(models.Model):
    UNIT_CHOICES = [
        ('oz', 'ounce'),
        ('ml', 'mililitre'),
        ('l', 'litre'),
        ('g', 'gram')
    ]
    quantity = models.FloatField()
    unit = models.CharField(max_length=15, choices=UNIT_CHOICES, null=True)
    fragrance = models.ForeignKey(Fragrance, on_delete=models.CASCADE)
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
