from django.core.urlresolvers import reverse

from forumuser.tests.factories import UserFactory
from thatforum.test_helpers import ThatForumTestCase


class TestUserListView(ThatForumTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.list_url = reverse('user:list')

    def test_non_logged_in(self):
        response = self.GET(self.list_url, 302)
