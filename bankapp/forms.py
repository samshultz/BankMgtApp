from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=250, label='Last Name')
    middle_name = forms.CharField(max_length=250, label='Middle Name', required=False)
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if middle_name:
            user.last_name +=  " " + self.cleaned_data['middle_name']
            
        user.save()
        return user