from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PurchaseMatch(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    is_paid = models.BooleanField(_('is paid'), default=False)
    match = models.ForeignKey('stadiums.Match', verbose_name=_('match'), on_delete=models.CASCADE, related_name='purchases')
    seat = models.ForeignKey('stadiums.Seat', verbose_name=_('seat'), on_delete=models.CASCADE, related_name='purchases')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE, related_name='purchases')

    class Meta:
        verbose_name = _("Purchase")
        verbose_name_plural = _("Purchases")


    def __str__(self):
        return f"user_id: {self.user_id}, seat: {self.seat_id}"
