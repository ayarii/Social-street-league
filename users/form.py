
from sre_parse import Verbose
from tabnanny import verbose
from tkinter.ttk import Style
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.',widget=forms.EmailInput(attrs={'style': 'width: 100%; padding: 0 5px; height: 40px;font-size: 16px;border: none;background: none;outline: none;'}))
    password1 = forms.CharField(label="Password" , widget=forms.PasswordInput(attrs={'style': 'width: 100%; padding: 0 5px; height: 40px;font-size: 16px;border: none;background: none;outline: none;','id':'id_password'}))
    password2 = forms.CharField(label="Password Confirmation" , widget=forms.PasswordInput(attrs={'style': 'width: 100%; padding: 0 5px; height: 40px;font-size: 16px;border: none;background: none;outline: none;','id':'id_password2'}))
    username = forms.CharField( widget=forms.TextInput(attrs={'style': 'width: 100%; padding: 0 5px; height: 40px;font-size: 16px;border: none;background: none;outline: none;'}))
    class Meta:
         model=User
         fields = ('email', 'username', 'password1', 'password2')
         
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)
          
          
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)    
    


class AccountAuthenticationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email':forms.EmailInput(attrs={'style': 'width: 100%; padding: 0 5px; height: 40px;font-size: 16px;border: none;background: none;outline: none;'}),
            'password': forms.PasswordInput(attrs={'style': 'width: 100%; padding: 0 5px; height: 40px;font-size: 16px;border: none;background: none;outline: none;','id':'id_password'}),
        }
        
	#password = forms.CharField(label='Password', widget=forms.PasswordInput)        
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_image','birth_date','prefer_activity','user_disponibility')
        widgets = {
             'email':forms.EmailInput(attrs={'class':'form-control','id':"inputEmail4",'placeholder':'Email'}),
             'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
             'birth_date':forms.DateInput(attrs={'class': 'form-control ','type': 'date' }),
             'lat':forms.TextInput(attrs={'class':'form-control'}),
             'long': forms.TextInput(attrs={'class':'form-control'}),
             'prefer_activity' : forms.CheckboxSelectMultiple(attrs={'class':'checkbox-inline'}),
             'user_disponibility':forms.CheckboxSelectMultiple(attrs={'class':'checkbox-inline'}),
         }
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        # account.profile_image = self.cleaned_data['profile_image']
        activity = self.cleaned_data['prefer_activity']
        account.prefer_activity.set(activity)
        account.birth_date = self.cleaned_data['birth_date']
        disponibility = self.cleaned_data['user_disponibility']
        account.user_disponibility.set(disponibility)
        #account.address = self.cleaned_data['address']
        if commit:
            account.save()
        return account

class ImageUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('profile_image',)
        widgets = {
             'profile_image': forms.FileInput(attrs={'class':'image','id':'upload_image','name':'image','style':'display: none;'})
         }