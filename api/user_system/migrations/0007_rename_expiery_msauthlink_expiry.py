# Generated by Django 5.1.2 on 2024-10-20 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_system', '0006_msauthlink_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='msauthlink',
            old_name='expiery',
            new_name='expiry',
        ),
    ]
