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
        list_url = reverse('list')
        response = self.GET(list_url)
        import pdb;pdb.set_trace()
        self.assertEqual(response.context['object_list'].count(), settings.DEFAULT_PAGINATE_BY)
