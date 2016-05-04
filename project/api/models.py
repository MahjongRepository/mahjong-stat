from django.db import models

from api.utils import make_random_letters_string
from website.accounts.models import User


class ApiToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_api_token'

    def __str__(self):
        return self.token

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.token:
            self.token = make_random_letters_string(40)

        super(ApiToken, self).save(force_insert, force_update, using, update_fields)
