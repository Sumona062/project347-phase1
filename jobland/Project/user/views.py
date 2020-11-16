from django.shortcuts import render, redirect
from .decorators import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .models import *


@unauthenticated_user
def home(request):
    applicants = User.objects.filter(is_applicant=True)
    companies = User.objects.filter(is_company=True)

    context = {
        'applicants': applicants,
        'applicants_len': applicants.count(),
        'companies': companies,
        'companies_len': companies.count(),
    }

    return render(request, 'user/index.html', context)


@unauthenticated_user
def login_page(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user and user.is_applicant:
                login(request, user)
                return redirect('applicant-feed')
            elif user and user.is_company:
                login(request, user)
                return redirect('company-profile', user.id)
            else:
                messages.error(request, 'Username or Password is incorrect.')
        # else:
        #     return render(request, 'user/login.html', {'form': form})
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def applicant_register(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            ApplicantProfileModel.objects.create(user=user)
            messages.success(request, "Account created successfully.")
            return redirect('applicant-feed')

    form = ApplicantRegistrationForm()
    context = {
        "form": form
    }
    return render(request, 'user/applicant/applicant-register.html', context)


@unauthenticated_user
def company_register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            CompanyProfileModel.objects.create(user=user)
            messages.success(request, "Account created successfully.")
            return redirect('company-profile', user.id)

    form = CompanyRegistrationForm()
    context = {
        "form": form
    }
    return render(request, 'user/company/company-register.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_feed(request):
    applicants = User.objects.filter(is_applicant=True)
    companies = User.objects.filter(is_company=True)

    context = {
        'applicants': applicants,
        'applicants_len': applicants.count(),
        'companies': companies,
        'companies_len': companies.count(),
    }
    return render(request, 'user/applicant/applicant-feed.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_profile(request, pk):
    user = User.objects.get(id=pk)

    context = {
        'user': user,
    }
    return render(request, 'user/applicant/applicant-profile.html', context)


    user = User.objects.get(id=pk)

    context = {
        'user': user,
    }
    return render(request, 'user/applicant/applicant-public-profile.html', context)


@login_required(login_url='login')
def company_profile(request, pk):
    applicants = User.objects.filter(is_applicant=True)
    companies = User.objects.filter(is_company=True)
    user = User.objects.get(id=pk)
    context = {
        'user': user,
        'applicants': applicants,
        'applicants_len': applicants.count(),
        'companies': companies,
        'companies_len': companies.count(),
    }
    return render(request, 'user/company/company-profile.html', context)


@login_required(login_url='login')
@show_to_applicant(allowed_roles=['admin', 'is_applicant'])
def applicant_edit_profile(request):
    applicant = request.user.applicantprofilemodel
    form = ApplicantEditProfileForm(instance=applicant)
    if request.method == 'POST':
        form = ApplicantEditProfileForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            return redirect('applicant-profile', request.user.id)
        else:
            messages.error(request, 'There are a few problems')
            return redirect('applicant-edit-profile')

    context = {
        'form': form,
    }
    return render(request, 'user/applicant/applicant-edit-profile.html', context)


@login_required(login_url='login')
@show_to_company(allowed_roles=['admin', 'is_company'])
def company_edit_profile(request):
    company = request.user.companyprofilemodel
    form = CompanyEditProfileForm(instance=company)
    if request.method == 'POST':
        form = CompanyEditProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company-profile', request.user.id)
        else:
            messages.error(request, 'There are a few problems')
            return redirect('company-edit-profile')

    context = {
        'form': form,
    }
    return render(request, 'user/company/company-edit-profile.html', context)


def about(request):
    applicants = User.objects.filter(is_applicant=True)
    companies = User.objects.filter(is_company=True)
    context = {
        'applicants': applicants,
        'applicants_len': applicants.count(),
        'companies': companies,
        'companies_len': companies.count(),
    }
    return render(request, 'user/about.html', context)


def contact(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email_add = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        send_mail(
            
            subject +"  from " + email_add  ,  
            message, 
            email_add,        
            
            ['officialjobland777@gmail.com' , ], 
             #the mail adddress that the email will be sent to
        )

        return render(request, 'user/contact.html', {'frist_name': fname})
    else:
        return render(request, 'user/contact.html', {})