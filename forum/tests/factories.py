from factory import Sequence
from factory.django import DjangoModelFactory
from faker import Faker

from forumuser.tests.factories import UserFactory


class ForumCategoryFactory(DjangoModelFactory):
    name = Sequence(lambda n: 'forum-category-{0}'.format(n))


class ForumThreadFactory(DjangoModelFactory):
    category = ForumCategoryFactory()
    title = Sequence(lambda n: 'forum-thread-{0}'.format(n))
    user = UserFactory()


class ForumPostFactory(DjangoModelFactory):
    thread = ForumThreadFactory()
    author = UserFactory()
    post = Faker().text()
