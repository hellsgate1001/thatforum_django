from django import forms

from thatforum.forms import ThatForumBaseForm

from .models import ForumThread, ForumPost


class ThreadCreateUpdateForm(ThatForumBaseForm):
    post = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super(ThreadCreateUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        thread = super(ThreadCreateUpdateForm, self).save(False)
        thread.author = self.request.user
        thread.category = self.category
        thread.save()
        thread_post = ForumPost(
            thread=self.instance,
            post=self.cleaned_data['post'],
            author=self.request.user,
            is_thread_starter=True
        )
        thread_post.save()
        return thread

    class Meta:
        model = ForumThread
        fields = ('title',)


class ThreadReplyForm(ThatForumBaseForm):
    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop('thread')
        super(ThreadReplyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super(ThreadReplyForm, self).save(False)
        post.author = self.request.user
        post.thread = self.thread
        post.save()

    class Meta:
        model = ForumPost
        fields = ('post',)
