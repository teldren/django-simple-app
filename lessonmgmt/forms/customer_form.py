#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm
from lessonmgmt.models.customer import *

class CustomerForm(ModelForm):
    """
    受講者情報の入力用フォーム
    """
    class Meta:
        model = Customer
        fields = ('name', 'gender', 'age', )
