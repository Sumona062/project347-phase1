from django import forms
from django.contrib.auth.forms import authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class ApplicantRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 charecter including numeric values',
    )
    is_applicant = forms.BooleanField(initial=True)

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2", "is_applicant")


class CompanyRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 character including numeric values',
    )
    is_company = forms.BooleanField(initial=True)

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2", "is_company")


class ApplicantEditProfileForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ApplicantProfileModel
        fields = '__all__'
        exclude = ['user']


class CompanyEditProfileForm(ModelForm):
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    logo = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CompanyProfileModel
        fields = '__all__'
        exclude = ['user']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("invalid log in credentials")
