# Manual migration to rename fields to lowercase

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0022_auto_20181105_2104'),
    ]

    operations = [
        # Edition model fields
        migrations.RenameField(
            model_name='edition',
            old_name='Edition_number',
            new_name='edition_number',
        ),
        migrations.RenameField(
            model_name='edition',
            old_name='Edition_format',
            new_name='edition_format',
        ),
        # Issue model fields
        migrations.RenameField(
            model_name='issue',
            old_name='STC_Wing',
            new_name='stc_wing',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='ESTC',
            new_name='estc',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='DEEP',
            new_name='deep',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='Variant_Description',
            new_name='variant_description',
        ),
        # BaseCopy model fields
        migrations.RenameField(
            model_name='basecopy',
            old_name='thumbnail_URL',
            new_name='thumbnail_url',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='NSC',
            new_name='nsc',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Shelfmark',
            new_name='shelfmark',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Height',
            new_name='height',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Width',
            new_name='width',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Marginalia',
            new_name='marginalia',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Condition',
            new_name='condition',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Binding',
            new_name='binding',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Binder',
            new_name='binder',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Bookplate',
            new_name='bookplate',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Bookplate_Location',
            new_name='bookplate_location',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Bartlett1939',
            new_name='bartlett1939',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Bartlett1939_Notes',
            new_name='bartlett1939_notes',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Bartlett1916',
            new_name='bartlett1916',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Bartlett1916_Notes',
            new_name='bartlett1916_notes',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Lee_Notes',
            new_name='lee_notes',
        ),
        migrations.RenameField(
            model_name='basecopy',
            old_name='Local_Notes',
            new_name='local_notes',
        ),
    ]
