from django.test import TestCase

from forumuser.tests.factories import UserFactory


class ThatForumTestCase(TestCase):
    def login_user(self, user=None, password='testpassword', **kwargs):
        if user is None:
            user = UserFactory.create(**kwargs)

        user.set_password(password)
        user.save()
        self.client.login(username=user.username, password=user.password)
        return user

    def logout_user(self, user):
        self.client.logout()

    def GET(self, url, status=200):
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, status)
        return response

    def POST(self, url, params, status=200):
        response = self.client.post(url, params)
        self.failUnlessEqual(response.status_code, status)
        return response
