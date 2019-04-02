#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from lessonmgmt.forms.selectmonth_form import *
from lessonmgmt.views.customer_lesson_history_table import *

class ReportView(FormView):
    """
    レポートの月指定用の選択フォームを表示
    """
    template_name = 'lessonmgmt/report_list.html'
    form_class = SelectMonthForm # [teldren] 月の選択リスト用フォーム

    def get_context_data(self, **kwargs):
        form = self.form_class(initial={'number': 3})
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        context['form'] = form
        return context

class GenreGenderAgeFilterView(TemplateView):
    """
    レポートの選択月の結果表示
    """
    template_name = 'lessonmgmt/report_genre_gender_age.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        self.select_month = self.request.GET.get('select_month', None) # [teldren] 検索月の指定。e.g. 2019-12-01
        if self.select_month is None:
            return context
        clht = CustomerLessonHistoryTable(self.select_month)
        reports_genre_gender_df = clht.get_reports_genre_gender()
        reports_genre_age_df = clht.get_reports_genre_age()
        #0 代，80 代，90 代を削除
        reports_genre_age_df = reports_genre_age_df.\
                               drop(reports_genre_age_df[(reports_genre_age_df.age=='0 代')\
                                                         | (reports_genre_age_df.age=='80 代')
                                                         | (reports_genre_age_df.age=='90 代')].index)
        context['reports_genre_gender'] = reports_genre_gender_df.to_dict(orient='records')
        context['reports_genre_age'] = reports_genre_age_df.to_dict(orient='records')
        return context
