import factory
from faker import Faker
from django.contrib.auth import get_user_model
profile = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = profile

    email = 'user@test.com'
    user_name = 'nickname'
    first_name = fake.first_name()
    last_name = fake.last_name()
    is_active = True
    is_staff = False
    is_superuser = False
    phone_number = '+48517856890'
    confirm = True


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = profile

    email = 'superuser@test.com'
    user_name = 'supernickname'
    first_name = fake.first_name()
    last_name = fake.last_name()
    is_active = True
    is_staff = True
    is_superuser = True
    phone_number = '+48670765567'
    confirm = True



