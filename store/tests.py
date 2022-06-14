from urllib import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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

    # def test_productpage_template_used(self):
    #     response = self.client.get(reverse("product-detail"))
    #     self.assertTemplateUsed(response, 'store/product-details.html')

    # def test_productpage_contains(self):
    #     response = self.client.get(reverse("product-detail"))
    #     self.assertContains(response, "P's GADGETS")


class UserPageTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username = 'esther',
            email = 'esther@gmail.com',
            password = 'testing321'
        )
        self.assertEqual(user.username, 'esther')
        self.assertEqual(user.email, 'esther@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    
    def test_user_registration_status_code(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_user_registration_template(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_user_registration_page_contains(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "P's Gadgets | Sign In")

    def test_user_registration_page_not_contained(self):
        response = self.client.get(reverse("login"))
        self.assertNotContains(response, 'This is John')
