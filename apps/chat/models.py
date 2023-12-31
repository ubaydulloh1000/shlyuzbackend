from django.contrib.auth import get_user_model
from django.db import models
from apps.base.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from . import managers

UserModel = get_user_model()


class Chat(TimeStampedModel):
    class ChatTypeChoices(models.TextChoices):
        PRIVATE = "PRIVATE", _("Private")
        GROUP = "GROUP", _("Group")
        CHANNEL = "CHANNEL", _("Channel")

    class Meta:
        db_table = "chat"
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")
        unique_together = ("user1", "user2")

    type = models.CharField(
        verbose_name=_("Type"),
        max_length=255,
        choices=ChatTypeChoices.choices,
        null=True,
    )
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="chat_avatars/%Y/%m/",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        verbose_name=_("Owner"),
        to="accounts.User",
        related_name="owned_chat_groups",
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        verbose_name=_("Members"),
        to="accounts.User",
        related_name="chats",
        blank=True,
    )
    user1 = models.ForeignKey(
        verbose_name=_("User 1"),
        to="accounts.User",
        related_name="user1_chats",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user2 = models.ForeignKey(
        verbose_name=_("User 2"),
        to="accounts.User",
        related_name="user2_chats",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def is_permitted(self, user: UserModel) -> bool:
        return bool(
            self.chat_memberships.filter(user_id=user.pk).exists()
        )


class ChatMembership(TimeStampedModel):
    class Meta:
        db_table = "chat_membership"
        verbose_name = _("Chat Membership")
        verbose_name_plural = _("Chat Memberships")
        unique_together = ("chat", "user")

    chat = models.ForeignKey(
        verbose_name=_("Chat"),
        to="chat.Chat",
        related_name="chat_memberships",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name=_("User"),
        to="accounts.User",
        related_name="chat_memberships",
        on_delete=models.CASCADE,
    )
    is_archived = models.BooleanField(verbose_name=_("Is Archived"), default=False)
    is_muted = models.BooleanField(verbose_name=_("Is Muted"), default=False)

    objects = managers.ChatMembershipQuerySet.as_manager()

    def __str__(self):
        return f"{self.chat} - {self.user}"


class Message(TimeStampedModel):
    class Meta:
        db_table = "message"
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ("-created_at",)

    class MessageTypeChoices(models.TextChoices):
        TEXT = "TEXT", _("Text")
        IMAGE = "IMAGE", _("Image")
        VIDEO = "VIDEO", _("Video")
        AUDIO = "AUDIO", _("Audio")

    chat = models.ForeignKey(
        verbose_name=_("Chat"),
        to="chat.Chat",
        related_name="messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sender = models.ForeignKey(
        verbose_name=_("Sender"),
        to="accounts.User",
        related_name="messages",
        on_delete=models.CASCADE,
        null=True,
    )
    recipient = models.ForeignKey(
        verbose_name=_("Recipient"),
        to="accounts.User",
        related_name="received_messages",
        on_delete=models.CASCADE,
        null=True,
    )
    type = models.CharField(
        verbose_name=_("Type"),
        max_length=255,
        choices=MessageTypeChoices.choices,
        default=MessageTypeChoices.TEXT,
    )
    content = models.TextField(verbose_name=_("Content"))
    is_seen = models.BooleanField(verbose_name=_("Is Seen"), default=False)
    seen_at = models.DateTimeField(verbose_name=_("Seen At"), null=True, blank=True)
    is_edited = models.BooleanField(verbose_name=_("Is Edited"), default=False)
    is_reacted = models.BooleanField(verbose_name=_("Is Reacted"), default=False)

    objects = managers.MessageQuerySet.as_manager()

    def __str__(self):
        return self.type

    @staticmethod
    async def get_unread_count_for_private_chat(sender: UserModel, recipient: UserModel) -> int:
        return Message.objects.filter(
            sender=sender,
            recipient=recipient,
        ).count()


class MessageSee(TimeStampedModel):
    class Meta:
        db_table = "message_see"
        verbose_name = _("Message See")
        verbose_name_plural = _("Message Sees")
        unique_together = ("message", "user")

    message = models.ForeignKey(
        verbose_name=_("Message"),
        to="chat.Message",
        related_name="message_sees",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name=_("User"),
        to="accounts.User",
        related_name="message_sees",
        on_delete=models.CASCADE,
    )
    is_reacted = models.BooleanField(verbose_name=_("Is Reacted"), default=False)

    def __str__(self):
        return f"{self.message} - {self.user}"
