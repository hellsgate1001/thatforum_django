from factory import Sequence
from factory.django import DjangoModelFactory
from faker import Faker

from forumuser.tests.factories import UserFactory

from ..models import ForumCategory, ForumThread, ForumPost


class ForumCategoryFactory(DjangoModelFactory):
    FACTORY_FOR = ForumCategory
    name = Sequence(lambda n: 'forum-category-{0}'.format(n))


class ForumThreadFactory(DjangoModelFactory):
    FACTORY_FOR = ForumThread
    category = ForumCategoryFactory()
    title = Sequence(lambda n: 'forum-thread-{0}'.format(n))
    author = UserFactory()


class ForumPostFactory(DjangoModelFactory):
    FACTORY_FOR = ForumPost
    thread = ForumThreadFactory()
    author = UserFactory()
    post = Faker().text()
