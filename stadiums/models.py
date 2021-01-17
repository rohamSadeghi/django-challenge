from django.db import models
from django.utils.translation import ugettext_lazy as _


class Stadium(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    is_enable = models.BooleanField(_('is enable'), default=True)
    name = models.CharField(_('name'), max_length=80)
    address = models.TextField(_('address'))
    phone_number = models.BigIntegerField(_('phone number'), blank=True, null=True)

    class Meta:
        verbose_name = _("Stadium")
        verbose_name_plural = _("Stadiums")

    def __str__(self):
        return self.name


class Seat(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    is_enable = models.BooleanField(_('is enable'), default=True)
    stadium = models.ForeignKey('Stadium', verbose_name=_('stadium'), on_delete=models.CASCADE, related_name='seats')
    price = models.PositiveIntegerField(_('price'))
    price_discount = models.PositiveIntegerField(_('price discount'), default=0)
    position = models.PositiveSmallIntegerField(_('position'))
    row_number = models.PositiveSmallIntegerField(_('row number'))
    seat_number = models.PositiveSmallIntegerField(_('seat number'))
    is_available = models.BooleanField(_('is available'), default=True)

    class Meta:
        verbose_name = _("Seat")
        verbose_name_plural = _("Seats")

    def __str__(self):
        return f"{self.stadium}->{self.seat_number}"


class Match(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    is_enable = models.BooleanField(_('is enable'), default=True)
    title = models.CharField(_('title'), max_length=80)
    execute_time = models.DateTimeField(_('execute date'))
    stadium = models.ForeignKey('Stadium', verbose_name=_('stadium'), on_delete=models.CASCADE, related_name='matches')

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")

    def __str__(self):
        return self.title
