from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User

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
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(usermame=username).exists():
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
                messages.success(request, f"Hi {username}, your account has been created succesfully!")
                return redirect('/')
        else:
            messages.info(request, "Both password fields didn't match")
            return redirect("/")
    return render(request, 'users/register_2.html')

            

