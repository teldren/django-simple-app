#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm
from lessonmgmt.models.lessonhistory import *

class LessonHistoryForm(ModelForm):
    """
    受講履歴の入力用フォーム
    """
    class Meta:
        model = LessonHistory
        fields = ('customerName', 'lessonName', 'lessonDate', 'lessonHours')
