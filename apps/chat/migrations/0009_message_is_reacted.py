# Generated by Django 4.2.4 on 2023-09-02 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_chat_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_reacted',
            field=models.BooleanField(default=False, verbose_name='Is Reacted'),
        ),
    ]
