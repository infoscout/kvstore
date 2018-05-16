# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render

from kvstore.admin.forms import UploadForm
from kvstore.models import Tag


def upload(request):
    """
    Mass set kvtags
    """
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            ctype = form.cleaned_data['object']

            # Process here
            cnt = 0
            for obj_id, k, v in form.cleaned_data['input']:

                tag, created = Tag.objects.get_or_create(
                    content_type=ctype,
                    object_id=obj_id,
                    key=k,
                    defaults={'value': v},
                )
                cnt += 1

            messages.info(request, "%s tags set" % cnt)
    else:
        form = UploadForm()

    context = {'form': form}
    return render(request, 'admin/kvstore/upload.html', context)
