from django import forms
from .models import Client
from django.contrib.auth.models import User, Group

class ClientRegistrationForm(forms.ModelForm):
    assigned_user = forms.ModelChoiceField(queryset=User.objects.all(), 
                                           empty_label="Select User", required=False)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'gender', 'marital_status', 
                  'dob', 'phone', 'email', 'address', 'weight', 'height', 'assigned_user']
        
    # def __init__(self, *args, **kwargs):
    #     super(ClientRegistrationForm, self).__init__(*args, **kwargs)
    #     # Filter the users to exclude admin users
    #     self.fields['user'].queryset = User.objects.filter(is_staff=False)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    # def save(self, commit=True):
    #     user = super(UserRegistrationForm, self).save(commit=False)
    #     user_group = Group.objects.get(name='user')  # Replace 'user' with your group name
    #     print(f"Adding user to group: {user_group.name}")
    #     if commit:
    #         user.save()
    #         user.groups.add(user_group)
    #     return user

    # def save(self, commit=True):
    #     user = super(UserRegistrationForm, self).save(commit=False)
    #     try:
    #         user_group = Group.objects.get(name='user')  # Replace 'user' with your group name
    #         print(f"Adding user to group: {user_group.name}")
    #         if commit:
    #             user.save()
    #             user.groups.add(user_group)
    #     except Group.DoesNotExist:
    #         # Handle the case where the group doesn't exist (e.g., log an error)
    #         print(f"Group 'user' does not exist. User '{user.username}' not assigned to any group.")
    #         pass  # Or implement alternative logic
    #     return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data