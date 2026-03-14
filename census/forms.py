from django import forms
from .models import CanonicalCopy, DraftCopy, Location


_submission_field_order = [
    "location",
    "shelfmark",
    "prov_info",
    "marginalia",
    "binding",
    "binder",
    "bookplate",
    "bookplate_location",
    "local_notes",
    "height",
    "width",
]


class LibrarianCopySubmissionForm(forms.ModelForm):
    shelfmark = forms.CharField(label="Shelfmark", required=True)
    prov_info = forms.CharField(
        label="Provenance Information", widget=forms.Textarea, required=False
    )
    marginalia = forms.CharField(
        label="Marginalia", widget=forms.Textarea, required=False
    )
    binding = forms.CharField(label="Binding", required=False)
    binder = forms.CharField(label="Binder", required=False)
    bookplate = forms.CharField(label="Bookplate", required=False)
    bookplate_location = forms.CharField(label="Bookplate Location", required=False)
    local_notes = forms.CharField(
        label="Other Copy-specific Details", widget=forms.Textarea, required=False
    )
    height = forms.DecimalField(label="Height (cm)", initial=0, required=False)
    width = forms.DecimalField(label="Width (cm)", initial=0, required=False)

    field_order = _submission_field_order[1:]

    class Meta:
        model = DraftCopy
        fields = _submission_field_order[1:]


class AdminCopySubmissionForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=Location.objects.order_by("name"), required=True
    )
    shelfmark = forms.CharField(label="Shelfmark", required=True)
    prov_info = forms.CharField(
        label="Provenance Information", widget=forms.Textarea, required=False
    )
    marginalia = forms.CharField(
        label="Marginalia", widget=forms.Textarea, required=False
    )
    binding = forms.CharField(label="Binding", required=False)
    binder = forms.CharField(label="Binder", required=False)
    bookplate = forms.CharField(label="Bookplate", required=False)
    bookplate_location = forms.CharField(label="Bookplate Location", required=False)
    local_notes = forms.CharField(
        label="Other Copy-specific Details", widget=forms.Textarea, required=False
    )
    height = forms.DecimalField(label="Height (cm)", initial=0, required=False)
    width = forms.DecimalField(label="Width (cm)", initial=0, required=False)

    field_order = _submission_field_order

    class Meta:
        model = CanonicalCopy
        fields = _submission_field_order
