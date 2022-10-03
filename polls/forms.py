from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import modelformset_factory
from .models import Profile, Contact
import datetime

class RegisterForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=100,
                                 required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']




class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    birth_place = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(required=False,initial=datetime.date.today)
    residency = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']



class ContactForm(forms.ModelForm):

    first_name = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    info = forms.CharField(required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone', 'email', 'avatar', 'info']

ContactModelFormset = modelformset_factory(
    Contact,
    fields=('first_name', 'last_name', 'phone'),
    extra=1,
    max_num=3,
    widgets={'first_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'required': True}),
            'last_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'})
            })
    
