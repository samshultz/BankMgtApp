from django.shortcuts import render
from allauth.account.forms import ChangePasswordForm

# Create your views here.
def profile(request):
    return render(request, "account/profile.html", {"form": ChangePasswordForm})