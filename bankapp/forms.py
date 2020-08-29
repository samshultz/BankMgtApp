from allauth.account.forms import SignupForm
from django import forms
from django.forms import ValidationError

from OTP_Auth.models import Profile


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=250, label='Last Name')
    middle_name = forms.CharField(max_length=250, label='Middle Name', required=False)
    phonenumber = forms.CharField(max_length=14, label="Phone Number")
    
    def clean_phonenumber(self):
        if Profile.objects.filter(phonenumber=self.cleaned_data['phonenumber']).exists():
            raise ValidationError("Phone Number already in use")
        return self.cleaned_data['phonenumber']

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        

        Profile.objects.create(user=user, phonenumber=self.cleaned_data['phonenumber'])
        # user.profile.phonenumber = self.cleaned_data['phonenumber']

        if self.cleaned_data['middle_name']:
            user.last_name +=  " " + self.cleaned_data['middle_name']
            
        user.save()
        return user
