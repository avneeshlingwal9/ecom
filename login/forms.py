from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email" , required=True)
    first_name = forms.CharField(label = "First name", required=True)
    last_name = forms.CharField(label= "Last name", required=True)

    class Meta:
        model = User
        fields = ("username", "first_name","last_name", "email", )
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists. Please use a different email")
        return email


    def save(self, commit = True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user



