from urllib import response
from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class StorePage(TestCase):

    def test_homepageurl_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepageurl_url(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_homepageurl_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "store/index.html")

    def test_homepageurl_contains(self):
        response = self.client.get("/")
        self.assertContains(response, "P's GADGETS")


    # def test_productpage_status_code(self):
    #     response = self.client.get("product-detail",  kwargs={'slug': self.product.slug})
    #     self.assertEqual(response.status_code, 200)

    # def test_productpage_url(self):
    #     response = self.client.get(reverse("product-detail"))
    #     self.assertEqual(response.status_code, 200)

    def test_productpage_template_used(self):
        response = self.client.get("product-detail")
        self.assertTemplateUsed(response.status_code, 'store/product-details.html')

    def test_productpage_contains(self):
        response = self.client.get("product-detail")
        self.assertContains(response.status_code, '{{ product.title }}')