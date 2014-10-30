from droplet.models import Model
from droplet.network.util import getifaddrs

from django.db import models
from django.utils.translation import ugettext as _


class Interface(Model):
    """
    Network Interfaces, both physical and virtual
    """

    # Only manage system interfaces matching this filter
    NAME_FILTER = ('eth', 'wlan')

    ETHERNET = 'ethernet'

    TYPE_CHOICES = (
        (ETHERNET, _('Ethernet')),
    )

    UNCONFIGURED = 'notset'
    STATIC = 'static'
    DHCP = 'dhcp'

    MODE_CHOICES = (
        (UNCONFIGURED, _('Unconfigured')),
        (STATIC, _('Static')),
        (DHCP, _('DHCP')),
    )

    # Interface name (eth0, eth0:1 br0, etc..)
    name = models.CharField(max_length=10, editable=False)

    # Type (ethernet, vlan, bridge...)
    type = models.CharField(choices=TYPE_CHOICES,
                            max_length=10,
                            default=ETHERNET)

    # Mode (dhcp, static, bridged...)
    mode = models.CharField(choices=MODE_CHOICES,
                            max_length=10,
                            default=UNCONFIGURED)

    # IP Address (Ignored in DHCP)
    address = models.GenericIPAddressField(protocol='IPv4',
                                           null=True,
                                           blank=True)

    # Netmask (Ignored in DHCP)
    netmask = models.GenericIPAddressField(protocol='IPv4',
                                           null=True,
                                           blank=True)

    @classmethod
    def update(cls):
        """
        Update rows to include known network interfaces
        """
        ifaddrs = getifaddrs()
        # Create new interfaces
        for ifname in ifaddrs.keys():
            if filter(ifname.startswith, cls.NAME_FILTER):
                cls.objects.get_or_create(name=ifname)

        # Delete no longer existing ones
        cls.objects.exclude(name__in=ifaddrs.keys()).delete()

    @property
    def configured(self):
        """
        Return True if this interface is configured
        """
        return self.mode != Interface.UNCONFIGURED

    def __unicode__(self):
        return self.name
