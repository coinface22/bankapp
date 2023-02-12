from django import forms
from django.contrib.auth import authenticate
from .models import Account, User
from django.conf import settings

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self,request,*args,**kwargs):
        self.request = request
        self.user  = None
        super().__init__(*args,**kwargs)
    
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        self.user = authenticate(self.request,email = email, password = password)

        if not self.user:
            raise forms.ValidationError("Incorrect Credentials")

        return self.cleaned_data
    
    def get_user(self):
        return self.user

class AccountAddForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField()
    class Meta:
        model = Account
        exclude = ['user','date_created','account_number']
    def clean(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Email already exists")
        
        return super().clean()

class AccountEditForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False)
    class Meta:
        model = Account
        exclude = ['user','date_created','account_number']
    def clean(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Email already exists")
        
        return super().clean()