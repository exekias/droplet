from django.utils.translation import ugettext as _


from droplet import models


class DomainSettings(models.SingletonModel):

    MODE_CHOICES = (
        ('ad', _('Domain controller')),
        ('member', _('Domain member')),
    )

    mode = models.CharField(choices=MODE_CHOICES, default='ad', max_length=10)

    domain = models.CharField(max_length=20, default='droplet')

    workgroup = models.CharField(max_length=20, default='DROPLET')

    realm = models.CharField(max_length=20, default='DROPLET.LAN')

    netbios = models.CharField(max_length=20, default='DC')

    description = models.CharField(max_length=20, default='droplet server')

    adminpass = models.CharField(max_length=50, editable=False, default='')
