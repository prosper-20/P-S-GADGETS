from pickle import FALSE
import re
from django import forms
from django.forms import widgets
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    ashipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    shipping_zip = forms.CharField(required=False)
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
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



