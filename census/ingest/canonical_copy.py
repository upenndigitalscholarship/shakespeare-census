
from django.db import models
import inspect
from census.models import Copy, CanonicalCopy, FalseCopy, BaseCopy, Location



def export_old_copies():
    old_copies = Copy.objects.filter(is_parent=True)
    _export(old_copies, CanonicalCopy)

def export_false_copies():
    false_copies = Copy.objects.filter(is_parent=False)
    _export(false_copies, FalseCopy)

def _export(copies, model):
    base_copy_fields = set(f.name for f in BaseCopy._meta.get_fields())
    base_copy_fields &= set(f.name for f in Copy._meta.get_fields())

    base_copy_fields.discard('id')
    base_copy_fields.discard('pk')
    base_copy_fields.discard('created_by')

    for copy in copies:
        new_copy = model()
        for f in base_copy_fields:
            setattr(new_copy, f, getattr(copy, f))
        owner = copy.Owner
        location = Location.objects.filter(name=owner).first()
        if location is None:
            location = Location(name=owner)
            location.save()
        new_copy.location = location
        new_copy.save()
