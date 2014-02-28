from django.db import models
from django.utils.translation import ugettext as _

from nazs.core.models import Model
from nazs.folders.models import Folder


class Settings(Model):
    """
    Transmission Settings
    """

    # Locations
    incomplete_dir = models.ForeignKey(
        Folder,
        verbose_name=_('Incomplete downloads folder'),
        related_name='+')

    download_dir = models.ForeignKey(
        Folder,
        verbose_name=_('Completed downloads folder'),
        related_name='+')

    # Speed limits
    speed_limit_down_enabled = models.BooleanField(
        verbose_name=_('Limit download speed'),
        default=False)

    speed_limit_down = models.PositiveIntegerField(
        verbose_name=_('Download speed limit (KB/s)'),
        default=100)

    speed_limit_up_enabled = models.BooleanField(
        verbose_name=_('Limit upload speed'),
        default=True)

    speed_limit_up = models.PositiveIntegerField(
        verbose_name=_('Upload speed limit (KB/s)'),
        default=10)

    # Per torrent conf
    upload_slots_per_torrent = models.PositiveIntegerField(
        verbose_name=_('Upload slots per torrent'),
        default=14)

    # Misc
    ENCRYPTION_CHOICES = (
        (0, _('Prefer unencrypted connections')),
        (1, _('Prefer encrypted connections')),
        (2, _('Require encrypted connections'))
    )
    encryption = models.IntegerField(verbose_name=_('Encryption mode'),
                                     choices=ENCRYPTION_CHOICES,
                                     default=1)

    download_queue_size = models.PositiveIntegerField(
        verbose_name=_('Download queue size'),
        default=5)

    @classmethod
    def get_or_create(cls):
        try:
            return cls.objects.all()[0]
        except:
            res = cls()
            res.save()
            return res
