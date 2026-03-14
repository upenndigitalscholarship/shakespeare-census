import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestHomepage:
    def test_root_returns_200(self, client, census_data):
        response = client.get("/")
        assert response.status_code == 200

    def test_homepage_path_returns_200(self, client, census_data):
        response = client.get("/homepage")
        assert response.status_code == 200

    def test_titles_in_context(self, client, census_data):
        response = client.get("/")
        titles = [t for row in response.context["titlerows"] for t in row]
        assert census_data["title"] in titles


@pytest.mark.django_db
class TestEditionDetail:
    def test_edition_detail_returns_200(self, client, census_data):
        url = reverse("detail", kwargs={"id": census_data["title"].pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_edition_detail_contains_issues(self, client, census_data):
        url = reverse("detail", kwargs={"id": census_data["title"].pk})
        response = client.get(url)
        assert census_data["issue"] in response.context["issues"]

    def test_edition_detail_copy_count(self, client, census_data):
        url = reverse("detail", kwargs={"id": census_data["title"].pk})
        response = client.get(url)
        assert response.context["copy_count"] == 1


@pytest.mark.django_db
class TestCopyView:
    def test_copy_view_returns_200(self, client, census_data):
        url = reverse("copy", kwargs={"id": census_data["issue"].pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_copy_view_lists_copies(self, client, census_data):
        url = reverse("copy", kwargs={"id": census_data["issue"].pk})
        response = client.get(url)
        assert census_data["copy"] in response.context["all_copies"]

    def test_copy_view_copy_count(self, client, census_data):
        url = reverse("copy", kwargs={"id": census_data["issue"].pk})
        response = client.get(url)
        assert response.context["copy_count"] == 1


@pytest.mark.django_db
class TestSearch:
    def test_search_by_stc_returns_200(self, client, census_data):
        response = client.get("/search/", {"field": "stc", "value": "STC 22273"})
        assert response.status_code == 200

    def test_search_by_stc_finds_copy(self, client, census_data):
        response = client.get("/search/", {"field": "stc", "value": "STC 22273"})
        assert census_data["copy"] in response.context["result_list"]

    def test_search_by_location_returns_200(self, client, census_data):
        response = client.get("/search/", {"field": "location", "value": "Bodleian Library"})
        assert response.status_code == 200

    def test_search_by_location_finds_copy(self, client, census_data):
        response = client.get("/search/", {"field": "location", "value": "Bodleian Library"})
        assert census_data["copy"] in response.context["result_list"]

    def test_search_empty_returns_200(self, client, census_data):
        response = client.get("/search/")
        assert response.status_code == 200
