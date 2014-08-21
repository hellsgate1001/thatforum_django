from django.contrib.auth import get_user_model

from factory import Sequence
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = Sequence(lambda n: 'user-{0}'.format(n))
    email = Sequence(lambda n: 'person{0}@example.com'.format(n))
