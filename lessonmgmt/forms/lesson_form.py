#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from lessonmgmt.models.lesson import *
import json

class LessonForm(ModelForm):
    """
    ジャンル情報の入力用フォーム
    """
    class Meta:
        model = Lesson
        fields = ('lessonName', 'basicCharge', 'includeHour', 'hourlyRate')

    def clean_hourlyRate(self):
        """
        従量課金情報のバリデーション
        e.g. [{"hour" : 0, "rate" : 1500}, {"hour" : 20, "rate" : 1000}, {"hour" : 35, "rate" : 800}]
        """
        hourlyRate  = self.cleaned_data['hourlyRate']
        try:
            hourlyRate_json = json.loads(hourlyRate)
            json_length = len(hourlyRate_json)
            if json_length == 0:
                raise forms.ValidationError()
            for i in range(0, json_length):
                hourlyRate_json[i]["hour"]
                hourlyRate_json[i]["rate"]
        except:
            raise forms.ValidationError(u'有効なJson形式ではありません')

        return hourlyRate
