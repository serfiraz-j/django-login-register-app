from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import LoginUserForm, NewUserForm, UserPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm

    
def login(request):
   if request.user.is_authenticated:
     return render(request, "welcome.html")

   if request.method == "POST":
      form = LoginUserForm(request, data=request.POST)
      if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        remember_me = form.cleaned_data.get("remember_me")
        user = authenticate(request, username=username, password=password)
        nextUrl = request.GET.get('next', None)
        if user is not None:
          auth_login(request, user)
          if not remember_me:
            request.session.set_expiry(0)
            request.session.modified = True
          if nextUrl is None:
            return redirect("welcome")
          else:
            return redirect(nextUrl)
      else:
        messages.error(request,  "Invalid username or password", extra_tags="Error!")
        return render(request, "login.html",{'form':form})
   
   else:
    form = LoginUserForm()
    return render(request, "login.html",{'form':form})

def register(request):
   if request.method == "POST":
      form = NewUserForm(request.POST)
      if form.is_valid():
        form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(username=username, password=password)
        auth_login(request,user)
        return redirect("welcome")
      else:
        return render(request, "register.html", {'form':form})
   else:
    form = NewUserForm()
    return render(request, "register.html", {'form':form})

@login_required(login_url="login")
def change_password(request):
  if request.method == "POST":
    form = UserPasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)
      messages.success(request,  "Your password has been successfully changed", extra_tags="Success!")
      return redirect("welcome")
    else:
      return render(request, "change_password.html", {'form':form})
  else:
    form = UserPasswordChangeForm(request.user)
    return render(request, "change_password.html", {'form':form})

def logout(request):
   auth_logout(request)
   return redirect("login")

@login_required(login_url="login")
def welcome(request):
   return render(request, "welcome.html")