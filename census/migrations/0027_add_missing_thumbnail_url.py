# Add missing thumbnail_url column

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("census", "0026_delete_contactform"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='thumbnail_url') THEN
                    ALTER TABLE census_basecopy ADD COLUMN thumbnail_url VARCHAR(500) NULL;
                END IF;
            END $$;""",
            reverse_sql="""ALTER TABLE census_basecopy DROP COLUMN IF EXISTS thumbnail_url;""",
        ),
    ]
