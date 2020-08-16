from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice

from allauth_2fa.utils import user_has_valid_totp_device
from .utils import get_user_otp_device


class ValidTOTPDeviceRequiredMixin(AccessMixin):
    no_valid_totp_device_url = reverse_lazy('two-factor-setup')

    def dispatch(self, request, *args, **kwargs):
        device = get_user_otp_device(request.user)
        
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if device:
            if isinstance(device, TOTPDevice):
                if not user_has_valid_totp_device(request.user):
                    return self.handle_missing_totp_device()

        return super(ValidTOTPDeviceRequiredMixin, self).dispatch(request, *args, **kwargs)

    def handle_missing_totp_device(self):
        return HttpResponseRedirect(self.no_valid_totp_device_url)
