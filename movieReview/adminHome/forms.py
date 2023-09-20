from django import forms
from .models import myuser

class UserForm(forms.ModelForm):
    class Meta:
        model = myuser
        fields = ['username', 'password', 'firstname', 'lastname', 'date_of_birth', 'email']