from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField


class MsAuthLink(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expiry = models.IntegerField()
    key = EncryptedCharField(max_length=3000)  # Should be sufficient for most cases
    refresh_key = EncryptedCharField(max_length=3000)
    temp_token = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MsAuthLink for {self.user.username}"
    