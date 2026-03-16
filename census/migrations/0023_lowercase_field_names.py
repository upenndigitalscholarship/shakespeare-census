# Manual migration to rename fields to lowercase (conditionally)
# Uses SeparateDatabaseAndState to update Django's state tracking

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("census", "0022_auto_20181105_2104"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # Edition model fields
                migrations.RenameField(
                    model_name="edition",
                    old_name="Edition_number",
                    new_name="edition_number",
                ),
                migrations.RenameField(
                    model_name="edition",
                    old_name="Edition_format",
                    new_name="edition_format",
                ),
                # Issue model fields
                migrations.RenameField(
                    model_name="issue",
                    old_name="STC_Wing",
                    new_name="stc_wing",
                ),
                migrations.RenameField(
                    model_name="issue",
                    old_name="ESTC",
                    new_name="estc",
                ),
                migrations.RenameField(
                    model_name="issue",
                    old_name="DEEP",
                    new_name="deep",
                ),
                migrations.RenameField(
                    model_name="issue",
                    old_name="Variant_Description",
                    new_name="variant_description",
                ),
                # BaseCopy model fields
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="thumbnail_URL",
                    new_name="thumbnail_url",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="NSC",
                    new_name="nsc",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Shelfmark",
                    new_name="shelfmark",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Height",
                    new_name="height",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Width",
                    new_name="width",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Marginalia",
                    new_name="marginalia",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Condition",
                    new_name="condition",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Binding",
                    new_name="binding",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Binder",
                    new_name="binder",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Bookplate",
                    new_name="bookplate",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Bookplate_Location",
                    new_name="bookplate_location",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Bartlett1939",
                    new_name="bartlett1939",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Bartlett1939_Notes",
                    new_name="bartlett1939_notes",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Bartlett1916",
                    new_name="bartlett1916",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Bartlett1916_Notes",
                    new_name="bartlett1916_notes",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Lee_Notes",
                    new_name="lee_notes",
                ),
                migrations.RenameField(
                    model_name="basecopy",
                    old_name="Local_Notes",
                    new_name="local_notes",
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql=[
                        # Edition model fields
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_edition' AND column_name='Edition_number') THEN
                                ALTER TABLE census_edition RENAME COLUMN "Edition_number" TO edition_number;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_edition' AND column_name='Edition_format') THEN
                                ALTER TABLE census_edition RENAME COLUMN "Edition_format" TO edition_format;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        # Issue model fields
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_issue' AND column_name='STC_Wing') THEN
                                ALTER TABLE census_issue RENAME COLUMN "STC_Wing" TO stc_wing;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_issue' AND column_name='ESTC') THEN
                                ALTER TABLE census_issue RENAME COLUMN "ESTC" TO estc;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_issue' AND column_name='DEEP') THEN
                                ALTER TABLE census_issue RENAME COLUMN "DEEP" TO deep;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_issue' AND column_name='Variant_Description') THEN
                                ALTER TABLE census_issue RENAME COLUMN "Variant_Description" TO variant_description;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        # BaseCopy model fields
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='thumbnail_URL') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "thumbnail_URL" TO thumbnail_url;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='NSC') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "NSC" TO nsc;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Shelfmark') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Shelfmark" TO shelfmark;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Height') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Height" TO height;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Width') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Width" TO width;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Marginalia') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Marginalia" TO marginalia;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Condition') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Condition" TO condition;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Binding') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Binding" TO binding;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Binder') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Binder" TO binder;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Bookplate') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Bookplate" TO bookplate;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Bookplate_Location') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Bookplate_Location" TO bookplate_location;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Bartlett1939') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Bartlett1939" TO bartlett1939;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Bartlett1939_Notes') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Bartlett1939_Notes" TO bartlett1939_notes;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Bartlett1916') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Bartlett1916" TO bartlett1916;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Bartlett1916_Notes') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Bartlett1916_Notes" TO bartlett1916_notes;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Lee_Notes') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Lee_Notes" TO lee_notes;
                            END IF;
                        END $$;""",
                            None,
                        ),
                        (
                            """DO $$ BEGIN
                            IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='census_basecopy' AND column_name='Local_Notes') THEN
                                ALTER TABLE census_basecopy RENAME COLUMN "Local_Notes" TO local_notes;
                            END IF;
                        END $$;""",
                            None,
                        ),
                    ],
                    reverse_sql=[
                        (
                            'ALTER TABLE census_edition RENAME COLUMN edition_number TO "Edition_number"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_edition RENAME COLUMN edition_format TO "Edition_format"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_issue RENAME COLUMN stc_wing TO "STC_Wing"',
                            None,
                        ),
                        ('ALTER TABLE census_issue RENAME COLUMN estc TO "ESTC"', None),
                        ('ALTER TABLE census_issue RENAME COLUMN deep TO "DEEP"', None),
                        (
                            'ALTER TABLE census_issue RENAME COLUMN variant_description TO "Variant_Description"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN thumbnail_url TO "thumbnail_URL"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN nsc TO "NSC"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN shelfmark TO "Shelfmark"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN height TO "Height"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN width TO "Width"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN marginalia TO "Marginalia"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN condition TO "Condition"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN binding TO "Binding"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN binder TO "Binder"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN bookplate TO "Bookplate"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN bookplate_location TO "Bookplate_Location"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN bartlett1939 TO "Bartlett1939"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN bartlett1939_notes TO "Bartlett1939_Notes"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN bartlett1916 TO "Bartlett1916"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN bartlett1916_notes TO "Bartlett1916_Notes"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN lee_notes TO "Lee_Notes"',
                            None,
                        ),
                        (
                            'ALTER TABLE census_basecopy RENAME COLUMN local_notes TO "Local_Notes"',
                            None,
                        ),
                    ],
                ),
            ],
        ),
    ]
