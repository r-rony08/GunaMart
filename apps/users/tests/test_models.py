import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.users.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


@pytest.mark.django_db
def test_create_user_with_email_and_username():
    user = User.objects.create_user(
        email="customer@example.com",
        username="customer",
        password="TestPassword123",
    )

    assert user.email == "customer@example.com"
    assert user.username == "customer"
    assert user.role == User.Role.CUSTOMER
    assert user.is_active is True
    assert user.is_staff is False


@pytest.mark.django_db
def test_user_password_is_hashed():
    user = User.objects.create_user(
        email="customer@example.com",
        username="customer",
        password="TestPassword123",
    )

    assert user.password != "TestPassword123"
    assert user.check_password("TestPassword123") is True
    assert user.check_password("WrongPassword") is False


@pytest.mark.django_db
def test_create_user_without_email_raises_error():
    with pytest.raises(ValueError, match="email field must be set"):
        User.objects.create_user(
            email="",
            username="customer",
            password="TestPassword123",
        )


@pytest.mark.django_db
def test_user_default_role_is_customer():
    user = User.objects.create_user(
        email="customer@example.com",
        username="customer",
        password="TestPassword123",
    )

    assert user.role == User.Role.CUSTOMER


@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(
        email="admin@example.com",
        username="admin",
        password="AdminPassword123",
    )

    assert admin.is_staff is True
    assert admin.is_superuser is True
    assert admin.is_active is True


@pytest.mark.django_db
def test_email_must_be_unique():
    User.objects.create_user(
        email="customer@example.com",
        username="customer1",
        password="TestPassword123",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="customer@example.com",
            username="customer2",
            password="TestPassword123",
        )


@pytest.mark.django_db
def test_username_must_be_unique():
    User.objects.create_user(
        email="customer1@example.com",
        username="customer",
        password="TestPassword123",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="customer2@example.com",
            username="customer",
            password="TestPassword123",
        )


@pytest.mark.django_db
def test_user_can_have_phone_number():
    user = User.objects.create_user(
        email="customer@example.com",
        username="customer",
        password="TestPassword123",
        phone_number="+8801712345678",
    )

    assert user.phone_number == "+8801712345678"


def test_phone_number_is_not_in_required_fields():
    assert "phone_number" not in User.REQUIRED_FIELDS


@pytest.mark.django_db
def test_user_profile_can_be_created():

    user = User.objects.create_user(
        email="profile@example.com",
        username="profileuser",
        password="TestPassword123",
    )

    profile = UserProfile.objects.create(
        user=user
    )

    assert profile.user == user
    assert user.profile == profile
    assert profile.profile_picture.name is None


@pytest.mark.django_db
def test_user_profile_has_related_user():

    user = User.objects.create_user(
        email="profile@example.com",
        username="profileuser",
        password="TestPassword123",
    )

    profile = UserProfile.objects.create(user=user)

    assert user.profile == profile


@pytest.mark.django_db
def test_user_profile_can_store_profile_picture():

    user = User.objects.create_user(
        email="avatar@example.com",
        username="avataruser",
        password="TestPassword123",
    )

    image = SimpleUploadedFile(
        name="avatar.jpg",
        content=(
            b"\xFF\xD8\xFF\xE0"
            b"\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
            b"\xFF\xDB\x00\x43\x00"
            b"\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\x09"
        ),
        content_type="image/jpeg",
    )

    profile = UserProfile.objects.create(
        user=user,
        profile_picture=image,
    )

    assert profile.profile_picture.name.startswith("profiles/")