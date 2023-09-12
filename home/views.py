from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from home.models import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def home(request):
    if request.method == "GET":
       return render (request, "home.html")
    elif request.method == "POST":
       file = request.FILES["my_file"]
       file_name = file.__getattribute__('name')

       img = Image.open(file)
       path = os.path.join(f'{settings.BASE_DIR}\\home\\media', file_name)
       img = img.save(path)


       print(file)

       return render (request, "home.html")
    
    
    

    


def signin (request):
   if request.user.is_authenticated:
       return redirect('home')
   if request.method == "GET":
      return render (request,"login.html")
   else:
      username = request.POST.get('username')
      password = request.POST.get('password1')

      user = authenticate(username=username, password=password)
      if user:
       login_django(request, user)
       return redirect ('home')
         
      #    return redirect ('home')
   return render (request, "login.html")
    

@login_required(login_url="login")
def galeria (request):
    if request.method == "GET":
       path = "/home/media"
       files = os.listdir(f'{settings.BASE_DIR}\\home\\media')
       images = [{"name":image, "url":f'{path}/{image}'}for image in files]
       print(images)
       return render(request, "galeria.html", {"images": images})
    



def register(request):
    if request.user.is_authenticated:
       return redirect('home')
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
          username = form.cleaned_data.get("username")
          password = form.cleaned_data.get("password1")
          email = form.cleaned_data.get("email")
          if User.objects.filter(email=email).exists():
             print ("exists")
             return
         #  user = User(username=username, password=password, email=email)
         #  login_django(request, user)
          user2 = User.objects.create_user(username=username, password=password, email=email)
          user2.save()
          return redirect ('login') 
       else:
          return render(request, 'register.html') 
    else:
      form = UserCreationForm()
      return render(request, 'register.html')
     



def index (request):
   return render (request, "index.html")




def sair(request):
   logout(request)
   return redirect('login')




    
    
 