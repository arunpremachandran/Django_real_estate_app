from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from contacts.models import Contact

# Create your views here.

def register(request):
    if request.method == 'POST':
        #get from values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # validation
        #check if passwords match
        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken')
                return redirect ('register')
            else:
                #check emails
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That emailid is taken')
                    return redirect('register')
                else:
                    # looks good all validation passed
                    user = User.objects.create_user(username=username, first_name=first_name,
                     last_name=last_name, password=password, email=email)
                    #login after register
                    #auth.login(request, user)
                    #messages.success(request, 'You are now logged in')
                    #return redirect('index')
                    user.save()
                    messages.success(request, 'You are now registered and can logged in')
                    return redirect('login')

        else:
            messages.error(request, 'passwords do not match')

            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        # Login user
    # getting the values
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalide Credentials')
            return  redirect('login')

    else:

        return render(request, 'accounts/login.html')

def logout(request):

    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now successfully logged out')
        return redirect('index')

def dashboard(request):

    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {

        'contacts': user_contacts

    }

    return render(request, 'accounts/dashboard.html', context)
