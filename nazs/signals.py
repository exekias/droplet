from django.dispatch import Signal

# Module install signals
pre_install = Signal()
post_install = Signal()

# Module enable signals
pre_enable = Signal()
post_enable = Signal()

# Module disable signals
pre_disable = Signal()
post_disable = Signal()

# Module save signals
pre_save = Signal()
post_save = Signal()
