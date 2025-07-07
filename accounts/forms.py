from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    phone = forms.CharField(max_length=20, required=False, help_text='Optional. Enter your phone number.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')   
class EditProfile(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone']