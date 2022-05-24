from operator import mod
from django.db import models

# Create your models here.


CATEGORY_CHOICES = (
    ('P', 'Snacks'),
    ('T', 'Entre'),
    ('G', 'Drink'),
    ('A', 'Appetizer'),
    ('MC', 'Main Course')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    released_on = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    label =  models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="product_images")
