from django.shortcuts import render
from allauth.account.forms import ChangePasswordForm, AddEmailForm
from allauth.account.views import PasswordChangeView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

@login_required
def profile(request):
    return render(request, "account/profile.html", {"form": ChangePasswordForm, "email_form": AddEmailForm})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("profile")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "bankapp/dashboard.html"
