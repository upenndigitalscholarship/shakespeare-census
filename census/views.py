from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template import loader
from . import models
from . import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime
from string import Formatter
import csv


## UTILITY FUNCTIONS ##
# Eventually these should be moved into a separate util module.
def get_or_create_draft(selected_copy):
    assert selected_copy.drafts.count() < 2, (
        "There should not be more than one Draft copy"
    )
    if not selected_copy.drafts.exists():
        models.create_draft(selected_copy)

    draft_copy = selected_copy.drafts.get()
    return draft_copy


def get_draft_if_exists(selected_copy):
    if not selected_copy.drafts.exists():
        return selected_copy
    else:
        return selected_copy.drafts.get()


def search_sort_date(copy):
    return (
        copy_date_sort_key(copy),
        title_sort_key(copy.issue.edition.title),
        copy_location_sort_key(copy),
    )


def search_sort_title(copy):
    return (
        title_sort_key(copy.issue.edition.title),
        copy_date_sort_key(copy),
        copy_location_sort_key(copy),
    )


def search_sort_location(copy):
    return (
        copy_location_sort_key(copy),
        copy_date_sort_key(copy),
        title_sort_key(copy.issue.edition.title),
    )


def search_sort_stc(copy):
    return (copy.issue.stc_wing, copy_location_sort_key(copy))


def copy_date_sort_key(c):
    return int(c.issue.start_date)


def copy_nsc_sort_key(c):
    nsc = c.nsc if c.nsc is not None else ""
    nsc_a = 0
    nsc_b = 0
    try:
        if "." in nsc:
            a, b = nsc.split(".", maxsplit=1)
            nsc_a, nsc_b = int(a), int(b)
        else:
            nsc_a = int(nsc)
    except ValueError:
        pass
    return (nsc_a, nsc_b)


def copy_location_sort_key(c):
    name = c.location.name
    return strip_article(name if name else "")


def copy_shelfmark_sort_key(c):
    sm = c.shelfmark
    return sm if sm else ""


def strip_article(s):
    articles = ["a ", "A ", "an ", "An ", "the ", "The "]
    for a in articles:
        if s.startswith(a):
            return s.replace(a, "", 1)
    else:
        return s


def title_sort_key(title_object):
    title = title_object.title
    if title == "Comedies, Histories, and Tragedies":
        title = " " + title
    if title and title[0].isdigit():
        title = title.split()
        return strip_article(" ".join(title[1:] + [title[0]]))
    else:
        return strip_article(title)


def issue_sort_key(i):
    ed_number = i.edition.edition_number
    ed_idx = int(ed_number) if ed_number.isdigit() else float("inf")
    return (ed_idx, i.stc_wing)


def copy_sort_key(c):
    nsc_a, nsc_b = copy_nsc_sort_key(c)
    return (copy_location_sort_key(c), copy_shelfmark_sort_key(c), nsc_a, nsc_b)


def convert_year_range(year):
    if "-" in year:
        start, end = (n.strip() for n in year.split("-", 1))
        if len(start) == 4 and start.isdigit() and len(end) == 4 and end.isdigit():
            return int(start), int(end)
    elif len(year) == 4 and year.isdigit():
        return int(year), int(year)
    return False


def get_icon_path(id=None):
    if id is None:
        return "census/images/title_icons/generic-title-icon.png"
    else:
        return f"census/images/title_icons/{id}.png"


## VIEW FUNCTIONS ##


def get_collection(copy_list, coll_name):
    if coll_name == "earlyprovenance":
        results = copy_list.filter(provenanceownership__owner__start_century="17")
        display = "Copies with known early provenance (before 1700)"
    elif coll_name == "womanowner":
        results = copy_list.filter(provenanceownership__owner__gender="F")
        display = "Copies with a known woman owner"
    elif coll_name == "earlywomanowner":
        results = copy_list.filter(
            Q(provenanceownership__owner__gender="F")
            & (
                Q(provenanceownership__owner__start_century="17")
                | Q(provenanceownership__owner__start_century="18")
            )
        )
        display = "Copies with a known woman owner before 1800"
    elif coll_name == "marginalia":
        results = copy_list.exclude(Q(marginalia="") | Q(marginalia=None))
        display = "Copies that include marginalia"
    elif coll_name == "earlysammelband":
        results = copy_list.filter(in_early_sammelband=True)
        display = "Copies in an early sammelband"
    else:
        raise Http404("Not found")
    return results, display


def autofill_collection(request, query=None):
    collection = [
        {
            "label": "With known early provenance (before 1700)",
            "value": "earlyprovenance",
        },
        {"label": "With a known woman owner", "value": "womanowner"},
        {"label": "With a known woman owner before 1800", "value": "earlywomanowner"},
        {"label": "Includes marginalia", "value": "marginalia"},
        {"label": "In an early sammelband", "value": "earlysammelband"},
    ]
    return JsonResponse({"matches": collection})


def autofill_location(request, query=None):
    if query is not None:
        location_matches = models.Location.objects.filter(name__icontains=query)
        match_object = {"matches": [m.name for m in location_matches]}
    else:
        match_object = {"matches": []}
    return JsonResponse(match_object)


def autofill_provenance(request, query=None):
    if query is not None:
        prov_matches = models.ProvenanceName.objects.filter(name__icontains=query)
        match_object = {"matches": [m.name for m in prov_matches]}
    else:
        match_object = {"matches": []}
    return JsonResponse(match_object)


def search(request, field=None, value=None, order=None):
    template = loader.get_template("census/search-results.html")
    field = field if field is not None else request.GET.get("field")
    value = value if value is not None else request.GET.get("value")
    order = order if order is not None else request.GET.get("order")
    copy_list = models.CanonicalCopy.objects.all()
    display_field = field
    display_value = value

    if field == "keyword" or field is None and value:
        field = "keyword"
        display_field = "Keyword Search"
        query = (
            Q(marginalia__icontains=value)
            | Q(binding__icontains=value)
            | Q(binder__icontains=value)
            | Q(bookplate__icontains=value)
            | Q(bookplate_location__icontains=value)
            | Q(bartlett1939_notes__icontains=value)
            | Q(bartlett1916_notes__icontains=value)
            | Q(lee_notes__icontains=value)
            | Q(rasmussen_west_notes__icontains=value)
            | Q(local_notes__icontains=value)
            | Q(prov_info__icontains=value)
            | Q(bibliography__icontains=value)
            | Q(provenanceownership__owner__name__icontains=value)
        )
        result_list = copy_list.filter(query)
    elif field == "stc" and value:
        display_field = "STC / Wing"
        result_list = copy_list.filter(issue__stc_wing__icontains=value)
    elif field == "nsc" and value:
        display_field = "SC"
        result_list = copy_list.filter(nsc=value)
    elif field == "year" and value:
        display_field = "Year"
        year_range = convert_year_range(value)
        if year_range:
            start, end = year_range
            result_list = copy_list.filter(
                issue__start_date__lte=end, issue__end_date__gte=start
            )
        else:
            result_list = copy_list.filter(issue__year__icontains=value)
    elif field == "location" and value:
        display_field = "Location"
        result_list = copy_list.filter(location__name__icontains=value)
    elif field == "bartlett" and value:
        display_field = "Bartlett"
        result_list = copy_list.filter(Q(bartlett1916=value) | Q(bartlett1939=value))
    elif field == "provenance_name" and value:
        display_field = "Provenance Name"
        result_list = copy_list.filter(
            provenanceownership__owner__name__icontains=value
        )
    elif field == "unverified":
        display_field = "Unverified"
        display_value = "All"
        result_list = copy_list.filter(location_verified=False)
        if order is None:
            order = "location"
    elif field == "ghosts":
        display_field = "Ghosts"
        display_value = "All"
        result_list = models.FalseCopy.objects.all()
    elif field == "collection":
        result_list, display_field = get_collection(copy_list, value)
        display_value = "All"
    else:
        result_list = models.CanonicalCopy.objects.none()

    result_list = result_list.exclude(issue__edition__title__hidden=True)
    result_list = result_list.distinct()

    if order is None or order == "date":
        result_list = sorted(result_list, key=search_sort_date)
    elif order == "title":
        result_list = sorted(result_list, key=search_sort_title)
    elif order == "location":
        result_list = sorted(result_list, key=search_sort_location)
    elif order == "stc":
        result_list = sorted(result_list, key=search_sort_stc)
    elif order == "sc":
        result_list = sorted(result_list, key=copy_nsc_sort_key)
    else:
        raise Http404("Not found")

    frag_count = sum(c.fragment for c in result_list)

    context = {
        "icon_path": get_icon_path(),
        "value": value,
        "field": field,
        "display_value": display_value,
        "display_field": display_field,
        "result_list": result_list,
        "copy_count": len(result_list) - frag_count,
        "frag_count": frag_count,
    }

    return HttpResponse(template.render(context, request))


def homepage(request):
    template = loader.get_template("census/frontpage.html")
    gridwidth = 5
    titlelist = sorted(models.Title.objects.all(), key=title_sort_key)
    titlerows = [
        titlelist[i : i + gridwidth] for i in range(0, len(titlelist), gridwidth)
    ]
    for row in titlerows:
        for t in row:
            t.icon_path = get_icon_path(t.id)
    context = {
        "frontpage": True,
        "titlelist": titlelist,
        "titlerows": titlerows,
    }
    return HttpResponse(template.render(context, request))


def safe_format(strng, val_dict):
    """
    Call the `format` method of the given template string, passing val_dict
    as the values. But rather than throwing an error when no value is
    supplied for a named field, leave the given field unchanged. All fields
    in the template string must be named fields.
    """
    val_dict = dict(val_dict)  # Will be modified, so make a copy

    names = [
        field
        for literal, field, format_spec, conv in Formatter().parse(strng)
        if field is not None
    ]
    for n in names:
        if n not in val_dict:
            val_dict[n] = "{" + n + "}"

    return strng.format(**val_dict)


def about(request, viewname="about"):
    template = loader.get_template("census/about.html")

    copy_count = models.CanonicalCopy.objects.exclude(
        issue__edition__title__hidden=True
    ).count()
    frag_count = models.CanonicalCopy.objects.filter(fragment=True).count()
    facsimile_copy_count = models.CanonicalCopy.objects.filter(
        ~Q(digital_facsimile_url=None) & ~Q(digital_facsimile_url="")
    ).count()
    facsimile_copy_percent = round(100 * facsimile_copy_count / copy_count)

    verified_copy_count = (
        models.CanonicalCopy.objects.exclude(issue__edition__title__hidden=True)
        .filter(location_verified=True)
        .count()
    )
    unverified_copy_count = (
        models.CanonicalCopy.objects.exclude(issue__edition__title__hidden=True)
        .filter(location_verified=False)
        .count()
    )

    pre_render_context = {
        "copy_count": str(copy_count - frag_count),
        "frag_count": str(frag_count),
        "verified_copy_count": str(verified_copy_count),
        "unverified_copy_count": str(unverified_copy_count),
        "current_date": f"{datetime.now():%d %B %Y}",
        "facsimile_copy_count": str(facsimile_copy_count),
        "facsimile_copy_percent": f"{facsimile_copy_percent}%",
        "estc_copy_count": str(
            models.CanonicalCopy.objects.filter(from_estc=True).count()
        ),
        "non_estc_copy_count": str(
            models.CanonicalCopy.objects.filter(from_estc=False).count()
        ),
    }
    content = [
        safe_format(s.content, pre_render_context)
        for s in models.StaticPageText.objects.filter(viewname=viewname)
    ]

    context = {
        "content": content,
    }
    return HttpResponse(template.render(context, request))


def detail(request, id):
    selected_title = models.Title.objects.get(pk=id)
    if id == "5" or id == "6":
        editions = list(selected_title.edition_set.all())
        extra_ed = list(models.Title.objects.get(pk="39").edition_set.all())
        extra_ed[0].edition_number = "3"
        editions.extend(extra_ed)
    else:
        editions = list(selected_title.edition_set.all())

    issues = [issue for ed in editions for issue in ed.issue_set.all()]
    issues.sort(key=issue_sort_key)
    all_copies = models.CanonicalCopy.objects.filter(
        issue__id__in=[i.id for i in issues]
    )
    copy_count = all_copies.filter(fragment=False).count()
    fragment_count = all_copies.filter(fragment=True).count()
    template = loader.get_template("census/detail.html")
    context = {
        "icon_path": get_icon_path(id),
        "editions": editions,
        "issues": issues,
        "title": selected_title,
        "copy_count": copy_count,
        "fragment_count": fragment_count,
    }
    return HttpResponse(template.render(context, request))


# showing all copies for an issue
def copy(request, id):
    selected_issue = models.Issue.objects.get(pk=id)
    all_copies = models.CanonicalCopy.objects.filter(issue__id=id).order_by(
        "location__name", "shelfmark"
    )
    all_copies = sorted(all_copies, key=copy_sort_key)
    copy_count = len([c for c in all_copies if not c.fragment])
    fragment_count = len([c for c in all_copies if c.fragment])
    template = loader.get_template("census/copy.html")
    context = {
        "all_copies": all_copies,
        "copy_count": copy_count,
        "fragment_count": fragment_count,
        "selected_issue": selected_issue,
        "icon_path": get_icon_path(selected_issue.edition.title.id),
        "title": selected_issue.edition.title,
    }
    return HttpResponse(template.render(context, request))


def draft_copy_data(request, copy_id):
    template = loader.get_template("census/copy_modal.html")
    selected_copy = models.CanonicalCopy.objects.filter(pk=copy_id)
    if selected_copy:
        selected_copy = get_draft_if_exists(selected_copy[0])
    else:
        selected_copy = models.DraftCopy.objects.get(pk=copy_id)

    context = {"copy": selected_copy}

    return HttpResponse(template.render(context, request))


def copy_data(request, copy_id):
    template = loader.get_template("census/copy_modal.html")
    selected_copy = models.CanonicalCopy.objects.get(pk=copy_id)
    context = {"copy": selected_copy}

    return HttpResponse(template.render(context, request))


@login_required()
def add_copy(request, id):
    template = loader.get_template("census/copy_submission.html")
    selected_issue = models.Issue.objects.get(pk=id)

    data = {"issue_id": id, "shelfmark": "", "local_notes": "", "prov_info": ""}
    if request.method == "POST":
        if request.user.is_staff:
            copy_submission_form = forms.AdminCopySubmissionForm(
                request.POST, initial=data
            )
        else:
            copy_submission_form = forms.LibrarianCopySubmissionForm(
                request.POST, initial=data
            )

        if copy_submission_form.is_valid():
            """
            add draft
            linked to canonical_copy
            click to make prefilled word disappear
            move to the next page
            """
            copy = copy_submission_form.save(commit=False)
            copy.location_verified = False
            if not request.user.is_staff:
                copy.location = models.UserDetail.objects.get(
                    user=request.user
                ).affiliation
                copy.location_verified = True
            copy.issue = models.Issue.objects.get(pk=id)
            copy.save()
            return HttpResponseRedirect(reverse("copy", args=(id,)))
    else:
        if request.user.is_staff:
            copy_submission_form = forms.AdminCopySubmissionForm(initial=data)
        else:
            copy_submission_form = forms.LibrarianCopySubmissionForm(initial=data)
    context = {
        "form": copy_submission_form,
        "issue": selected_issue,
        "icon_path": get_icon_path(selected_issue.edition.title.id),
    }

    return HttpResponse(template.render(context, request))


@login_required
def librarian_start(request):
    template = loader.get_template("census/librarian/librarian_start_page.html")
    current_user = request.user
    cur_user_detail = models.UserDetail.objects.get(user=current_user)
    affiliation = cur_user_detail.affiliation

    copy_count = (
        models.CanonicalCopy.objects.all()
        .filter(location=affiliation, location_verified=False)
        .count()
    )
    draft_count = (
        models.DraftCopy.objects.all()
        .filter(
            location=affiliation,
            location_verified=True,
            parent__location_verified=False,
        )
        .count()
    )
    copy_count -= draft_count
    verified_count = (
        models.CanonicalCopy.objects.all()
        .filter(location=affiliation, location_verified=True)
        .count()
    )
    verified_count += draft_count

    context = {
        "affiliation": affiliation.name,
        "copy_count": copy_count,
        "verified_count": verified_count,
    }
    return HttpResponse(template.render(context, request))


def librarian_validate_sort_key(copy):
    return (title_sort_key(copy.issue.edition.title), int(copy.issue.start_date))


@login_required
def librarian_validate1(request):
    template = loader.get_template("census/librarian/librarian_validate1.html")
    current_user = request.user
    cur_user_detail = models.UserDetail.objects.get(user=current_user)
    affiliation = cur_user_detail.affiliation

    # Include all unverified records...
    copy_list = list(
        models.CanonicalCopy.objects.filter(
            location=affiliation, location_verified=False
        )
    )

    print([c.drafts for c in copy_list])
    print([c.drafts.first() for c in copy_list if c.drafts])
    print(
        [
            c.drafts.first().location_verified
            for c in copy_list
            if c.drafts and c.drafts.first()
        ]
    )

    # ...but filter out ones with drafts that have been verified.
    copy_list = [
        c
        for c in copy_list
        if not c.drafts
        or not c.drafts.first()
        or not c.drafts.first().location_verified
    ]

    copy_list = sorted(copy_list, key=librarian_validate_sort_key)
    context = {
        "affiliation": affiliation.name,
        "copies": copy_list,
    }

    return HttpResponse(template.render(context, request))


@login_required
def librarian_validate2(request):
    template = loader.get_template("census/librarian/librarian_validate2.html")
    current_user = request.user
    cur_user_detail = models.UserDetail.objects.get(user=current_user)
    affiliation = cur_user_detail.affiliation

    # Include all verified drafts...
    verified_drafts = models.DraftCopy.objects.filter(
        location=affiliation, location_verified=True
    )
    # And all verified copies...
    verified_copies = models.CanonicalCopy.objects.filter(
        location=affiliation, location_verified=True
    )

    # ...but convert drafts to parents and include only verified copies without drafts.
    all_copies = [d.parent for d in verified_drafts] + [
        c for c in verified_copies if not c.drafts or not c.drafts.first()
    ]

    all_copies = sorted(all_copies, key=librarian_validate_sort_key)
    context = {
        "user_detail": cur_user_detail,
        "affiliation": affiliation.name,
        "child_copies": all_copies,
    }
    return HttpResponse(template.render(context, request))


@login_required()
def update_draft_copy(request, id):
    template = loader.get_template("census/copy_submission.html")
    canonical_copy = models.CanonicalCopy.objects.get(pk=id)
    selected_copy = get_draft_if_exists(canonical_copy)
    init_fields = [
        "shelfmark",
        "local_notes",
        "prov_info",
        "height",
        "width",
        "marginalia",
        "binding",
        "binder",
    ]
    data = {f: getattr(selected_copy, f) for f in init_fields}
    if request.method == "POST":
        copy_form = forms.LibrarianCopySubmissionForm(request.POST)

        if copy_form.is_valid():
            copy_form_data = copy_form.save(commit=False)
            draft_copy = get_or_create_draft(canonical_copy)
            for f in init_fields:
                setattr(draft_copy, f, getattr(copy_form_data, f))
            draft_copy.save()
            return HttpResponseRedirect(reverse("librarian_validate2"))
    else:
        copy_form = forms.LibrarianCopySubmissionForm(initial=data)
        context = {
            "form": copy_form,
            "copy": selected_copy,
            "icon_path": get_icon_path(selected_copy.issue.edition.title.id),
        }
        return HttpResponse(template.render(context, request))


@login_required
def admin_start(request):
    template = loader.get_template("census/staff/admin_start_page.html")
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
def admin_edit_verify(request):
    template = template = loader.get_template("census/staff/admin_edit_verify.html")
    selected_copies = models.DraftCopy.objects.all()
    copies = [
        copy
        for copy in selected_copies
        if copy.parent
        and isinstance(copy.parent, models.CanonicalCopy)
        and copy.parent.location_verified
    ]

    paginator = Paginator(copies, 10)
    page = request.GET.get("page")
    try:
        copies_per_page = paginator.page(page)
    except PageNotAnInteger:
        copies_per_page = paginator.page(1)
    except EmptyPage:
        copies_per_page = paginator.page(paginator.num_pages)

    context = {
        "copies": copies_per_page,
    }
    return HttpResponse(template.render(context, request))


@login_required
def admin_submission_verify(request):
    template = template = loader.get_template(
        "census/staff/admin_submission_verify.html"
    )
    selected_copies = models.DraftCopy.objects.all()
    copies = [copy for copy in selected_copies if not copy.parent]

    paginator = Paginator(copies, 10)
    page = request.GET.get("page")
    try:
        copies_per_page = paginator.page(page)
    except PageNotAnInteger:
        copies_per_page = paginator.page(1)
    except EmptyPage:
        copies_per_page = paginator.page(paginator.num_pages)

    context = {
        "copies": copies_per_page,
    }
    return HttpResponse(template.render(context, request))


@login_required
def admin_verify_single_edit_accept(request):
    try:
        copy_id = request.GET.get("copy_id")
    except OSError:
        print("something wrong with id, may be it does not exist at all?")
    selected_draft_copy = models.DraftCopy.objects.get(pk=copy_id)
    if selected_draft_copy.parent and isinstance(
        selected_draft_copy.parent, models.CanonicalCopy
    ):
        models.draft_to_canonical_update(selected_draft_copy)
    else:
        models.draft_to_canonical_create(selected_draft_copy)

    return HttpResponse("success")


@login_required
def admin_verify_single_edit_reject(request):
    return HttpResponse("success")


@login_required
def admin_verify_location_verified(request):
    template = loader.get_template("census/staff/admin_verify.html")
    selected_copies = models.DraftCopy.objects.all()
    copies = [
        copy
        for copy in selected_copies
        if copy.parent
        and isinstance(copy.parent, models.CanonicalCopy)
        and not copy.parent.location_verified
    ]

    context = {"copies": copies}
    return HttpResponse(template.render(context, request))


# This is for validate old copyx
@login_required()
def admin_verify_copy(request):
    try:
        copy_id = request.GET.get("copy_id")
    except OSError:
        print("something wrong with id, may be it does not exist at all?")
    selected_draft_copy = models.DraftCopy.objects.get(pk=copy_id)
    canonical_copy = selected_draft_copy.parent

    if not selected_draft_copy.location_verified:
        selected_draft_copy.delete()
        models.canonical_to_fp_move(canonical_copy)
    else:
        # We directly edit the canonical copy here and create a history
        # record for it, without touching the draft, because we need to
        # verify the edits separately. This means that in cases where the
        # librarian has made no edits, this will still appear in the admin
        # edit verify queue. I am not sure about the best way to handle this.
        models.create_history(canonical_copy)
        canonical_copy.location_verified = True
        canonical_copy.save()

    return HttpResponse("success")


# used by aja
@login_required
def create_draftcopy(request):
    try:
        copy_id = request.GET.get("copy_id")
    except OSError:
        print("something wrong with id, may be it does not exist at all?")

    selected_copy = models.CanonicalCopy.objects.get(pk=copy_id)
    draft_copy = get_or_create_draft(selected_copy)
    draft_copy.location_verified = True
    draft_copy.save()

    return HttpResponse("success!")


@login_required
def location_incorrect(request):
    try:
        copy_id = request.GET.get("copy_id")
    except OSError:
        print("something wrong with id, may be it does not exist at all?")

    selected_copy = models.CanonicalCopy.objects.get(pk=copy_id)
    draft_copy = get_or_create_draft(selected_copy)
    draft_copy.location_verified = False
    draft_copy.save()

    return HttpResponse("success!")


def contact(request):
    template = loader.get_template("census/contact-form.html")
    content = [
        s.content for s in models.StaticPageText.objects.filter(viewname="contact")
    ]
    context = {"content": content}
    return HttpResponse(template.render(context, request))


## DATA EXPORT VIEWS ##


def location_copy_count_csv_export(request):
    locations = models.CanonicalCopy.objects.all().values("location")
    locations = locations.annotate(total=Count("location")).order_by("location__name")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="shakespeare_census_location_copy_count.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["Location", "Number of Copies"])
    for loc in locations:
        writer.writerow(
            [models.Location.objects.get(pk=loc["location"]).name, loc["total"]]
        )

    return response


def year_issue_copy_count_csv_export(request):
    issues = models.CanonicalCopy.objects.exclude(
        issue__edition__title__hidden=True
    ).values("issue")
    issues = issues.annotate(total=Count("issue")).order_by("issue__start_date")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="shakespeare_census_year_issue_copy_count.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["Year", "STC/Wing", "Title", "Number of Copies"])
    for iss in issues:
        iss_obj = models.Issue.objects.get(pk=iss["issue"])
        writer.writerow(
            [
                iss_obj.start_date,
                iss_obj.stc_wing,
                iss_obj.edition.title.title,
                iss["total"],
            ]
        )

    return response


def copy_sc_bartlett_csv_export(request):
    copies = models.CanonicalCopy.objects.exclude(issue__edition__title__hidden=True)
    copies = copies.exclude(bartlett1939=0, bartlett1916=0)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="shakespeare_census_sc_bartlett.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["SC #", "Bartlett 1939 #", "Bartlett 1916 #", "Title", "Year"])
    for copy in copies:
        writer.writerow(
            [
                copy.nsc,
                copy.bartlett1939,
                copy.bartlett1916,
                copy.issue.edition.title.title,
                copy.issue.start_date,
            ]
        )

    return response


def export(request, groupby, column, aggregate):
    agg_model = Sum if aggregate == "sum" else Count
    try:
        groups = models.CanonicalCopy.objects.all().values(groupby)
    except Exception:
        raise Http404("Invalid groupby column.")

    try:
        rows = groups.annotate(agg=agg_model(column)).order_by(groupby)
    except Exception:
        raise Http404("Invalid aggregation column.")

    filename = "shakespeare_census_{}_of_{}_for_each_{}.csv"
    filename = filename.format(aggregate, column, groupby)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([groupby, f"{aggregate} of {column}"])

    for row in rows:
        writer.writerow([row[groupby], row["agg"]])

    return response
