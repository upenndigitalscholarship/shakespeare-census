import csv
import io

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
        response = client.get(
            "/search/", {"field": "location", "value": "Bodleian Library"}
        )
        assert response.status_code == 200

    def test_search_by_location_finds_copy(self, client, census_data):
        response = client.get(
            "/search/", {"field": "location", "value": "Bodleian Library"}
        )
        assert census_data["copy"] in response.context["result_list"]

    def test_search_empty_returns_200(self, client, census_data):
        response = client.get("/search/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestLocationCopyCountCsvExport:
    def test_returns_200(self, client, census_data):
        url = reverse("location_copy_count_csv_export")
        response = client.get(url)
        assert response.status_code == 200

    def test_content_type_is_csv(self, client, census_data):
        url = reverse("location_copy_count_csv_export")
        response = client.get(url)
        assert response["Content-Type"] == "text/csv"

    def test_has_content_disposition_header(self, client, census_data):
        url = reverse("location_copy_count_csv_export")
        response = client.get(url)
        assert "attachment" in response["Content-Disposition"]
        assert (
            "shakespeare_census_location_copy_count.csv"
            in response["Content-Disposition"]
        )

    def test_csv_has_correct_headers(self, client, census_data):
        url = reverse("location_copy_count_csv_export")
        response = client.get(url)
        content = response.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        headers = next(reader)
        assert headers == ["Location", "Number of Copies"]

    def test_csv_includes_census_data(self, client, census_data):
        url = reverse("location_copy_count_csv_export")
        response = client.get(url)
        content = response.content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        location_names = [row["Location"] for row in rows]
        assert census_data["location"].name in location_names


@pytest.mark.django_db
class TestYearIssueCopyCountCsvExport:
    def test_returns_200(self, client, census_data):
        url = reverse("year_issue_copy_count_csv_export")
        response = client.get(url)
        assert response.status_code == 200

    def test_content_type_is_csv(self, client, census_data):
        url = reverse("year_issue_copy_count_csv_export")
        response = client.get(url)
        assert response["Content-Type"] == "text/csv"

    def test_has_content_disposition_header(self, client, census_data):
        url = reverse("year_issue_copy_count_csv_export")
        response = client.get(url)
        assert "attachment" in response["Content-Disposition"]
        assert (
            "shakespeare_census_year_issue_copy_count.csv"
            in response["Content-Disposition"]
        )

    def test_csv_has_correct_headers(self, client, census_data):
        url = reverse("year_issue_copy_count_csv_export")
        response = client.get(url)
        content = response.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        headers = next(reader)
        assert headers == ["Year", "STC/Wing", "Title", "Number of Copies"]

    def test_csv_includes_census_data(self, client, census_data):
        url = reverse("year_issue_copy_count_csv_export")
        response = client.get(url)
        content = response.content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        stc_values = [row["STC/Wing"] for row in rows]
        assert census_data["issue"].stc_wing in stc_values


@pytest.mark.django_db
class TestCopyScBartlettCsvExport:
    def test_returns_200(self, client, census_data):
        url = reverse("copy_sc_bartlett_csv_export")
        response = client.get(url)
        assert response.status_code == 200

    def test_content_type_is_csv(self, client, census_data):
        url = reverse("copy_sc_bartlett_csv_export")
        response = client.get(url)
        assert response["Content-Type"] == "text/csv"

    def test_has_content_disposition_header(self, client, census_data):
        url = reverse("copy_sc_bartlett_csv_export")
        response = client.get(url)
        assert "attachment" in response["Content-Disposition"]
        assert "shakespeare_census_sc_bartlett.csv" in response["Content-Disposition"]

    def test_csv_has_correct_headers(self, client, census_data):
        url = reverse("copy_sc_bartlett_csv_export")
        response = client.get(url)
        content = response.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        headers = next(reader)
        assert headers == [
            "SC #",
            "Bartlett 1939 #",
            "Bartlett 1916 #",
            "Title",
            "Year",
        ]


@pytest.mark.django_db
class TestExport:
    def test_export_count_returns_200(self, client, census_data):
        url = reverse(
            "export",
            kwargs={"groupby": "location", "column": "id", "aggregate": "count"},
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_export_sum_returns_200(self, client, census_data):
        url = reverse(
            "export",
            kwargs={"groupby": "location", "column": "height", "aggregate": "sum"},
        )
        response = client.get(url)
        assert response.status_code == 200

    def test_content_type_is_csv(self, client, census_data):
        url = reverse(
            "export",
            kwargs={"groupby": "location", "column": "id", "aggregate": "count"},
        )
        response = client.get(url)
        assert response["Content-Type"] == "text/csv"

    def test_csv_has_correct_headers(self, client, census_data):
        url = reverse(
            "export",
            kwargs={"groupby": "location", "column": "id", "aggregate": "count"},
        )
        response = client.get(url)
        content = response.content.decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        headers = next(reader)
        assert headers == ["location", "count of id"]

    def test_invalid_groupby_returns_404(self, client, census_data):
        url = reverse(
            "export",
            kwargs={"groupby": "invalid_column", "column": "id", "aggregate": "count"},
        )
        response = client.get(url)
        assert response.status_code == 404

    def test_invalid_column_returns_404(self, client, census_data):
        url = reverse(
            "export",
            kwargs={
                "groupby": "location",
                "column": "invalid_column",
                "aggregate": "count",
            },
        )
        response = client.get(url)
        assert response.status_code == 404
