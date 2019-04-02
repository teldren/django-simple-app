#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from lessonmgmt.models.lessonhistory import *
from lessonmgmt.forms.selectmonth_form import *
from lessonmgmt.views.customer_lesson_history_table import *

import datetime
from dateutil.relativedelta import relativedelta

# Create your views here.
class InvoiceView(FormView):
    """
    請求一覧の月指定用の選択フォームを表示
    """
    template_name = 'lessonmgmt/invoice_list.html'
    form_class = SelectMonthForm # [teldren] 月の選択リスト用フォーム

    def get_context_data(self, **kwargs):
        form = self.form_class(initial={'number': 3}) # [teldren] 現在＋3ヶ月分を表示
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        context['form'] = form
        return context

class InvoiceFilterView(TemplateView):
    """
    請求一覧の選択月の結果表示
    """
    template_name = 'lessonmgmt/invoice_filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        self.select_month = self.request.GET.get('select_month', None) # [teldren] 検索月の指定。e.g. 2019-12-01
        if self.select_month is None:
            return context
        clht = CustomerLessonHistoryTable(self.select_month)
        invoices_df = clht.get_invoices()
        if len(invoices_df.index) == 0:
            context['invoices'] = invoices_df.to_dict(orient='records')
            return context
        invoices_df.loc[invoices_df['Total_Price'] == 0, 'lessonName'] = '-----'
        context['invoices'] = invoices_df.to_dict(orient='records')
        return context
