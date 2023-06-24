# Generated by Django 4.2.2 on 2023-06-24 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan sana')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_chat_groups', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'db_table': 'chat_group',
            },
        ),
        migrations.CreateModel(
            name='PrivateChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan sana')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_chats1', to=settings.AUTH_USER_MODEL, verbose_name='User 1')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_chats2', to=settings.AUTH_USER_MODEL, verbose_name='User 2')),
            ],
            options={
                'db_table': 'private_chat',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan sana')),
                ('type', models.CharField(choices=[('TEXT', 'Text'), ('IMAGE', 'Image'), ('VIDEO', 'Video'), ('AUDIO', 'Audio')], default='TEXT', max_length=255, verbose_name='Type')),
                ('content', models.TextField(verbose_name='Content')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatgroup', verbose_name='Group')),
                ('private_chat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.privatechat', verbose_name='Private Chat')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]