from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'username'}))  
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'confirm password'}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email
    
    def clean_username(self):
        q = self.cleaned_data['username']
        user = User.objects.filter(username=q).exists()
        if user:
            raise ValidationError('This username is taken')
        return q
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        
        if p1 and p2 and p1 != p2:
            raise ValidationError('passwords must match')
                
    
    
class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'password'}))
    


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = Profile
        fields = ('age', 'bio')