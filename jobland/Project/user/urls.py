from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    # user login and logout url
    path('account/login', login_page, name='login'),
    path('account/logout', logout_user, name='logout'),

    # applicant and company registration url
    path('account/applicant-registration', applicant_register, name='applicant-register'),
    path('account/company-registration', company_register, name='company-register'),

    # applicant feed url
    path('applicant/applicant-feed', applicant_feed, name='applicant-feed'),

    # applicant profile, public profile and company profile url
    path('applicant/applicant-profile/<str:pk>/', applicant_profile, name='applicant-profile'),
    path('company/company-profile/<str:pk>/', company_profile, name='company-profile'),

    # applicant add and edit url
    path('applicant/applicant-edit-profile', applicant_edit_profile, name='applicant-edit-profile'),
    path('company/company-edit-profile', company_edit_profile, name='company-edit-profile'),



    # utilities
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
]
