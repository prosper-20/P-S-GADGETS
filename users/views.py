from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Hi {username}, your account has been created succesfully!")
            return redirect('/')
    else:
        form = UserRegisterForm()
    context = {
        "form": form
    }
    return render(request, 'users/register.html', context)
