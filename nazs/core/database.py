

class VolatileRouter(object):
    """
    Router to use special db for volatile models
    """
    def db_for_read(self, model, **hints):
        if self._model_volatile(model):
            return 'volatile_db'
        return None

    def db_for_write(self, model, **hints):
        if self._model_volatile(model):
            return 'volatile_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, model):
        if db == 'volatile_db':
            return False
        return None

    def _model_volatile(self, model):
        if hasattr(model._meta, 'volatile'):
            return model._meta.volatile
        return False
