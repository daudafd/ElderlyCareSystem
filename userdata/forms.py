from django import forms
from .models import Client
from django.contrib.auth.models import User

class ClientRegistrationForm(forms.ModelForm):
    assigned_user = forms.ModelChoiceField(queryset=User.objects.all(), 
                                           empty_label="Select User", required=False)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'gender', 'marital_status', 
                  'dob', 'phone', 'email', 'address', 'weight', 'height', 'assigned_user']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data