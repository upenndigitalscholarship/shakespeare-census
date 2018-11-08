import os
import codecs
from census import models
from django.core.serializers import serialize, deserialize
from django.contrib import auth
from django.db.utils import ProgrammingError
from django.db import connection


# This defines the primary backup dataset. There are lots of
# other tables, but we regard all of them as containing ephemeral
# data subject to loss at any time. *This* data is unrecoverable
# if lost, and is therefore the first priority for backups. It
# should be saved to files tracked by version control -- the
# quantity will never be so large that it won't fit in a
# standard GitHub repository.

_canonical_models = [
    ('locations', models.Location),
    ('titles', models.Title),
    ('editions', models.Edition),
    ('issues', models.Issue),
    ('basecopies', models.BaseCopy),
    ('canonicalcopies', models.CanonicalCopy),
    ('falsecopies', models.FalseCopy),
    ('draftcopies', models.DraftCopy),
    ('historycopies', models.HistoryCopy),
    ('statictext', models.StaticPageText),
]

_user_models = [
    ('user', auth.get_user_model()),
    ('userdetail', models.UserDetail),
]

def check_filename(f):
    new_f = f
    if os.path.exists(f):
        n = 1
        new_f, ext = os.path.splitext(f)
        new_f_template = new_f + '-{}{}'
        new_f = new_f_template.format(n, ext)
        while os.path.exists(new_f):
            n += 1
            new_f = new_f_template.format(n, ext)
    return new_f

def export_query_json(filename, queryset):
    data = serialize('json', queryset)

    filename = check_filename(filename)
    with codecs.open(filename, 'w', encoding='utf-8') as op:
        op.write(data)

def import_query_json(filename, model):
    with codecs.open(filename, 'r', encoding='utf-8') as ip:
        data = ip.read()

    for row in deserialize('json', data):
        row.save()

    try:
        table = model._meta.db_table
        cur = connection.cursor()
        cur.execute("SELECT setval('{}_id_seq', (SELECT max(id) FROM {}))".format(table, table))
    except ProgrammingError:
        pass

def export_modelset_json(modelset, filename_base):
    for name, model in modelset:
        filename = '{}_{}.json'.format(filename_base, name)
        export_query_json(filename, model)

def import_modelset_json(modelset, filename_base):
    canonical_models = [('{}_{}.json'.format(filename_base, name), model)
                        for name, model in modelset]
    if all(os.path.isfile(filename) for filename, model in canonical_models):
        for filename, model in canonical_models:
            import_query_json(filename, model)
    else:
        print("couldn't find backup files")

def export_canon_json(filename_base='backup'):
    export_modelset_json(_canonical_models, filename_base)

def import_canon_json(filename_base='backup'):
    import_modelset_json(_canonical_models, filename_base)

def export_user_json(filename_base='_user_backup'):
    export_modelset_json(_user_models, filename_base)

def import_user_json(filename_base='_user_backup'):
    import_modelset_json(_user_models, filename_base)


