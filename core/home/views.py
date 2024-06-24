from django.shortcuts import render,redirect
from django.http import HttpResponse ##used for direct returning the html tags.
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from home.models import *
from django.contrib import messages
from django.db import IntegrityError

def home(request):
    return render(request, "home.html")

def freeTrial(request):
    return render(request, 'home.html')

def joinCreateOrganisation(request):
    return render(request, 'home.html')  # Assuming this is your join/create organisation template


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')


        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'login.html')

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to some 'home' page or dashboard
        else:
            try:
                user = Users.objects.get(email_id=email)
                messages.error(request, "Invalid email or password.")
            except Users.DoesNotExist:
                try:
                    default_company_name = "DefaultCompany"  # Replace with actual logic or default value
                    company, created = Company.objects.get_or_create(company_name=default_company_name)
                    user = Users(
                        email_id=email,
                        user_first_name='DefaultFirstName',  # Replace with actual form data or defaults
                        user_last_name='DefaultLastName',    # Replace with actual form data or defaults
                        user_type='Company_loader',          # Replace with actual logic for user type
                        user_status='Active',        
                        company=company         # Default status
                    )

                    user.set_password(password)
                    user.save()
                    messages.success(request, "New account created. Please log in.")
                    return redirect('dashboard')  # Redirect to login page or wherever appropriate
                except IntegrityError:
                    messages.error(request, "There was an error creating your account. Please try again.")

    return render(request, 'login.html')  # Render the login template in case of GET request or errors


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})