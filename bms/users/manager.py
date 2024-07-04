from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    Manager that manages the creation of user and superuser for User model in model.py
    """
    def create_user(self, username, email=None, password=None, **extras):
        extras.setdefault('is_active', True)
        extras.setdefault('is_employee', True)

        if not username:
            raise ValueError('Username is required!')
        email = self.normalize_email(email)
        user = self.model(username=username , email=email, **extras)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extras):
        owner_passkey = extras.pop('owner_passkey', None)
        extras.setdefault('is_owner', True)
        
        # 'passkey' is '1300' for creating owner/superuser
        if owner_passkey != '1300':
            raise ValueError('Wrong passkey/password to create OWNER USER')
        
        return self.create_user(username, email, password, **extras)
        
    def __repr__():
        return f'values which create_superuser function accepts are: "email", "password", "passkey required for superuser"'
        