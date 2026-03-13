# Manual migration to rename additional fields to lowercase

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0023_lowercase_field_names'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                ("ALTER TABLE census_basecopy RENAME COLUMN \"Digital_Facsimile_URL\" TO digital_facsimile_url", None),
                ("ALTER TABLE census_basecopy RENAME COLUMN \"Bartlett_MS_Annotations\" TO bartlett_ms_annotations", None),
            ],
            reverse_sql=[
                ("ALTER TABLE census_basecopy RENAME COLUMN digital_facsimile_url TO \"Digital_Facsimile_URL\"", None),
                ("ALTER TABLE census_basecopy RENAME COLUMN bartlett_ms_annotations TO \"Bartlett_MS_Annotations\"", None),
            ],
        ),
    ]
