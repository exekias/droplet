from django.utils.translation import ugettext as _


from nazs import models


class DomainSettings(models.SingletonModel):

    MODE_CHOICES = (
        ('ad', _('Domain controller')),
        ('member', _('Domain member')),
    )

    mode = models.CharField(choices=MODE_CHOICES, default='ad', max_length=10)
