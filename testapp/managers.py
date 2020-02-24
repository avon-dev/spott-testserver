from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_uid, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not user_uid:
            raise ValueError('The given email must be set')
        email = self.normalize_email(user_uid)
        user = self.model(user_uid=user_uid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_uid, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_uid, password, **extra_fields)

    def create_superuser(self, user_uid, password, **extra_fields):
        user = self.create_user(
            user_uid=user_uid,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(is_active=True)
