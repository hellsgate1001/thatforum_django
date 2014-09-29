from django.contrib.auth.models import AbstractUser, Group
from django.core.urlresolvers import reverse
from django.db import models


class ForumUser(AbstractUser):
    items_per_page = models.PositiveSmallIntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%(username)s (%(email)s)' % {
            'username': self.username,
            'email': self.email
        }

    def get_absolute_url(self, *args, **kwargs):
        return reverse('user:detail', kwargs={'pk': self.pk})

    @property
    def name(self):
        if any(self.first_name) and any(self.last_name):
            return '%s %s' % (self.first_name, self.last_name)
        elif any(self.first_name):
            return self.first_name
        elif any(self.last_name):
            return self.last_name
        else:
            return self.username
