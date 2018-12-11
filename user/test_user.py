#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : testing_on_commit/tests/test_users.py
#
#       Creation Date : Tue 11 Dec 2018 09:50:12 AM EET
#
#       Last Modified : Tue 11 Dec 2018 11:30:08 AM EET
#
#       Developer : raratiru  | https://twitter.com/raratiru
#
# ==============================================================================

import pytest
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils import timezone
from itertools import chain


pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def group():
    superuser = Group()
    superuser.name = 'Superuser'
    superuser.save()
    return superuser


@pytest.fixture
def user_data():
    return {
        'username': 'user',
        'password1': '123!trettb',
        'password2': '123!trettb',
    }


@pytest.fixture
def superuser_data(user_data):
    new_data = {
        'is_staff': True,
        'is_superuser': True,
        'date_joined': timezone.now(),
    }
    return dict(chain.from_iterable(
        d.items() for d in (user_data, new_data)
    ))


def test_user(group, user_data, superuser_data):
    '''
    This test will fail if on_commit is not used in the signal.
    '''
    creation_form = UserCreationForm(data=user_data)
    user = creation_form.save()
    change_form = UserChangeForm(instance=user, data=superuser_data)
    with transaction.atomic():
        superuser = change_form.save()
    assert group in superuser.groups.all()


def test_user_non_atomic(group, user_data, superuser_data):
    '''
    An atomic transaction is necessary for on_commit to work as expected.
    Without it, no groups are added
    '''
    creation_form = UserCreationForm(data=user_data)
    user = creation_form.save()
    change_form = UserChangeForm(instance=user, data=superuser_data)
    superuser = change_form.save()
    assert group not in superuser.groups.all()
