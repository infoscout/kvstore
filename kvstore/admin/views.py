# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from kvstore.admin.forms import UploadForm
from kvstore.models import Tag


@permission_required(('kvstore.add_tag', 'kvstore.change_tag',))
def upload(request):
    bulk_entry_form = UploadForm()
    context = {'bulk_entry_form': bulk_entry_form}
    return render(request, 'admin/kvstore/upload.html', context)


@permission_required(('kvstore.add_tag', 'kvstore.change_tag',))
def upload_bulk(request):
    """
    Mass set kvtags
    """
    if request.method == 'POST':
        bulk_entry_form = UploadForm(request.POST)
        if bulk_entry_form.is_valid():
            ctype = bulk_entry_form.cleaned_data['object']

            # Process here
            count = 0
            for obj_id, k, v in bulk_entry_form.cleaned_data['input']:

                tag, created = Tag.objects.update_or_create(
                    content_type=ctype,
                    object_id=obj_id,
                    key=k,
                    defaults={'value': v}
                )
                count += 1

            messages.info(request, "%s tags set" % count)
    else:
        bulk_entry_form = UploadForm()
    context = {'bulk_entry_form': bulk_entry_form}
    return render(request, 'admin/kvstore/upload.html', context)
