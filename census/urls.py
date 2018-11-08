from django.conf.urls import url, include
from django.contrib.auth.views import (password_reset,
                                       password_reset_done,
                                       password_reset_confirm,
                                       password_reset_complete,
                                       password_change,
                                       password_change_done,
                                       logout)

from . import views

# from .models import StaticPageText
# _static_page_names = '|'.join(sorted(set(s.viewname for s in StaticPageText.objects.all())))

urlpatterns = [
    # Main site functionality
    url(r'^$', views.homepage, name='homepage'),
    url(r'^$', views.homepage, name='home'),
    url(r'^homepage$',views.homepage, name='homepage'),
    url(r'^search/$', views.search, name='search_for_something'),
    url(r'^editions/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^about/$', views.about, name='about'),
    url(r'^about/(?P<viewname>[A-Za-z0-9]+)/$', views.about, name='about'),
    url(r'^copy/(?P<id>[0-9]+)/$', views.copy, name='copy'),
    url(r'^copydata/(?P<copy_id>[0-9]+)/$', views.copy_data, name='copy_data'),
    url(r'^draftcopydata/(?P<copy_id>[0-9]+)/$', views.draft_copy_data, name='draft_copy_data'),
    url(r'^add_copy/(?P<id>[0-9]+)/$', views.add_copy, name='add_copy'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/contact_success/$', views.display_contact_success, name='contact_success'),

    # User accounts and management
    url(r'^login', views.login_user, name='login_user'),
    url(r'^logout$', views.logout_user, name='logout_user'),
    url(r'^profile$', views.display_user_profile, name='profile'),
    url(r'^editProfile$', views.edit_profile, name='edit_profile'),

    # Librarian verification and admin approval routines.

    # Admin start page:
    url(r'^admin_start$', views.admin_start, name='admin_start'),

    # Location verification page:
    url(r'^admin_verify_copy/$', views.admin_verify_copy, name='admin_verify_copy'),
    # ...and ajax call
    url(r'^admin_verify_location_verified$', views.admin_verify_location_verified, name='admin_verify_location_verified'),

    # Edit verification and submission verification pages:
    url(r'^admin_edit_verify$', views.admin_edit_verify, name='admin_edit_verify'),
    url(r'^admin_submission_verify$', views.admin_submission_verify, name='admin_submission_verify'),
    # ...and ajax calls
    url(r'^admin_verify_single_edit_accept/$', views.admin_verify_single_edit_accept, name='admin_verify_single_edit_accept'),
    url(r'^admin_verify_single_edit_reject/$', views.admin_verify_single_edit_reject, name='admin_verify_single_edit_reject'),

    # Librarian-specific verification UI elements:
    url(r'^librarian_start$', views.librarian_start, name='librarian_start'),
    url(r'^librarian_validate1$', views.librarian_validate1, name='librarian_validate1'),
    url(r'^librarian_validate2$', views.librarian_validate2, name='librarian_validate2'),
    url(r'^updatedraftcopy/(?P<id>[0-9]+)/$', views.update_draft_copy, name='update_draft_copy'),

    # url for the ajax view that creates the new draftcopy
    url(r'^create_draftcopy/$',views.create_draftcopy, name='create_draftcopy'),
    url(r'^location_incorrect/$',views.location_incorrect, name='location_incorrect'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
