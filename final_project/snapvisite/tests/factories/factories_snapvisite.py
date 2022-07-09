import factory
from faker import Faker
from django.contrib.auth import get_user_model
from snapvisite.models import Company, Category
from snapvisite.tests.factories.factories_user import UserFactory, SuperUserFactory
profile = get_user_model()
fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    category_name = 'category'


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    company_name = 'company'
    description = fake.text()
    owner = factory.SubFactory(UserFactory)

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.category.add(category)

    phone_number = "+48519874567"
    email = fake.ascii_company_email()
