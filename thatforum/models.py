from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

from mptt.models import MPTTModel, TreeForeignKey


class ForumCategory(MPTTModel):
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    @property
    def post_count(self):
        count = 0
        for thread in self.forumthread_set.all():
            count += thread.forumpost_set.count()
        return count

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

    def get_absolute_url(self):
        return reverse('thread_home', kwargs={'slug': self.slug})

    @property
    def last_post(self):
        return self.forumpost_set.order_by('-created').first()

    @property
    def num_replies(self):
        return self.forumpost_set.filter(is_thread_starter=False).count()

    @property
    def thread_starter(self):
        return self.forumpost_set.get(thread=self, is_thread_starter=True)

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)
        return super(ForumThread, self).save(*args, **kwargs)


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

    def get_breadcrumb(self):
        breadcrumb = [
            (
                self.thread.title,
                reverse(
                    'thread_home',
                    kwargs={'slug': self.thread.slug}
                )
            ),
        ]
        category = self.thread.category
        while True:
            breadcrumb_item = (
                category.name,
                reverse(
                    'category_home',
                    kwargs={'slug': category.slug}
                ),
            )
            breadcrumb.insert(0, breadcrumb_item)
            if category.parent is None:
                break
            category = category.parent

        return breadcrumb
