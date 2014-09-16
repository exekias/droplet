from django.utils.translation import ugettext as _
from nazs.web import tables, blocks

from .models import Module, Conf

register = blocks.Library('apache')


def enable(transport, table, item):
    item.enabled = True
    item.save()


def disable(transport, table, item):
    item.enabled = False
    item.system = False
    item.save()


@register.block('modules')
class Modules(tables.Table):

    model = Module

    name = tables.Column(verbose_name=_('Name'))

    status = tables.MergeColumn(
        verbose_name=_('Status'),
        columns=(
            ('enable',
             tables.ActionColumn(verbose_name=_('Enable'),
                                 action=enable,
                                 classes='btn btn-success',
                                 visible=lambda m: not m.enabled)),

            ('disable',
             tables.ActionColumn(verbose_name=_('Disable'),
                                 action=disable,
                                 classes='btn btn-info',
                                 visible=lambda m: m.enabled)),
        )
    )


@register.block('confs')
class Confs(tables.Table):

    model = Conf

    name = tables.Column(verbose_name=_('Name'))

    status = tables.MergeColumn(
        verbose_name=_('Status'),
        columns=(
            ('enable',
             tables.ActionColumn(verbose_name=_('Enable'),
                                 action=enable,
                                 classes='btn btn-success',
                                 visible=lambda m: not m.enabled)),

            ('disable',
             tables.ActionColumn(verbose_name=_('Disable'),
                                 action=disable,
                                 classes='btn btn-info',
                                 visible=lambda m: m.enabled)),
        )
    )
