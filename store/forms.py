from pickle import FALSE
import re
from xmlrpc.client import Boolean
from django import forms
from django.forms import BooleanField, widgets
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from store.models import Comment

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    shipping_zip = forms.CharField(required=False)
   

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.BooleanField(required=False)
    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
    "class": "form-control",
    "placeholder": "Promo Code",
    "aria-label": "Recipient\'s username",
    "aria-describedby": "basi-addon2"
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
       'rows': 4 
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 

        fields = ["name", "body"]



