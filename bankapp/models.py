from django.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _


class BankAccountDetails(models.Model):
    """Model definition for users Bank Account Details."""
    NGN = "NGN"
    CURRENCY_CODE = (
        (NGN, 'Naira'),
    )

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ACCOUNT_STATUS = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "account_details"), on_delete=models.CASCADE)
    name = models.CharField(_("Full Name"), max_length=250)

    bank_name = models.CharField(_("Bank Name"), max_length=30)
    bank_slug = models.SlugField(_("Bank Slug"), max_length=30)
    bank_code = models.CharField(_("Bank Code"), max_length=3)
    account_number = models.CharField(_("Account Number"), max_length=10)
    account_balance = models.CharField(
        _("Account Balance"), default="0", max_length=10)
    customer_code = models.CharField(_("Customer Code"), max_length=40)
    customer_id = models.CharField(_("Customer ID"), max_length=10)
    # BVN = models.CharField(_("Bank Verification Number"),
      #                     max_length=11, blank=True)
    currency_code = models.CharField(
        _("Currency Code"), choices=CURRENCY_CODE, default=NGN, max_length=3)
    #reservation_reference = models.CharField(
     #   _("Reservation Reference"), max_length=40)
    #account_reference = models.CharField(_("Account Reference"), max_length=20)
    status = models.CharField(
        _("Account Status"), choices=ACCOUNT_STATUS, max_length=15)
    created_on = models.DateTimeField(_("Account Created on"))

    class Meta:
        """Meta definition for BankAccount."""

        verbose_name = 'Bank Account Detail'
        verbose_name_plural = 'Bank Account Details'

    def __str__(self):
        """Unicode representation of BankAccount."""
        return f"{self.user.get_full_name()} Bank Account Details"
