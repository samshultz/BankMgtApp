from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from allauth.account import signals
from allauth.account.adapter import get_adapter
from allauth.account.utils import get_login_redirect_url
from .mixins import ValidTOTPDeviceRequiredMixin

from django.contrib import messages
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.plugins.otp_static.models import StaticToken

from allauth_2fa import app_settings
from allauth_2fa.forms import TOTPAuthenticateForm
from django.contrib.auth import get_user_model

from .forms import EmailDeviceForm
from .utils import user_has_valid_totp_device, get_user_otp_device


def twoFAHome(request):
    return render(request, "OTP_Auth/two_fa_index.html", {})


class TwoFactorAuthenticate(FormView):
    template_name = 'allauth_2fa/authenticate.' + app_settings.TEMPLATE_EXTENSION
    form_class = TOTPAuthenticateForm

    def _new_device(self):
        """
        Replace any unconfirmed TOTPDevices with a new one for confirmation.
        This needs to be done whenever a GET request to the page is received OR
        if the confirmation of the device fails.
        """
        # devices = devices_for_user(self.request.user, confirmed=True)
        user_id = self.request.session['allauth_2fa_user_id']
        user = get_user_model().objects.get(id=user_id)
        
        # device = user_has_valid_totp_device(user)
        device = get_user_otp_device(user)
        if not device:
            user.emaildevice_set.filter(confirmed=False).delete()
            device = user.emaildevice_set.create(confirmed=False)
            device.generate_challenge()
        else:
            device.generate_challenge()

    def dispatch(self, request, *args, **kwargs):
        # If the user is not about to enter their two-factor credentials,
        # redirect to the login page (they shouldn't be here!). This includes
        # anonymous users.
        # self._new_device()
        print(request.session.get("allauth_2fa_user_id"))
        if 'allauth_2fa_user_id' not in request.session:
            # Don't use the redirect_to_login here since we don't actually want
            # to include the next parameter.
            return redirect('account_login')
        return super(TwoFactorAuthenticate, self).dispatch(request, *args,
                                            **kwargs)

    
    def get(self, request, *args, **kwargs):
        self._new_device()

        return super(TwoFactorAuthenticate, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TwoFactorAuthenticate, self).get_form_kwargs()
        user_id = self.request.session['allauth_2fa_user_id']
        kwargs['user'] = get_user_model().objects.get(id=user_id)
        return kwargs

    def form_valid(self, form):
        print("="*15)
        """
        The allauth 2fa login flow is now done (the user logged in successfully
        with 2FA), continue the logic from allauth.account.utils.perform_login
        since it was interrupted earlier.
        """
        adapter = get_adapter(self.request)

        # Skip over the (already done) 2fa login flow and continue the original
        # allauth login flow.
        super(adapter.__class__, adapter).login(self.request, form.user)

        # Perform the rest of allauth.account.utils.perform_login, this is
        # copied from commit cedad9f156a8c78bfbe43a0b3a723c1a0b840dbd.

        # TODO Support redirect_url.
        response = HttpResponseRedirect(
            get_login_redirect_url(self.request))

        # TODO Support signal_kwargs.
        signals.user_logged_in.send(sender=form.user.__class__,
                                    request=self.request,
                                    response=response,
                                    user=form.user)

        adapter.add_message(
            self.request,
            messages.SUCCESS,
            'account/messages/logged_in.txt',
            {'user': form.user})

        return response


class TwoFactorEmailSetup(LoginRequiredMixin, FormView):
    template_name = 'OTP_Auth/emailOTP.' + app_settings.TEMPLATE_EXTENSION
    form_class = EmailDeviceForm
    success_url = reverse_lazy('two-factor-backup-tokens')

    def dispatch(self, request, *args, **kwargs):
        # If the user has 2FA setup already, redirect them to the backup tokens.
        print("="*12)
        print(user_has_valid_totp_device(request.user))
        print("="*12)
        if user_has_valid_totp_device(request.user):
            return HttpResponseRedirect(reverse('two-factor-backup-tokens'))

        return super(TwoFactorEmailSetup, self).dispatch(request, *args, **kwargs)

    def _new_device(self):
        """
        Replace any unconfirmed TOTPDevices with a new one for confirmation.
        This needs to be done whenever a GET request to the page is received OR
        if the confirmation of the device fails.
        """
        # devices = devices_for_user(self.request.user, confirmed=True)
    
        user = self.request.user
        # device = user_has_valid_totp_device(user)
        device = get_user_otp_device(user)
        if not device:
            # self.request.user.emaildevice_set.filter(confirmed=False).delete()
            # self.device = EmailDevice.objects.create(user=self.request.user, confirmed=False)
            self.request.user.emaildevice_set.filter(confirmed=False).delete()
            device = user.emaildevice_set.create(confirmed=False)
            # print(device.generate_token(valid_secs=360))
            print(device.generate_challenge())
            print(device.token)


    def get(self, request, *args, **kwargs):
        # Whenever this page is loaded, create a new device (this ensures a
        # user's QR code isn't shown multiple times).
        self._new_device()
        return super(TwoFactorEmailSetup, self).get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(TwoFactorSetup, self).get_context_data(**kwargs)
    #     context['qr_code_url'] = self.get_qr_code_data_uri()
    #     return context

    def get_form_kwargs(self):
        kwargs = super(TwoFactorEmailSetup, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Confirm the device.
        form.save()
        return super(TwoFactorEmailSetup, self).form_valid(form)

    def form_invalid(self, form):
        # If the confirmation code was wrong, generate a new device.
        self._new_device()
        return super(TwoFactorEmailSetup, self).form_invalid(form)


class TwoFactorBackupTokens(ValidTOTPDeviceRequiredMixin, TemplateView):
    template_name = 'allauth_2fa/backup_tokens.' + app_settings.TEMPLATE_EXTENSION
    # This can be overridden in a subclass to True,
    # to have that particular view always reveal the tokens.
    reveal_tokens = bool(app_settings.ALWAYS_REVEAL_BACKUP_TOKENS)

    def get_context_data(self, **kwargs):
        context = super(TwoFactorBackupTokens, self).get_context_data(**kwargs)
        static_device, _ = self.request.user.staticdevice_set.get_or_create(
            name='backup'
        )

        if static_device:
            context['backup_tokens'] = static_device.token_set.all()
            context['reveal_tokens'] = self.reveal_tokens

        return context

    def post(self, request, *args, **kwargs):
        static_device, _ = request.user.staticdevice_set.get_or_create(
            name='backup'
        )
        static_device.token_set.all().delete()
        for _ in range(3):
            static_device.token_set.create(token=StaticToken.random_token())
        self.reveal_tokens = True
        return self.get(request, *args, **kwargs)

