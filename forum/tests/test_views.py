from django.conf import settings
from django.core.urlresolvers import reverse

from forum.tests.factories import (ForumCategoryFactory, ForumThreadFactory,
    ForumPostFactory)
from thatforum.test_helpers import ThatForumTestCase


class TestListView(ThatForumTestCase):
    def setUp(self):
        self.category = ForumCategoryFactory()
        self.thread = ForumThreadFactory(category=category)
        self.posts = ForumPostFactory.create_batch(40, thread=thread)

    def test_pagination(self):
        list_url = reverse('forum:list')
        response = self.GET(list_url)
        import pdb;pdb.set_trace()
        self.assertEqual(response.context['object_list'].count(), settings.DEFAULT_PAGINATE_BY)
