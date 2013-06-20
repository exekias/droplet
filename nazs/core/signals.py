import django.dispatch

# Module enable signals
pre_enable = django.dispatch.Signal()
post_enable = django.dispatch.Signal()

# Module disable signals
pre_disable = django.dispatch.Signal()
post_disable = django.dispatch.Signal()

