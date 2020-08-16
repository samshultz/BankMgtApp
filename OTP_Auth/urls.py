from django.urls import path, re_path
from .views import TwoFactorEmailSetup, twoFAHome, TwoFactorAuthenticate, TwoFactorBackupTokens



urlpatterns = [
    re_path("^two-factor-authenticate/two_factor/email/", TwoFactorEmailSetup.as_view(), name="email_two_factor"),
    path("two_factor/", twoFAHome, name="two_fa_home"),
    
    re_path("^two-factor-authenticate/", TwoFactorAuthenticate.as_view(), name="two-factor-authenticate-email")
]