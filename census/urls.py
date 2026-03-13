from django.urls import path, re_path

from . import views

urlpatterns = [
    # Main site functionality
    path("", views.homepage, name="homepage"),
    path("", views.homepage, name="home"),
    path("homepage", views.homepage, name="homepage"),
    path("search/", views.search, name="search_for_something"),
    path("editions/<int:id>/", views.detail, name="detail"),
    path("about/", views.about, name="about"),
    re_path(r"^about/(?P<viewname>[A-Za-z0-9]+)/$", views.about, name="about"),
    path("copy/<int:id>/", views.copy, name="copy"),
    path("copydata/<int:copy_id>/", views.copy_data, name="copy_data"),
    path("draftcopydata/<int:copy_id>/", views.draft_copy_data, name="draft_copy_data"),
    path("add_copy/<int:id>/", views.add_copy, name="add_copy"),
    path("contact/", views.contact, name="contact"),
    path(
        "contact/contact_success/",
        views.display_contact_success,
        name="contact_success",
    ),
    # Admin start page:
    path("admin_start", views.admin_start, name="admin_start"),
    # Location verification page:
    path("admin_verify_copy/", views.admin_verify_copy, name="admin_verify_copy"),
    # ...and ajax call
    path(
        "admin_verify_location_verified",
        views.admin_verify_location_verified,
        name="admin_verify_location_verified",
    ),
    # Edit verification and submission verification pages:
    path("admin_edit_verify", views.admin_edit_verify, name="admin_edit_verify"),
    path(
        "admin_submission_verify",
        views.admin_submission_verify,
        name="admin_submission_verify",
    ),
    # ...and ajax calls
    path(
        "admin_verify_single_edit_accept/",
        views.admin_verify_single_edit_accept,
        name="admin_verify_single_edit_accept",
    ),
    path(
        "admin_verify_single_edit_reject/",
        views.admin_verify_single_edit_reject,
        name="admin_verify_single_edit_reject",
    ),
    # Librarian-specific verification UI elements:
    path("librarian_start", views.librarian_start, name="librarian_start"),
    path("librarian_validate1", views.librarian_validate1, name="librarian_validate1"),
    path("librarian_validate2", views.librarian_validate2, name="librarian_validate2"),
    path(
        "updatedraftcopy/<int:id>/", views.update_draft_copy, name="update_draft_copy"
    ),
    # url for the ajax view that creates the new draftcopy
    path("create_draftcopy/", views.create_draftcopy, name="create_draftcopy"),
    path("location_incorrect/", views.location_incorrect, name="location_incorrect"),
]
