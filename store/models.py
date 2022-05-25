from operator import mod
from django.db import models
from django.urls import reverse

# Create your models here.


CATEGORY_CHOICES = (
    ('P', 'Phones'),
    ('T', 'Tablets'),
    ('C', 'Computing'),
    ('E', 'Electronics'),
    ('H', 'Home & Kitchen'),
    ('A', 'Accessories')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=250, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=100)
    released_on = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    label =  models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="product_images")


    def get_absolute_url(self):
        return reverse("product-detail", kwargs={
            'slug': self.slug
        })




    def __str__(self):
        return self.title
