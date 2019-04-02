#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from lessonmgmt.models.lessonhistory import *
from lessonmgmt.forms.lessonhistory_form import *

# Create your views here.
class LessonHistoryListView(ListView):
    """
    受講履歴一覧を表示
    """
    template_name = 'lessonmgmt/lessonhistory_list.html'
    model = LessonHistory

    def get_queryset(self):
        return LessonHistory.objects.all().select_related() # [teldren] Joinして引っ張ってくる。

class LessonHistoryCreateView(CreateView):
    """
    受講履歴新規追加
    """
    template_name = 'lessonmgmt/lessonhistory_update.html'
    model = LessonHistory
    form_class = LessonHistoryForm
    success_url = reverse_lazy('lessonmgmt:lessonhistory_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」を作成しました'.format(form.instance))
        return result

class LessonHistoryUpdateView(UpdateView):
    """
    受講履歴の情報修正
    """
    template_name = 'lessonmgmt/lessonhistory_update.html'
    model = LessonHistory
    form_class = LessonHistoryForm
    success_url = reverse_lazy('lessonmgmt:lessonhistory_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」を更新しました'.format(form.instance))
        return result

class LessonHistoryDeleteView(DeleteView):
    """
    受講履歴の削除
    """
    template_name = 'lessonmgmt/lessonhistory_confirm_delete.html'
    model = LessonHistory
    form_class = LessonHistoryForm
    success_url = reverse_lazy('lessonmgmt:lessonhistory_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{0}: {1}の{2}」を削除しました'.format(self.object.lessonDate,
                                                                self.object,
                                                                self.object.lessonName))
        return result
