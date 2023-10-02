from django import forms
from .models import myuser


class UserForm(forms.ModelForm):
    class Meta:
        model = myuser
        fields = ['username', 'password', 'firstname', 'lastname', 'date_of_birth', 'email']


from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")
    date_of_birth = forms.DateField()

    class Meta:
        model = User
        fields = ['username',  'password1', 'password2','first_name', 'last_name', 'date_of_birth', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ResetPasswordForm(forms.Form):
    current_password = forms.CharField(label='รหัสผ่านปัจจุบัน', widget=forms.PasswordInput)
    new_password = forms.CharField(label='รหัสผ่านใหม่', widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(label='ยืนยันรหัสผ่านใหม่', widget=forms.PasswordInput)