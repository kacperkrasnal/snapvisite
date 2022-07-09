import pytest

from django.contrib.auth import get_user_model
from faker import Faker
from snapvisite.forms import CreateCompanyFirstStepForm, EditCategoriesForm, AddressForm, UpdateCompanyNameForm

profile = get_user_model()
fake = Faker()


@pytest.mark.parametrize(
    "company_name, category, validity",
    [
        ('Firma1', [1], True),
        ('Firma2', [1, 2], True),
        ('Firma321312313121231231asdadsasdasdasdads asdas', [1], False),  # Too long company_name
        ('Firma3', [1, 2, 3], False),  # In db exist only 2 categories
        ('Firma4', [], False)  # Minimum one category is needed.
    ],
)
@pytest.mark.django_db
def test_company_create_form(
        company_name, category, validity, new_category, new_category2
):
    form = CreateCompanyFirstStepForm(
        data={
            "company_name": company_name,
            "category": category
        }
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "category, validity",
    [
        ([1], True),
        ([1, 2], True),
        ([1, 2, 3], False),  # In db exist only 2 categories
        ([], False)  # Minimum one category is needed.
    ],
)
@pytest.mark.django_db
def test_edit_categories_form(
        category, validity, new_company, new_category, new_category2
):
    form = EditCategoriesForm(
        data={
            "category": category
        }
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "city, postal_code, street_name, street_number, apartment_number, validity",
    [
        ("Warsaw", "00-420", "Long", "13", "4", True),
        ("warsaw", "00-420", "Long", "13", "4", False),
        ("warsaw", "00-42000986", "Long", "13", "4", False),
        ("Warsaw", "00-420", "Long", "13", "", True)
    ],
)
@pytest.mark.django_db
def test_create_address_form(
        city, postal_code, street_name, street_number, apartment_number, validity, new_company
):
    form = AddressForm(
        data={
            "city": city,
            "postal_code": postal_code,
            "street_name": street_name,
            "street_number": street_number,
            "apartment_number": apartment_number
        }
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "company_name, validity",
    [
        ("ProjectOne", True),
        ("Company Name Is Too Long for this form", False)
    ],
)
@pytest.mark.django_db
def test_edit_company_name_form(
        company_name, validity, new_company,
):
    form = UpdateCompanyNameForm(
        data={
            "company_name": company_name
        }
    )
    assert form.is_valid() is validity
