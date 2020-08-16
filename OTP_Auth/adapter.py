from urllib.parse import urlencode

from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice

from allauth_2fa.adapter import OTPAdapter as AllauthOTPAdapter
from django.http import HttpResponseRedirect
from django.urls import reverse

from .utils import user_has_valid_totp_device, get_user_otp_device

user_adapter = ""

class OTPAdapter(DefaultAccountAdapter):

    def has_2fa_enabled(self, user):
        """Returns True if the user has 2FA configured."""
        
        return user_has_valid_totp_device(user)

    def login(self, request, user):
        # Require two-factor authentication if it has been configured.
        if self.has_2fa_enabled(user):
            device = get_user_otp_device(user)

            if device:
                
                if isinstance(device, EmailDevice):
                    redirect_url = reverse('two-factor-authenticate-email')
                else:
                    user_adapter = AllauthOTPAdapter
                    redirect_url = reverse('two-factor-authenticate')
            # Cast to string for the case when this is not a JSON serializable
            # object, e.g. a UUID.
            request.session['allauth_2fa_user_id'] = str(user.id)
            
            # Add GET parameters to the URL if they exist.
            if request.GET:
                redirect_url += u'?' + urlencode(request.GET)

            raise ImmediateHttpResponse(
                response=HttpResponseRedirect(redirect_url)
            )

        # Otherwise defer to the original allauth adapter.
        return super(OTPAdapter, self).login(request, user)
    

# def adapter_choice(self):
#         adapter = ""
#         user = self.request.user
#         if self.has_2fa_enabled(user):
#             device = get_user_otp_device(user)
#             if device:
                
#                 if isinstance(device, EmailDevice):
#                     adapter = OTPAdapter()
#                 else:
#                     adapter = AllauthOTPAdapter()
        
#         return adapter

adapter_choice = user_adapter or  OTPAdapter