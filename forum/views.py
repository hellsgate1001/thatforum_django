from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render

from thatforum.mixins import RequestForFormMixIn

from .forms import ThreadCreateUpdateForm, ThreadReplyForm
from .models import ForumPost, ForumThread, ForumCategory


class DetailWithListMixin(object):
    valid_sort_fields = ()
    valid_sort_directions = {'asc': '', 'desc': '-'}
    list_model = None
    list_attribute = None
    paginate_by = 25

    def dispatch(self, request, *args, **kwargs):
        self.list_queryset = self.get_list_queryset()
        # Which content items should be shown?
        try:
            self.page = int(self.request.GET.get('page'))
        except (TypeError, ValueError) as e:
            # If the page is not an integer, deliver the first page
            self.page = 1

        # Sorting
        self.sorton = request.GET.get('sorton', '')
        self.sort_direction = request.GET.get('sort_direction', 'asc')
        # Validate the sort parameters
        if self.sorton not in self.valid_sort_fields:
            self.sorton = ''
        if self.sort_direction not in self.valid_sort_directions:
            self.sort_direction = 'asc'
        # build the items queryset
        self._build_sorted_queryset()

        return super(DetailWithListMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailWithListMixin, self).get_context_data(**kwargs)
        context['sorting'] = self._get_sorting_details()
        context['list_items'] = self._get_items_for_list()
        return context

    def get_list_attribute(self):
        return self.list_attribute

    def get_list_model(self, list_queryset=None):
        return self.list_model

    def get_list_queryset(self, *args, **kwargs):
        return self.list_model.objects.all()

    def _build_sorted_queryset(self):
        if (self.sorton not in self.valid_sort_fields or
            self.sort_direction not in self.valid_sort_directions.keys()):
            self.list_queryset = self.get_list_queryset()
            return

        ordering_string = '%(direction)s%(field)s' % {
            'direction': self.valid_sort_directions[self.sort_direction],
            'field': self.sorton
        }

        self.list_queryset = self.get_list_queryset().order_by(ordering_string)

    def _get_items_for_list(self):
        paginator = Paginator(self.list_queryset, self.paginate_by)
        try:
            list_items = paginator.page(self.page)
        except PageNotAnInteger:
            # Page is not an integer, serve the first page
            list_items = paginator.page(1)
        except EmptyPage:
            # Page is out of range, serve the last page
            list_items = paginator.page(paginator.num_pages)

        list_items = self._mark_selected_items(list_items)
        return list_items

    def _get_sorting_details(self):
        # build a dictionary to pass to the template to allow correct building
        # of the sort headers of the table
        sorting_info = {}
        for field in self.valid_sort_fields:
            if self.sorton == field:
                sorting_info[field] = 'asc' if self.sort_direction == 'desc' else 'desc'
            else:
                sorting_info[field] = 'desc'

        return sorting_info

    def _mark_selected_items(self, items):
        # Mark any items that are in the current blocked list
        selected = getattr(self.object, self.list_attribute).all()
        for item in items:
            item.selected = item in selected
        return items


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


class ForumThreadCreateView(RequestForFormMixIn, CreateView):
    model = ForumThread
    form_class = ThreadCreateUpdateForm

    def get_form_kwargs(self):
        kwargs = super(ForumThreadCreateView, self).get_form_kwargs()
        kwargs.update({'category': ForumCategory.objects.get(slug=self.kwargs['slug'])})
        return kwargs


class ForumThreadReply(RequestForFormMixIn, CreateView):
    model = ForumThread
    form_class = ThreadReplyForm
    template_name = 'forum/forumpost_form.html'

    def get_context_data(self, **kwargs):
        context = super(ForumThreadReply, self).get_context_data(**kwargs)
        context['posts'] = (
            self.get_object().forumpost_set.all().order_by('-created')[:5]
        )
        return context

    def get_form_kwargs(self):
        kwargs = super(ForumThreadReply, self).get_form_kwargs()
        kwargs.update({'thread': self.get_object()})
        return kwargs

    def get_success_url(self):
        return self.get_object().get_absolute_url()
