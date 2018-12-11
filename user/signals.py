#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : user/signals.py
#
#       Creation Date : Tue 11 Dec 2018 10:59:33 AM EET
#
#       Last Modified : Tue 11 Dec 2018 11:28:24 AM EET
#
#       Developer : raratiru  | https://twitter.com/raratiru
#
# ==============================================================================

from django.contrib.auth.models import Group
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner


@receiver(
    post_save,
    sender=settings.AUTH_USER_MODEL,
)
@on_transaction_commit
def add_superuser_group(instance, raw, **kwargs):
    if not raw:
        if instance.is_superuser:
            instance.groups.add(Group.objects.get(name='Superuser'))
