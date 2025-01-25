#!/usr/bin/env python
# -*- coding: utf-8 -*-

from human.model import human
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(human.Base)
Permission.objects.get_or_create(codename='create_human', name='社員情報作成権限', content_type=content_type)
Permission.objects.get_or_create(codename='change_human', name='社員情報変更権限', content_type=content_type)
Permission.objects.get_or_create(codename='view_human', name='社員情報見る権限', content_type=content_type)
