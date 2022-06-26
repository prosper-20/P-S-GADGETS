from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from sendgrid.helpers.mail import SandBoxMode, MailSettings
from store.models import Product
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hi {username}, your account has been created succesfully!")
            return redirect('/')
    else:
        form = UserRegisterForm()
    context = {
        "form": form
    }
    return render(request, 'users/register.html', context)


def register2(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken already')
                return redirect("register")
            else:
                user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                user.save()
                # For sending mails
                products = Product.objects.filter(type="F")[:4]
                accessories = Product.objects.filter(category="A").all()
                mydict = {'username': username, 'products':products, 'accessories': accessories}
                html_template = 'users/welcome_4.html' #Changed it from users/welcome_email.html to welcome_email_3.html
                html_message = render_to_string(html_template, context=mydict)
                subject = "Welcome!!! P's Gadgets"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
                message.content_subtype = 'html'
                message.send()
                messages.success(request, f"Hi {username}, your account has been created succesfully!")
                return redirect('login')
        else:
            messages.info(request, "Both password fields didn't match")
            return redirect("/")
    return render(request, 'users/register_2.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, f"Welcome back {username}!")
            return redirect("/")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("/")

    return render(request, "users/login.html")

def logout(request):
    auth.logout(request)
    messages.success(request, 'See you soon!')
    return redirect("/")



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


            

