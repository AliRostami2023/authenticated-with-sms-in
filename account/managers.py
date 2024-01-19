from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, full_name, phone_number, password):
        if not full_name:
            raise ValueError('user must have full name')

        if not phone_number:
            raise ValueError('user must have phone number')

        user = self.model(full_name=full_name, phone_number=phone_number, username=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user
