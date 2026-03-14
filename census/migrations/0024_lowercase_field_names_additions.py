# Manual migration to rename additional fields to lowercase

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("census", "0023_lowercase_field_names"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                # Conditionally rename only if old-style column exists (production DB had these manually added)
                (
                    """DO $$ BEGIN
                    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Digital_Facsimile_URL') THEN
                        ALTER TABLE census_basecopy RENAME COLUMN "Digital_Facsimile_URL" TO digital_facsimile_url;
                    END IF;
                END $$;""",
                    None,
                ),
                (
                    """DO $$ BEGIN
                    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Bartlett_MS_Annotations') THEN
                        ALTER TABLE census_basecopy RENAME COLUMN "Bartlett_MS_Annotations" TO bartlett_ms_annotations;
                    END IF;
                END $$;""",
                    None,
                ),
            ],
            reverse_sql=[
                (
                    'ALTER TABLE census_basecopy RENAME COLUMN digital_facsimile_url TO "Digital_Facsimile_URL"',
                    None,
                ),
                (
                    'ALTER TABLE census_basecopy RENAME COLUMN bartlett_ms_annotations TO "Bartlett_MS_Annotations"',
                    None,
                ),
            ],
        ),
    ]
