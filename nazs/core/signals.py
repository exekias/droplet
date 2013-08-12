import django.dispatch

# Module install signals
pre_install = django.dispatch.Signal()
post_install = django.dispatch.Signal()

# Module enable signals
pre_enable = django.dispatch.Signal()
post_enable = django.dispatch.Signal()

# Module disable signals
pre_disable = django.dispatch.Signal()
post_disable = django.dispatch.Signal()
