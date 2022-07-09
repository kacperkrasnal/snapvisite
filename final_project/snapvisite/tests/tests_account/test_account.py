from django.contrib.auth import get_user_model
profile = get_user_model()


def test_new_user(new_user):
    assert new_user.user_name == 'nickname'


def test_new_super_user(new_super_user):
    assert new_super_user.email == 'superuser@test.com'


def test_set_check_password(new_user):
    assert new_user.check_password("password") is False


def test_change_password(new_user):
    new_user.set_password("new-password")
    assert new_user.check_password("new-password") is True


def test_super_user_permissions(new_super_user):
    assert new_super_user.confirm is True
    assert new_super_user.is_superuser is True
    assert new_super_user.is_active is True
    assert new_super_user.is_staff is True


def test_user_permissions(new_user):
    assert new_user.confirm is True
    assert new_user.is_superuser is False
    assert new_user.is_active is True
    assert new_user.is_staff is False




