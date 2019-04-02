#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models

from lessonmgmt.models.lesson import *
from lessonmgmt.forms.lesson_form import *

# Create your views here.
class LessonListView(ListView):
    """
    ジャンル一覧を表示
    """
    template_name = 'lessonmgmt/lesson_list.html'
    model = Lesson

class LessonCreateView(CreateView):
    """
    ジャンル新規追加
    """
    template_name = 'lessonmgmt/lesson_update.html'
    model = Lesson
    form_class = LessonForm
    success_url = reverse_lazy('lessonmgmt:lesson_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」を作成しました'.format(form.instance))
        return result

class LessonUpdateView(UpdateView):
    """
    ジャンルの情報修正
    """
    template_name = 'lessonmgmt/lesson_update.html'
    model = Lesson
    form_class = LessonForm
    success_url = reverse_lazy('lessonmgmt:lesson_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」を更新しました'.format(form.instance))
        return result

class LessonDeleteView(DeleteView):
    """
    ジャンルの削除
    """
    template_name = 'lessonmgmt/lesson_confirm_delete.html'
    model = Lesson
    form_class = LessonForm
    success_url = reverse_lazy('lessonmgmt:lesson_list')

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
        except models.ProtectedError:
            messages.error(
                self.request, '「{}」は削除できませんでした'.format(self.object))
            return redirect('lessonmgmt:lesson_list')

        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result
