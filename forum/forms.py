from django import forms

from .models import ForumThread, ForumPost


class ThreadCreateUpdateForm(forms.ModelForm):
    post = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
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


class ThreadReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.thread = kwargs.pop('thread')
        super(ThreadReplyForm, self).__init__(*args, **kwargs)
        for fn, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        post = super(ThreadReplyForm, self).save(False)
        post.author = self.request.user
        post.thread = self.thread
        post.save()

    class Meta:
        model = ForumPost
        fields = ('post',)
