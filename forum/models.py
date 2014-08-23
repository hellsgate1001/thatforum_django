from django.conf import settings
from django.db import models


class ForumCategory(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Forum categories'


class ForumThread(models.Model):
    category = models.ForeignKey(ForumCategory)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    post = models.TextField()

    def __unicode__(self):
        return self.title


class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread)
    post = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return '%(thread)s - %(pk)s' % {
            'thread': self.thread.title,
            'pk': self.pk
        }
