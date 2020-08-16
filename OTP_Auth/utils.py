from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice


def user_has_valid_totp_device(user):
    devices = devices_for_user(user, confirmed=True)
    if not user.is_authenticated:
        return False
    for device in devices:
        if isinstance(device, EmailDevice):
            return user.emaildevice_set.filter(confirmed=True).exists()
        elif isinstance(device, TOTPDevice):
            return user.totpdevice_set.filter(confirmed=True).exists()

def get_user_otp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, EmailDevice):
            return device
        elif isinstance(device, TOTPDevice):
            return device