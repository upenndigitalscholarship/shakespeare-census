import pytest
from django.conf import settings
from django.test import RequestFactory
from model_bakery import baker

from users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def census_data(db):
    """Build a minimal but realistic graph of census objects for view tests."""
    location = baker.make("census.Location", name="Bodleian Library")

    title = baker.make("census.Title", title="Hamlet", apocryphal=False, hidden=False)
    edition = baker.make(
        "census.Edition", title=title, edition_number="1", edition_format="Folio"
    )
    issue = baker.make(
        "census.Issue",
        edition=edition,
        stc_wing="STC 22273",
        estc="S111604",
        year="1623",
        start_date=1623,
        end_date=1623,
    )
    copy = baker.make(
        "census.CanonicalCopy",
        issue=issue,
        location=location,
        shelfmark="Arch. G c.7",
        nsc="1.1",
        fragment=False,
        location_verified=True,
    )

    return {
        "location": location,
        "title": title,
        "edition": edition,
        "issue": issue,
        "copy": copy,
    }
