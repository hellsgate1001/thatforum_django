from django.conf import settings
from django.core.urlresolvers import reverse

from thatforum.test_helpers import ThatForumTestCase

from .factories import (ForumCategoryFactory, ForumThreadFactory,
    ForumPostFactory)


class TestListView(ThatForumTestCase):
    def setUp(self):
        self.category = ForumCategoryFactory()
        self.thread = ForumThreadFactory(category=self.category)
        self.posts = ForumPostFactory.create_batch(40, thread=self.thread)

    def test_pagination(self):
        list_url = reverse('thread_home', kwargs={'slug': self.thread.slug})
        response = self.GET(list_url)
        self.assertEqual(
            len(response.context['list_items'].object_list),
            settings.DEFAULT_PAGINATE_BY
        )
