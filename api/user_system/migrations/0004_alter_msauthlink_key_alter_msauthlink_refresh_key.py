# Generated by Django 5.1.2 on 2024-10-20 05:50

import encrypted_model_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_system', '0003_alter_msauthlink_key_alter_msauthlink_refresh_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msauthlink',
            name='key',
            field=encrypted_model_fields.fields.EncryptedCharField(),
        ),
        migrations.AlterField(
            model_name='msauthlink',
            name='refresh_key',
            field=encrypted_model_fields.fields.EncryptedCharField(),
        ),
    ]
