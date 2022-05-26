from operator import mod
from django.conf import settings
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
    discount_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    label =  models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="product_images")
    


    def get_absolute_url(self):
        return reverse("product-detail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
            "slug": self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={
            "slug": self.slug
        }) 


    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    strat_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    

