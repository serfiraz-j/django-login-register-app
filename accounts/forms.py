from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.forms import widgets
from django.contrib.auth.models import User

class LoginUserForm(AuthenticationForm): 
    remember_me = forms.BooleanField(required=False,initial=False, widget=forms.CheckboxInput(attrs={'class':"custom-control-input"}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(attrs={'class':"form-control",'placeholder': "Username"})
        self.fields["password"].widget = widgets.PasswordInput(attrs={'class':"form-control",'placeholder': "Password"})
    
class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","email",)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = widgets.PasswordInput(attrs={'class':"form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(attrs={'class':"form-control"})
        self.fields['username'].widget = widgets.TextInput(attrs={'class':"form-control"})
        self.fields['email'].widget = widgets.EmailInput(attrs={'class':"form-control"})
        self.fields['email'].required = True
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email = email).exists():
            self.add_error("email","This email is already taken.")
        return email
    
class UserPasswordChangeForm(PasswordChangeForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = widgets.PasswordInput(attrs={'class':"form-control"})
        self.fields["new_password1"].widget = widgets.PasswordInput(attrs={'class':"form-control"})
        self.fields["new_password2"].widget = widgets.PasswordInput(attrs={'class':"form-control"})