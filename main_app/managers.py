from django.contrib.auth.base_user import BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError('Users must have a phone')

        user = self.model(
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(
            phone,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
