from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from apps.base.models import TimeStampedModel


class UserManager(_UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = UserManager()

    avatar = models.ImageField(verbose_name=_("Avatar"), upload_to='accounts/avatars/%Y/%m', null=True, blank=True)
    is_online = models.BooleanField(verbose_name=_("Is Online"), default=False)
    last_seen_at = models.DateTimeField(verbose_name=_("Last Seen At"), null=True, blank=True)

    def __str__(self):
        return self.username


class AccountSettings(TimeStampedModel):
    class Meta:
        db_table = "account_settings"
        verbose_name = _("Account Settings")
        verbose_name_plural = _("Account Settings")

    user = models.OneToOneField(
        verbose_name=_("User"),
        to="accounts.User",
        related_name="account_settings",
        on_delete=models.CASCADE,
    )
    show_last_seen = models.BooleanField(verbose_name=_("Show Last Seen"), default=True)
    show_read_receipts = models.BooleanField(
        verbose_name=_("Show Read Receipts"),
        help_text=_("Show Read Receipts in Private Chats"),
        default=True,
    )
    allow_to_add_groups = models.BooleanField(verbose_name=_("Allow to Add Groups"), default=True)
    allow_private_messages_to_non_contacts = models.BooleanField(
        verbose_name=_("Allow Private Messages to Non Contacts"), default=True
    )

    push_notifications_enabled = models.BooleanField(
        verbose_name=_("Push Notifications Enabled"), default=True
    )

    def __str__(self):
        return f"{self.user}"
