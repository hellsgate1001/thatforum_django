from django.conf import settings
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class ForumCategory(MPTTModel):
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    @property
    def post_count(self):
        count = 0
        for thread in self.forumthread_set.all():
            count+= thread.forumpost_set.count()
        return count

    # @post_count.setter
    # def post_count(self, value):
    #     self._post_count = value


    class Meta:
        verbose_name_plural = 'Forum categories'


class ForumThread(models.Model):
    category = models.ForeignKey(ForumCategory)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    @property
    def num_replies(self):
        return self.forumpost_set.filter(is_thread_starter=False).count()


class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread)
    post = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    reply_to = models.ForeignKey('self', blank=True, null=True)
    is_thread_starter = models.BooleanField(default=False)

    def __unicode__(self):
        return '%(thread)s - %(pk)s' % {
            'thread': self.thread.title,
            'pk': self.pk
        }
