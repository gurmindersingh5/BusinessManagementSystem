class UsersdbRouter:
    """
    A router to control all database operations on models in the
    users application.
    """
    label = ['users']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.label:
            return 'usersdb'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.label:
            return 'usersdb'
        return None

    def allow_relations(self, obj1, obj2, **hints):
        """Allow relations if both models are involved in the usersdb."""
        if obj1._state.db in self.label or obj2._state.db in self.label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the usersdb only appears in the 'usersdb' database.
        if model_name == '' all models uses usersdb only so no need use model_name
        """
        if app_label in self.label:
                return db == 'userdb'
        
        # Allow migrations for other apps only on the 'default' database
        return db == 'default' # for now all other apps use default db