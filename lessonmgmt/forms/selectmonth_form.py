#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class SelectMonthForm(forms.Form):
    """
    選択月用のフォーム。フォーム呼び出し時に選択月の表示数を指示。
    選択月の表示数の指定がなければ，CHOICESが用いられ当月のみ表示。
    """
    CHOICES = [
        (datetime.now().strftime("%Y-%m-01"), datetime.now().strftime("%Y年%m月"))
    ]
    select_month = forms.ChoiceField(label='月選択', widget=forms.Select, choices=CHOICES)

    # [teldren] View で呼び出す際，'number'で指定された分だけの過去月をリスト表示する。指定がなければ，CHOICESで当月のみ表示。
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        initial = kargs.get('initial', None)
        if not initial:
            return
        self.number = initial.get('number', None)
        # リストに表示する月データの作成。
        now = datetime.now()
        _choices = []
        for i in range(0, self.number+1):
            before_month = now - relativedelta(months=i)
            _choices.append((before_month.strftime("%Y-%m-01"), before_month.strftime("%Y年%m月")))
        self.fields['select_month'].choices = _choices

