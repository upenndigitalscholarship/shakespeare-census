from django.contrib import admin, auth
from django.conf import settings

from . import models


class UserInlineAdmin(admin.StackedInline):
    model = models.UserDetail 

admin.site.unregister(auth.get_user_model())
@admin.register(auth.get_user_model())
class UserDetailAdmin(admin.ModelAdmin):
    inlines = (UserInlineAdmin,)

@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(models.StaticPageText)
admin.site.register(models.ContactForm)

# Higher-level FRBR categories:

@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    ordering = ('title',)
admin.site.register(models.Issue)
admin.site.register(models.Edition)

# Copy tables:

admin.site.register(models.CanonicalCopy)
admin.site.register(models.FalseCopy)
admin.site.register(models.BaseCopy)
@admin.register(models.DraftCopy)
class DraftCopyAdmin(admin.ModelAdmin):
    raw_id_fields = ("parent",)

@admin.register(models.HistoryCopy)
class HistoryCopyAdmin(admin.ModelAdmin):
    raw_id_fields = ("parent",)

### The below are all unused currently.

# admin.site.register(BookPlate)
# admin.site.register(BookPlate_Location)
# admin.site.register(Transfer)
# admin.site.register(Transfer_Value)
# admin.site.register(Provenance)
# admin.site.register(CanonicalCopyAdmin)
