from csvexport.actions import csvexport
from django.contrib import admin, auth

from . import models


class CSVExportModelAdmin(admin.ModelAdmin):
    """Make all census records available through the admin CSV export action."""

    actions = [csvexport]


class UserInlineAdmin(admin.StackedInline):
    model = models.UserDetail


admin.site.unregister(auth.get_user_model())


@admin.register(auth.get_user_model())
class UserDetailAdmin(CSVExportModelAdmin):
    list_display = ["username", "userdetail"]
    inlines = (UserInlineAdmin,)


class CanonicalCopyInline(admin.StackedInline):
    model = models.CanonicalCopy
    fields = ("issue",)
    readonly_fields = ("issue",)
    show_change_link = True
    extra = 0


@admin.register(models.UserProfile)
class UserProfileAdmin(CSVExportModelAdmin):
    pass


@admin.register(models.UserDetail)
class UserDetailRecordAdmin(CSVExportModelAdmin):
    pass


@admin.register(models.Location)
class LocationAdmin(CSVExportModelAdmin):
    ordering = ("name",)
    inlines = (CanonicalCopyInline,)


@admin.register(models.StaticPageText)
class StaticPageTextAdmin(CSVExportModelAdmin):
    pass


### Provenance tables


class ProvenanceOwnershipInline(admin.TabularInline):
    model = models.ProvenanceOwnership
    autocomplete_fields = ("copy", "owner")
    extra = 1


@admin.register(models.ProvenanceName)
class ProvenanceNameAdmin(CSVExportModelAdmin):
    ordering = ("name",)
    search_fields = ("name",)
    inlines = (ProvenanceOwnershipInline,)


@admin.register(models.ProvenanceOwnership)
class ProvenanceOwnershipAdmin(CSVExportModelAdmin):
    autocomplete_fields = ("copy", "owner")


# Higher-level FRBR categories:


@admin.register(models.Title)
class TitleAdmin(CSVExportModelAdmin):
    ordering = ("title",)


@admin.register(models.Issue)
class IssueAdmin(CSVExportModelAdmin):
    pass


@admin.register(models.Edition)
class EditionAdmin(CSVExportModelAdmin):
    pass


# Copy tables:


@admin.register(models.CanonicalCopy)
class CanonicalCopyAdmin(CSVExportModelAdmin):
    inlines = (ProvenanceOwnershipInline,)
    search_fields = ("NSC", "issue__edition__title__title")


@admin.register(models.FalseCopy)
class FalseCopyAdmin(CSVExportModelAdmin):
    pass


@admin.register(models.BaseCopy)
class BaseCopyAdmin(CSVExportModelAdmin):
    pass


@admin.register(models.DraftCopy)
class DraftCopyAdmin(CSVExportModelAdmin):
    raw_id_fields = ("parent",)


@admin.register(models.HistoryCopy)
class HistoryCopyAdmin(CSVExportModelAdmin):
    raw_id_fields = ("parent",)


@admin.register(models.RejectedDraftCopy)
class RejectedDraftCopyAdmin(CSVExportModelAdmin):
    raw_id_fields = ("parent",)


@admin.register(models.CopyForm)
class CopyFormAdmin(CSVExportModelAdmin):
    pass
