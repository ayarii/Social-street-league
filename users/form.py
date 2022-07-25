
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import User


class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    class Meta:
         model=User
         fields = ['email', 'username', 'password1', 'password2','age','disponibility','address','prefer_activity' ]
         widgets = {
             'email':forms.EmailInput(attrs={'class':'form-control'}),
             'username': forms.TextInput(attrs={'class':'form-control'}),
             'password1': forms.PasswordInput(attrs={'class':'form-control'}),
             'password2': forms.PasswordInput(attrs={'class':'form-control'}),
             'age': forms.NumberInput(attrs={'class':'form-control'}),
             'disponibility': forms.TextInput(attrs={'class':'form-control'}),
             'address':forms.TextInput(attrs={'class':'form-control'}),
             'prefer_activity' : forms.SelectMultiple(),
         }
         
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
            'password': forms.PasswordInput(attrs={'style': 'width: 100%; padding: 0 5px; height: 40px;font-size: 16px;border: none;background: none;outline: none;'}),
        }
        
	#password = forms.CharField(label='Password', widget=forms.PasswordInput)        
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


# class AccountUpdateForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'profile_image', 'hide_email' )

#     def clean_email(self):
#         email = self.cleaned_data['email'].lower()
#         try:
#             account = User.objects.exclude(pk=self.instance.pk).get(email=email)
#         except User.DoesNotExist:
#             return email
#         raise forms.ValidationError('Email "%s" is already in use.' % account)

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             account = User.objects.exclude(pk=self.instance.pk).get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError('Username "%s" is already in use.' % username)


#     def save(self, commit=True):
#         account = super(AccountUpdateForm, self).save(commit=False)
#         account.username = self.cleaned_data['username']
#         account.email = self.cleaned_data['email'].lower()
#         account.profile_image = self.cleaned_data['profile_image']
#         #account.hide_email = self.cleaned_data['hide_email']
#         if commit:
#             account.save()
#         return account