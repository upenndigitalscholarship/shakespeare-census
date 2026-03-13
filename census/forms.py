from django import forms
from .models import *


class ContactUs(forms.ModelForm):
    choices =(("General feedback", "General feedback"),
    ("I found an error in the data", "I found an error in the data"),
    ("I'd like to suggest a new feature", "I'd like to suggest a new feature"),
    ("I have a copy that should be in your database", "I have a copy that should be in your database"))

    subject=forms.ChoiceField(choices=choices)
    guardian=forms.CharField(widget=forms.Textarea(attrs={'class': 'guardian'}), required=False, label='')

    class Meta:
        model = ContactForm
        fields = '__all__'

_submission_field_order = [
    'location', 'shelfmark', 'prov_info', 'marginalia', 'binding',
    'binder', 'bookplate', 'bookplate_location', 'local_notes',
    'height', 'width']

class LibrarianCopySubmissionForm(forms.ModelForm):
    shelfmark = forms.CharField(label="Shelfmark", required=True)
    prov_info = forms.CharField(label="Provenance Information", widget=forms.Textarea, required=False)
    marginalia = forms.CharField(label="Marginalia", widget=forms.Textarea, required=False)
    binding = forms.CharField(label="Binding", required=False)
    binder = forms.CharField(label="Binder", required=False)
    bookplate = forms.CharField(label="Bookplate", required=False)
    bookplate_location = forms.CharField(label="Bookplate Location", required=False)
    local_notes = forms.CharField(label="Other Copy-specific Details", widget=forms.Textarea, required=False)
    height = forms.DecimalField(label="Height (cm)", initial=0, required=False)
    width = forms.DecimalField(label="Width (cm)", initial=0, required=False)

    field_order = _submission_field_order[1:]
    class Meta:
        model = DraftCopy
        fields = _submission_field_order[1:]

class AdminCopySubmissionForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.order_by('name'), required=True)
    shelfmark = forms.CharField(label="Shelfmark", required=True)
    prov_info = forms.CharField(label="Provenance Information", widget=forms.Textarea, required=False)
    marginalia = forms.CharField(label="Marginalia", widget=forms.Textarea, required=False)
    binding = forms.CharField(label="Binding", required=False)
    binder = forms.CharField(label="Binder", required=False)
    bookplate = forms.CharField(label="Bookplate", required=False)
    bookplate_location = forms.CharField(label="Bookplate Location", required=False)
    local_notes = forms.CharField(label="Other Copy-specific Details", widget=forms.Textarea, required=False)
    height = forms.DecimalField(label="Height (cm)", initial=0, required=False)
    width = forms.DecimalField(label="Width (cm)", initial=0, required=False)

    field_order = _submission_field_order
    class Meta:
        model = CanonicalCopy
        fields = _submission_field_order

