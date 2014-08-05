from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class ForumUser(AbstractUser):
    def __unicode__(self):
        return '%(username)s (%(email)s)' % {
            'username': self.username,
            'email': self.email
        }
