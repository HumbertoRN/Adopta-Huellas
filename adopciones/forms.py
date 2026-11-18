from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Pet


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False, label="Teléfono")

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'gender', 'size',
                  'description', 'health_status']
        labels = {'age': 'Edad (en meses)'}