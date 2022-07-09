import pytest
from pytest_factoryboy import register
from snapvisite.tests.factories.factories_user import UserFactory, SuperUserFactory
from snapvisite.tests.factories.factories_snapvisite import CategoryFactory, CompanyFactory
from django.contrib.auth import get_user_model
profile = get_user_model()


register(UserFactory)
register(SuperUserFactory)
register(CompanyFactory)
register(CategoryFactory)


@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def new_super_user(db, super_user_factory):
    superuser = super_user_factory.create()
    return superuser


@pytest.fixture
def new_category(db, category_factory):
    category = category_factory.create()
    return category


@pytest.fixture
def new_category2(db, category_factory):
    category = category_factory.create(category_name="Hairdresser")
    return category


@pytest.fixture
def new_company(db, company_factory):
    company = company_factory.create(company_name='FirstCompany')
    return company


@pytest.fixture
def new_company2(db, company_factory):
    company = company_factory.create(company_name='SecondCompany')
    return company
