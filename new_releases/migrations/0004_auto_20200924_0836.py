# Generated by Django 3.1.1 on 2020-09-24 08:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('new_releases', '0003_spotifyusermodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spotifyusermodel',
            old_name='token',
            new_name='access_token',
        ),
        migrations.RemoveField(
            model_name='spotifyusermodel',
            name='user_id',
        ),
        migrations.AddField(
            model_name='spotifyusermodel',
            name='scope',
            field=models.CharField(default='token', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spotifyusermodel',
            name='token_type',
            field=models.CharField(default='token', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spotifyusermodel',
            name='user_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
