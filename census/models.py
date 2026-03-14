from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

# from tinymce import models as tinymce_models

### Main Site Operations ###


class Location(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super().delete(*args, **kwargs)


class UserDetail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    affiliation_str = models.CharField(
        max_length=255, default="", null=True, blank=True
    )
    affiliation = models.ForeignKey(
        Location, on_delete=models.CASCADE, unique=False, null=True, blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, default=None, null=True, blank=True
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "user details"


"""
class LibrarianEmail(models.Model):
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural = "trusted emails"
"""


class StaticPageText(models.Model):
    content = models.TextField(null=True, blank=True, default=None)
    # htmlcontent = tinymce_models.HTMLField()
    viewname = models.CharField(max_length=255, default="", null=True, blank=True)

    def __str__(self):
        return self.viewname

    class Meta:
        verbose_name_plural = "Static Pages"


@receiver(post_save, sender=User)
def create_user_detail(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)


### Core Data Tables ###


class Title(models.Model):
    title = models.CharField(max_length=128, unique=True)
    apocryphal = models.BooleanField(default=False)
    image = models.CharField(max_length=500, null=True, blank=True)
    hidden = models.BooleanField(default=False)
    issue = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Edition(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    edition_number = models.CharField(
        max_length=20, unique=False, null=True, blank=True
    )
    edition_format = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.title} Edition {self.edition_number}"


class Issue(models.Model):
    edition = models.ForeignKey(Edition, unique=False, on_delete=models.CASCADE)
    stc_wing = models.CharField(max_length=20)
    estc = models.CharField(max_length=20)
    year = models.CharField(max_length=20, default=None)
    start_date = models.IntegerField(default=0)
    end_date = models.IntegerField(default=0)
    deep = models.CharField(max_length=20, default="", null=True, blank=True)
    notes = models.TextField(null=True, blank=True, default=None)
    variant_description = models.CharField(max_length=1000, null=True, blank=True)

    def estc_as_list(self):
        estc_list = self.estc.split("; ")
        return [(estc, (i + 1) == len(estc_list)) for i, estc in enumerate(estc_list)]

    def deep_as_list(self):
        deep_list = self.deep.split("; ")
        return [(deep, (i + 1) == len(deep_list)) for i, deep in enumerate(deep_list)]

    def __str__(self):
        return f"{self.edition} ESTC {self.estc}"


# Essential fields for all copies.
class BaseCopy(models.Model):
    location = models.ForeignKey(
        Location, unique=False, null=True, blank=True, on_delete=models.CASCADE
    )
    issue = models.ForeignKey(Issue, unique=False, on_delete=models.CASCADE)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    digital_facsimile_url = models.URLField(max_length=500, null=True, blank=True)
    nsc = models.CharField(max_length=40, default="", null=True, blank=True)
    shelfmark = models.CharField(max_length=500, default=None, null=True, blank=True)
    height = models.FloatField(default=0, null=True)
    width = models.FloatField(default=0, null=True)
    marginalia = models.TextField(null=True, blank=True, default=None)
    condition = models.CharField(max_length=500, default=None, null=True, blank=True)
    binding = models.CharField(max_length=500, default=None, null=True, blank=True)
    binder = models.CharField(max_length=500, default=None, null=True, blank=True)
    bookplate = models.CharField(max_length=500, default=None, null=True, blank=True)
    bookplate_location = models.CharField(
        max_length=500, default=None, null=True, blank=True
    )
    bartlett1939 = models.IntegerField(default=0, null=True)
    bartlett1939_notes = models.TextField(null=True, blank=True, default=None)
    bartlett1916 = models.IntegerField(default=0, null=True)
    bartlett1916_notes = models.TextField(null=True, blank=True, default=None)
    bartlett_ms_annotations = models.TextField(null=True, blank=True, default=None)
    lee = models.IntegerField(default=0, null=True, blank=True)
    lee_notes = models.TextField(null=True, blank=True, default=None)
    rasmussen_west = models.IntegerField(default=0, null=True, blank=True)
    rasmussen_west_notes = models.TextField(null=True, blank=True, default=None)
    local_notes = models.TextField(null=True, blank=True, default=None)
    in_early_sammelband = models.BooleanField(default=False)
    fragment = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_submitted_copies",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    prov_info = models.TextField(null=True, blank=True, default=None)
    bibliography = models.TextField(null=True, blank=True, default=None)
    from_estc = models.BooleanField(default=False)
    location_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.issue} ({self.issue.year})"

    class Meta:
        verbose_name_plural = "Base copies"


# Copy records that have been ruled spurious. These records should
# be preserved across versions of the app if possible.
class FalseCopy(BaseCopy):
    class Meta:
        verbose_name_plural = "False copies"


# Copy records that we are treating as accurate. These records *must*
# be preserved across versions of the app.
class CanonicalCopy(BaseCopy):
    class Meta:
        verbose_name_plural = "Canonical copies"


# Copy records that are modified versions of records from CanonicalCopy.
# These are working records and historical versions that we don't treat
# as vital for preservation.
class DraftCopy(BaseCopy):
    parent = models.ForeignKey(
        CanonicalCopy,
        related_name="drafts",
        default=None,
        null=True,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Draft copies"


class HistoryCopy(BaseCopy):
    parent = models.ForeignKey(
        CanonicalCopy,
        related_name="versions",
        default=None,
        null=True,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "History copies"


# Copy records that were rejected from draft review.
class RejectedDraftCopy(BaseCopy):
    parent = models.ForeignKey(
        CanonicalCopy,
        related_name="rejected_drafts",
        default=None,
        null=True,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Rejected draft copies"


### Provenance ###


class ProvenanceName(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    viaf = models.CharField(max_length=255, null=True, blank=True)
    start_century = models.CharField(max_length=255, null=True, blank=True)
    end_century = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name_plural = "Provenance names"


class ProvenanceOwnership(models.Model):
    copy = models.ForeignKey(CanonicalCopy, on_delete=models.CASCADE)
    owner = models.ForeignKey(ProvenanceName, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Provenance ownerships"


### Forms ###


class CopyForm(models.Model):
    shelfmark = models.CharField(max_length=500, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    rasmussen_west = models.IntegerField(null=True, blank=True)
    rasmussen_west_notes = models.TextField(null=True, blank=True)
    prov_info = models.TextField(null=True, blank=True)
    marginalia = models.TextField(null=True, blank=True)
    binding = models.CharField(max_length=500, null=True, blank=True)
    binder = models.CharField(max_length=500, null=True, blank=True)
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Copy forms"


### Copy Management Classes/Callables ###


class LinkedCopyCreate:
    def __init__(self, source_model, target_model, base_model):
        self.source_model = source_model
        self.target_model = target_model
        self.base_model = base_model
        self.copy_fields = {f.name for f in base_model._meta.fields}
        self.copy_fields.discard("id")
        self.copy_fields.discard("pk")

    def __call__(self, source):
        if not isinstance(source, self.source_model):
            raise ValueError(f"Can only copy instances of {self.source_model}")
        new = self.target_model()
        for f in self.copy_fields:
            setattr(new, f, getattr(source, f))
        new.parent = source
        new.save()
        return new


create_draft = LinkedCopyCreate(CanonicalCopy, DraftCopy, BaseCopy)
create_history = LinkedCopyCreate(CanonicalCopy, HistoryCopy, BaseCopy)


class LinkedCopyUpdate:
    def __init__(self, source_model, target_model, record_model, base_model):
        self.source_model = source_model
        self.target_model = target_model
        self.record_model = record_model
        self.base_model = base_model
        self.create_record = LinkedCopyCreate(target_model, record_model, base_model)
        self.copy_fields = {f.name for f in base_model._meta.fields}
        self.copy_fields.discard("id")
        self.copy_fields.discard("pk")

    def __call__(self, source):
        if not isinstance(source, self.source_model):
            raise ValueError(f"Can only update from instances of {self.source_model}")
        if not isinstance(source.parent, self.target_model):
            raise ValueError(
                "Can only update to instances of {}, but the parent of {} is a {}".format(
                    self.target_model, source, type(source.parent)
                )
            )
        parent = source.parent
        print(parent.id)
        print(source.id)
        self.create_record(parent)
        for f in self.copy_fields:
            setattr(parent, f, getattr(source, f))
        print(parent.id)
        print(source.id)

        parent.save()
        source.delete()


draft_to_canonical_update = LinkedCopyUpdate(
    DraftCopy, CanonicalCopy, HistoryCopy, BaseCopy
)
history_to_canonical_update = LinkedCopyUpdate(
    HistoryCopy, CanonicalCopy, DraftCopy, BaseCopy
)


class LinkedCopyCreateParent:
    def __init__(self, source_model, target_model, base_model):
        self.source_model = source_model
        self.target_model = target_model
        self.base_model = base_model
        self.copy_fields = {f.name for f in base_model._meta.fields}
        self.copy_fields.discard("id")
        self.copy_fields.discard("pk")

    def __call__(self, source):
        if not isinstance(source, self.source_model):
            raise ValueError(f"Can only copy instances of {self.source_model}")
        if source.parent:
            raise ValueError("Can only create parents for objects that don't have one!")
        new = self.target_model()
        for f in self.copy_fields:
            setattr(new, f, getattr(source, f))
        new.save()
        source.delete()


draft_to_canonical_create = LinkedCopyCreateParent(DraftCopy, CanonicalCopy, BaseCopy)


class ParentCopyMove:
    def __init__(self, source_model, target_model, base_model):
        self.source_model = source_model
        self.target_model = target_model
        self.base_model = base_model
        self.copy_fields = {f.name for f in base_model._meta.fields}
        self.copy_fields.discard("id")
        self.copy_fields.discard("pk")

    def __call__(self, source):
        if not isinstance(source, self.source_model):
            raise ValueError(f"Can only copy instances of {self.source_model}")
        new = self.target_model()
        for f in self.copy_fields:
            setattr(new, f, getattr(source, f))
        new.save()
        source.delete()


canonical_to_fp_move = ParentCopyMove(CanonicalCopy, FalseCopy, BaseCopy)
