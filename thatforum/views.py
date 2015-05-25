from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import ThreadCreateUpdateForm, ThreadReplyForm
from .mixins import DetailWithListMixin, RequestForFormMixIn
from .models import ForumPost, ForumThread, ForumCategory


class ForumHome(ListView):
    model = ForumCategory

    def get_queryset(self):
        queryset = super(ForumHome, self).get_queryset()
        return queryset.filter(parent=None)


class ForumCategoryHome(DetailWithListMixin, DetailView):
    model = ForumCategory

    def dispatch(self, request, *args, **kwargs):
        self.list_model = self.get_list_model()
        self.list_attribute = self.get_list_attribute()
        return super(ForumCategoryHome, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ForumCategoryHome, self).get_context_data(**kwargs)
        if self.list_attribute == 'forumthread_set':
            context['list_type'] = 'threads'
        else:
            context['list_type'] = 'categories'
        context['extra_title'] = ' - %s' % self.object.name
        return context

    def get_list_attribute(self):
        if ForumCategory.objects.filter(parent=self.get_object()).count() == 0:
            return 'forumthread_set'
        else:
            return 'children'

    def get_list_model(self):
        if ForumCategory.objects.filter(parent=self.get_object()).count() == 0:
            return ForumThread
        else:
            return ForumCategory

    def get_list_queryset(self):
        if ForumCategory.objects.filter(parent=self.get_object()).count() == 0:
            return ForumThread.objects.filter(category=self.get_object())
        else:
            return ForumCategory.objects.filter(parent=self.get_object())


class ForumThreadHome(DetailWithListMixin, DetailView):
    model = ForumThread
    list_model = ForumPost
    list_attribute = 'forumpost_set'

    def get_list_queryset(self):
        return (self.list_model.objects.filter(thread=self.get_object(),
                is_thread_starter=False).order_by('created'))

    def get_context_data(self, **kwargs):
        context = super(ForumThreadHome, self).get_context_data(**kwargs)
        context['extra_title'] = ' - %s' % self.object.title
        return context


class ForumThreadCreateView(RequestForFormMixIn, CreateView):
    model = ForumThread
    form_class = ThreadCreateUpdateForm

    def get_form_kwargs(self):
        kwargs = super(ForumThreadCreateView, self).get_form_kwargs()
        kwargs.update({'category': ForumCategory.objects.get(slug=self.kwargs['slug'])})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ForumThreadCreateView, self).get_context_data(**kwargs)
        context['extra_title'] = ' - New Thread'
        return context


class ForumThreadReply(RequestForFormMixIn, CreateView):
    model = ForumThread
    form_class = ThreadReplyForm
    template_name = 'thatforum/forumpost_form.html'

    def get_context_data(self, **kwargs):
        context = super(ForumThreadReply, self).get_context_data(**kwargs)
        context['posts'] = (
            self.get_object().forumpost_set.all().order_by('-created')[:5]
        )

        context['object'] = self.get_object()
        context['show_cancel'] = self.get_object().get_absolute_url()
        context['extra_title'] = ' - Reply'
        return context

    def get_form_kwargs(self):
        kwargs = super(ForumThreadReply, self).get_form_kwargs()
        kwargs.update({'thread': self.get_object()})
        return kwargs

    def get_success_url(self):
        return self.get_object().get_absolute_url()


# class HomeView(TemplateView):
#     template_name = 'home.html'
