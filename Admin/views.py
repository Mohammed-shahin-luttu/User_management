from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


# Create your views here.
# admin-panel

@never_cache
@login_required(login_url='login')
def my_admin(request):
    """
        This code shows a web page called "login" when you visit the my_admin link.
        If an admin is logged in, it shows myadmin.html and prints the search box text.
        If there's search text, find matching usernames or emails; otherwise, get all users.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        search = request.GET.get('search', '')
        if search:
            users = User.objects.filter(
                Q(username__icontains=search) | Q(email__icontains=search)
            )
        else:                
            users = User.objects.all()
        return render(request, 'myadmin.html', {'users': users})
    return redirect('login')

# ------------------------------------------------------------------------------------------
# adduser
"""
The add_user function renders the adduser.html template when the user visits the page.
This code checks the form submission, gets username, email, and password, then creates a new user.
This code checks if the email already exists in the database and shows an error message.
This code checks if the password meets criteria: length, uppercase, lowercase, digits, and special characters.
This code checks if the username already exists and shows an error if it does.
"""
@never_cache
def add_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            username =request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(username,email,password)
#------------------------username Validation--------------------------------------------------
            if User.objects.filter(username=username).exists():
                error = 'This username already exist'
                return render(request,'adduser.html',{'usererror':error})
#-------------------------email--------------------------------------------------------------
            if User.objects.filter(email=email).exists():
                error = 'this email already exists'
                return render(request,'adduser.html',{'emailerror':error})
#------------------------password-------------------------------------------------------------          
            if not password:
                error = 'Your password is mandatory'
                return render(request, 'adduser.html', {'passerror': error})
            elif len(password) < 8:
                error = 'Password must be at least 8 characters long.'
                return render(request, 'adduser.html', {'passerror': error})
            elif not any(char.isupper() for char in password):
                error = 'Password must contain at least one uppercase letter.'
                return render(request, 'adduser.html', {'passerror': error})
            elif not any(char.islower() for char in password):
                error = 'Password must contain at least one lowercase letter.'
                return render(request, 'adduser.html', {'passerror': error})
            elif not any(char.isdigit() for char in password):
                error = 'Password must contain at least one digit.'
                return render(request, 'adduser.html', {'passerror': error})
            elif not any(char in "!@#$%^&*()_" for char in password):
                error = 'Password must contain at least one special character.'
                return render(request, 'adduser.html', {'passerror': error})
#-----------------------creating the user------------------------------------------------------
            User.objects.create_user(username=username,email=email,password=password)
            return redirect('myadmin')
        
    return render(request,('adduser.html'))
# ---------------------------------------------------------------------------------------------
# edit 
"""
This code renders the edituser.html template with user data passed as context.
This code checks if the user is authenticated and a superuser, then fetches the user
This code processes a POST request, gets data from a form, and redirects to 'myadmin'.
This code checks if the username or email already exists, 
excluding the current user's ID, and displays an error if found.
This code updates the users username and email, and changes the password if provided.
"""
@never_cache
def edit_user(request,user_id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = get_object_or_404(User,id=user_id)
        if request.method == 'POST':
            error = ''
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                error = ' username already  exists'
                return render(request,'edituser.html',{'usererror':error})
            elif User.objects.filter(email=email).exclude(id=user_id).exists():
                error = 'Email already exists'
                return render(request,'edituser.html',{'mailerror':error})            
            if not error:
                user.username=username
                user.email=email
                if password:
                    user.set_password = password
                user.save()
            return redirect('myadmin')
    return render(request,'edituser.html',{'user':user})

# --------------------------------------------------------------------------------------------------
# delect
@never_cache
def delete_user(request,user_id):
    '''

    '''
    
    if request.user.is_superuser and request.user.is_authenticated:
        user = get_object_or_404(User, id = user_id)
        user.delete()
        messages.success(request,'User has been deleted successfully')
        return redirect('myadmin')
    return render(request,('myadmin.html'))