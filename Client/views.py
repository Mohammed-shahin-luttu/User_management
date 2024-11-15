from django.shortcuts import render,redirect,HttpResponse 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache 

# Create your views here.
# ----------------------------------------------------------------------------------
# Login User
"""
Redirects to home page if the user is already logged in.
If POST request, get credentials, authenticate user, and render login page.
If user is authenticated, login and show home page, else show error.
"""
@never_cache
def Loginpage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('myadmin')  
        else:
            return render(request, 'home.html') 
    
    
    error=''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)


        if user:
            login(request,user)
            if user.is_superuser:
                return redirect('myadmin')  
            else:
                return render(request, 'home.html')
        

        else:
            error = 'Incorrect Username or Password'


    return render(request,'login.html',{'message':error})
# --------------------------------------------------------------------------------
# Home page
"""
Prevent caching of the page and require login before accessing the page.
Renders the 'home.html' page when the HomePage function is called
Check if the user is logged in, then show the home page.
"""
@never_cache
@login_required(login_url="login")
def HomePage(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    return render(request, 'home.html')

# ----------------------------------------------------------------------------------
# Logout 
"""
Renders the 'login.html' page when the Logout function is called.
Logs out the user and redirects to the signup page if authenticated.
"""
def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('signup')
    return render(request,'login.html')
# ----------------------------------------------------------------------------------
#SignUp
"""
Prevents caching of the page, ensuring it's always fresh.
Render signup page for user to enter details.
Check if form is submitted, get username, email, and passwords.
Check if passwords match; if not, show an error message. Else, create user.
"""
@never_cache
def SignUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return HttpResponse("your password and conform password are not same!!!")
        else:
            my_user = User.objects.create_user(username,email,password1)
            my_user.save()
            return redirect('login')
    return render(request,'signup.html')

def Shahin(request):
    return render(request,'shahin.html')