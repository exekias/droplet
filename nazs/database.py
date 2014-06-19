

class VolatileRouter(object):
    """
    Router to use special db for volatile models
    """
    def db_for_read(self, model, **hints):
        if self._model_volatile(model):
            return 'volatile'
        return None

    def db_for_write(self, model, **hints):
        if self._model_volatile(model):
            return 'volatile'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, model):
        if db == 'volatile':
            return False
        return None

    def _model_volatile(self, model):
        if hasattr(model, 'volatile'):
            return model.volatile
        return False
