from django.contrib import admin, auth

from . import models


class UserInlineAdmin(admin.StackedInline):
    model = models.UserDetail


admin.site.unregister(auth.get_user_model())


@admin.register(auth.get_user_model())
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ["username", "userdetail"]
    inlines = (UserInlineAdmin,)


class CanonicalCopyInline(admin.StackedInline):
    model = models.CanonicalCopy
    fields = ("issue",)
    readonly_fields = ("issue",)
    show_change_link = True
    extra = 0


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    ordering = ("name",)
    inlines = (CanonicalCopyInline,)


@admin.register(models.StaticPageText)
class StaticPageTextAdmin(admin.ModelAdmin):
    pass


### Provenance tables


class ProvenanceOwnershipInline(admin.TabularInline):
    model = models.ProvenanceOwnership
    autocomplete_fields = ("copy", "owner")
    extra = 1


@admin.register(models.ProvenanceName)
class ProvenanceNameAdmin(admin.ModelAdmin):
    ordering = ("name",)
    search_fields = ("name",)
    inlines = (ProvenanceOwnershipInline,)


@admin.register(models.ProvenanceOwnership)
class ProvenanceOwnershipAdmin(admin.ModelAdmin):
    autocomplete_fields = ("copy", "owner")


# Higher-level FRBR categories:


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    ordering = ("title",)


@admin.register(models.Issue)
class IssueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Edition)
class EditionAdmin(admin.ModelAdmin):
    pass


# Copy tables:


@admin.register(models.CanonicalCopy)
class CanonicalCopyAdmin(admin.ModelAdmin):
    inlines = (ProvenanceOwnershipInline,)
    search_fields = ("NSC", "issue__edition__title__title")


admin.site.register(models.FalseCopy)
admin.site.register(models.BaseCopy)


@admin.register(models.DraftCopy)
class DraftCopyAdmin(admin.ModelAdmin):
    raw_id_fields = ("parent",)


@admin.register(models.HistoryCopy)
class HistoryCopyAdmin(admin.ModelAdmin):
    raw_id_fields = ("parent",)
