from email.policy import default
import imp
from itertools import product
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, Address, Payment, Coupon, Refund, Address, UserProfile, Question
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm, CommentForm
import stripe
import random
import string
from store.models import Comment
from .forms import CommentForm, ContactForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

class tester(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            products = Product.objects.filter(type="F")[:4]
            products2 = Product.objects.filter(type="F")[3:7]
            electronics = Product.objects.filter(category="E").all()
            phones = Product.objects.filter(category="P").all()
            tablets = Product.objects.filter(category="T").all()
            accessories = Product.objects.filter(category="A").all()
            home_kitchen = Product.objects.filter(category="H").all()
            camera = Product.objects.filter(category="CA").all()
            computing = Product.objects.filter(category="C").all()
            clothing = Product.objects.filter(category="CL").all()
            food_and_beverages = Product.objects.filter(category="FB").all()
            sound_and_vision = Product.objects.filter(category="S").all()
            latests = Product.objects.filter(type="L")
            sidebar = Product.objects.filter(type="S")
            products_total = Product.objects.all()
            context = {
                'object': order,
                'DISPLAY_COUPON_FORM': True,
                'couponform': CouponForm(),

                'products': products,
                'latests': latests,
                "products2": products2,
                "sidebar": sidebar,
                "electronics": electronics,
                "phones": phones,
                "tablets": tablets,
                "accessories": accessories,
                'home_kitchen': home_kitchen,
                "camera": camera,
                "computing": computing,
                "food_and_beverages": food_and_beverages,
                "clothing": clothing,
                "sound_and_vision": sound_and_vision,
                "products_total": products_total
            }
            return render(self.request, "store/order_summary_2.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('/')


def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=20))

def search_products(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # This returns the results of the user's search
        items = Product.objects.filter(slug__icontains=searched)
        # items_all = Item.objects.all()
        # rice_items = Item.objects.filter(title__icontains="rice")
        # You cahneged from new_search_posts.html to ....
        return render(request, "store/search_products.html", {'searched': searched, 'items': items})
    else:
        return render(request, "store/search_products.html")




class ProductCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "store/post_comment_form.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.product_id = self.kwargs['slug']
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('product-detail', kwargs={'slug': self.kwargs['slug']})


def ProductCommentView2(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get("name")
            messages.success(request, f"Comment has been saved")
            return redirect('/')
    else:
        form = CommentForm()
    context = {
        "form": form
    }
    return render(request, 'store/post_comment_form_2.html', form)

class Home(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = "products"
    
class HomeView(View):
    def get(self, *args, **kwargs):
        products = Product.objects.filter(type="F")[:4]
        products2 = Product.objects.filter(type="F")[3:7]
        electronics = Product.objects.filter(category="E").all()
        phones = Product.objects.filter(category="P").all()
        tablets = Product.objects.filter(category="T").all()
        accessories = Product.objects.filter(category="A").all()
        home_kitchen = Product.objects.filter(category="H").all()
        camera = Product.objects.filter(category="CA").all()
        computing = Product.objects.filter(category="C").all()
        clothing = Product.objects.filter(category="CL").all()
        food_and_beverages = Product.objects.filter(category="FB").all()
        sound_and_vision = Product.objects.filter(category="S").all()
        latests = Product.objects.filter(type="L")
        sidebar = Product.objects.filter(type="S")
        products_total = Product.objects.all()
        context = {
            'products': products,
            'latests': latests,
            "products2": products2,
            "sidebar": sidebar,
            "electronics": electronics,
            "phones": phones,
            "tablets": tablets,
            "accessories": accessories,
            'home_kitchen': home_kitchen,
            "camera": camera,
            "computing": computing,
            "food_and_beverages": food_and_beverages,
            "clothing": clothing,
            "sound_and_vision": sound_and_vision,
            "products_total": products_total
            }
    


        return render(self.request, 'store/index.html', context)




def is_valid_form(values):
    valid = True
    for field in values:
        if field == "":
            valid = False
    return valid




class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
            'form': form,
            'couponform': CouponForm(),
            'order': order,
            'DISPLAY_COUPON_FORM': True,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type="S",
                default=True
            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type="B",
                default=True
            )
            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})

            # You changed this from checkout_page_@.html to 
            return render(self.request, "store/checkout_3.html", context)   
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order')
            return redirect("checkout")

        

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type="S",
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip ]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address = shipping_address1,
                            apartment_address = shipping_address2,
                            country=shipping_country,
                            zip =shipping_zip,
                            address_type="S"
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get("set_default_shipping")
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required shipping address fields")

                    
                use_default_billing = form.cleaned_data.get('use_default_shipping')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = "B"
                    billing_address.save()
                    order.billig_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the default billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type="B",
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip ]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address = billing_address1,
                            apartment_address = billing_address2,
                            country=billing_country,
                            zip =billing_zip,
                            address_type="B"
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get("set_default_billing")
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required billing address fields")

                

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == "S":
                    return redirect("payment", payment_option="stripe")
                elif payment_option == "P":
                    return redirect("payment", payment_option="paypal")
                else:
                    messages.warning(self.request, "Invalid Payment Option Selected")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            # We changed this from order-summary to tester
            return redirect('tester')

    
class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                "order": order,
                'DISPLAY_COUPON_FORM': False,
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                cards = stripe.Customer.list_sources(
                    userprofile.stripe.customer_id,
                    limit=3,
                    object="card"
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, 'store/payment.html', context)
        else:
            messages.warning(self.request, "You have not added a billing address")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

        amount = int(order.get_total() * 100)

        try:
            if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                charge = stripe.Charge.create(
                    amount=amount,  # cents
                    currency="usd",
                    customer=userprofile.stripe_customer_id
                )
            else:
                charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                )
        
            
            # Creating the payment
            payment = Payment()
            payment.stripe_charge_id=charge["id"]
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # Assign payment to order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()
            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()


            messages.success(self.request, "Your order was successful")
            return redirect("/")
            
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("home")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate Limit Error")
            return redirect("home")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid Request Error")
            return redirect("home")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Oops! Authentication Error")
            return redirect("home")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Connection couldn't be established")
            return redirect("home")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request, "Something went wrong. Pls try again")
            return redirect("home")
        except Exception as e:
            # Send an email
            messages.warning(self.request, "A serious error occured, we are on it.")
            return redirect("home")

        # messages.warning(self.request, "Invalid data received")
        # return redirect("payment")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            # You changed this from store/order-summary.html to order_summary_2.html
            return render(self.request, "store/order_summary_2.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('/')


# def home(request):
#     products = Product.objects.all()
#     context = {
#         "products": products
#     }
#     return render(request, 'store/index.html', context)

# def detail(request, slug=None):
#     product = Product.objects.get(slug=slug)

#     context = {
#         "product": product
#     }
#     return render(request, 'store/product-details.html', context)

class Detail(DetailView):
    # model = Product
    # template_name = "store/product-details.html"
    # context_object_name = "product"
    def get(self, request, slug, *args, **kwargs):
        product = Product.objects.get(slug=slug)
        electronics = Product.objects.filter(category="E").all()
        phones = Product.objects.filter(category="P").all()
        tablets = Product.objects.filter(category="T").all()
        accessories = Product.objects.filter(category="A").all()
        home_kitchen = Product.objects.filter(category="H").all()
        camera = Product.objects.filter(category="CA").all()
        computing = Product.objects.filter(category="C").all()
        clothing = Product.objects.filter(category="CL").all()
        food_and_beverages = Product.objects.filter(category="FB").all()
        sound_and_vision = Product.objects.filter(category="S").all()
        sidebar = Product.objects.filter(type="S"),
        comment_form = CommentForm()

        context = {
        'product': product,
        "electronics": electronics,
        "phones": phones,
        "tablets": tablets,
        "accessories": accessories,
        'home_kitchen': home_kitchen,
        "camera": camera,
        "computing": computing,
        "food_and_beverages": food_and_beverages,
        "clothing": clothing,
        "sound_and_vision": sound_and_vision,
        "sidebar": sidebar,
        "comment_form": comment_form,
        }

        return render(self.request, 'store/product-details.html', context)


    def post(self, request, slug, *args, **kwargs):
        template_name = 'store/comment_tester.html'
        product = get_object_or_404(Product, slug=slug)
        comments = product.comments.filter(active=True)
        new_comment = None
        # Comment posted
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():

                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.product = product
                # Save the comment to the database
                new_comment.save()
                return redirect("product-details", args=[str(self.slug)])
        else:
            comment_form = CommentForm()

        return render(request, template_name, {'product': product,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})




@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity has been updated")
            # Changed from order-summary to tester
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            # Changed from order-summary to tester
            return redirect("tester")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        # Changed from order-summary to tester
        return redirect("tester")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart!")
            # Changed from order-summary to tester
            return redirect("tester")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("product-detail", slug=slug)

    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product-detail", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            # Changed from order-summary to tester
            return redirect("tester")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("product-detail", slug=slug)

    else:
        messages.info(request, "You do not have an active order.")
        return redirect("product-detail", slug=slug)

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon doesn't exist")
        return redirect("checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get("code")
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code=code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                # You changed it from home to checkout
                return redirect("checkout")

            except ObjectDoesNotExist:
                messages.info(self.request, 'You do not have an active order')
                return redirect("checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            "form": form
        }
        return render(self.request, 'store/request_refund.html', context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get("message")
            email = form.cleaned_data.get("email")
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received")
                return redirect('request-refund')

            except ObjectDoesNotExist:
                messages.warning(self.request, "This order doesn't exist")
                return redirect('request-refund')



# SEPARATE VIEWS FOR EACH CATEGORY

def phone_view(request):
    phones = Product.objects.filter(category="P").all()
    context = {
        "phones": phones
    }
    return render(request, 'store/phones.html', context)

def accessories_view(request):
    accessories = Product.objects.filter(category="A").all()
    context = {
        "accessories": accessories
    }
    return render(request, 'store/accessories.html', context)


def tablets_view(request):
    tablets = Product.objects.filter(category="T").all()
    context = {
        "tablets": tablets
    }
    return render(request, 'store/tablets.html', context)

def camera_view(request):
    camera = Product.objects.filter(category="CA").all()
    context = {
        "camera": camera
    }
    return render(request, 'store/camera.html', context)

def computing_view(request):
    computing = Product.objects.filter(category="C").all()
    context = {
        "computing": computing
    }
    return render(request, 'store/computing.html', context)

def discount_view(request):
    products = Product.objects.all()
    lis = []
    for product in products:
        if product.discount_price:
            lis.append(product)
    context = {
        "lis": lis,
        # You just added these for the side bar context
        "electronics" : Product.objects.filter(category="E").all(),
        "phones": Product.objects.filter(category="P").all(),
        "tablets" : Product.objects.filter(category="T").all(),
        "accessories" : Product.objects.filter(category="A").all(),
        "home_kitchen" : Product.objects.filter(category="H").all(),
        "camera" : Product.objects.filter(category="CA").all(),
        "computing" : Product.objects.filter(category="C").all(),
        "clothing" : Product.objects.filter(category="CL").all(),
        "food_and_beverages" : Product.objects.filter(category="FB").all(),
        "sound_and_vision" : Product.objects.filter(category="S").all()
    }

    return render(request, 'store/discount.html', context)


def food_view(request):
    food_and_beverages = Product.objects.filter(category="FB").all()
    context = {
        "food_and_beverages": food_and_beverages
    }

    return render(request, 'store/food_and_beverages.html', context)


def clothing_view(request):
    clothing = Product.objects.filter(category="CL").all()
    context = {
        "clothing": clothing
    }

    return render(request, 'store/clothing.html', context)

def sound_view(request):
    sound_and_vision = Product.objects.filter(category="S").all()
    context = {
        "sound_and_vision": sound_and_vision
    }
    return render(request, 'store/sound_and_vision.html', context)


def home_and_kitchen(request):
    home_kitchen = Product.objects.filter(category="H").all()
    context = {
        "home_kitchen": home_kitchen
    }
    return render(request, 'store/home_and_kitchen.html', context)



def contact(request):
    if request.method  == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            messages.success(request, f"Hi {username}, your message has been received. Please check your mail for a reply")
            return redirect("contact")
    else:
        form = ContactForm()
    context = {
        "form": form
    }
    return render(request, 'store/contact.html', context)


def faq(request):
    return render(request, 'store/faq.html')


def question(request):
    questions = Question.objects.all()
    context = {
        "questions": questions
    }
    return render(request, 'store/faq2.html', context)


def QuestionDetail(request, slug):
    question = Question.objects.get(slug=slug)
    context = {
        "question": question
    }

    return render(request, 'store/faq3.html', context) #You changed the template from store/question_details.html to faq3.html



def search_questions(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # This returns the results of the user's search
        items = Question.objects.filter(slug__icontains=searched)
        # items_all = Item.objects.all()
        # rice_items = Item.objects.filter(title__icontains="rice")
        # You cahneged from new_search_posts.html to ....
        return render(request, "store/search_questions.html", {'searched': searched, 'items': items})
    else:
        return render(request, "store/search_questions.html")


def post_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    comments = product.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'store/comment_tester.html', {'product': product,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def normal(request):
    return render(request, 'store/normal.html')

