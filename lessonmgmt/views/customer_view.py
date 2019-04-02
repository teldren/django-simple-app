#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from lessonmgmt.models.customer import *
from lessonmgmt.forms.customer_form import *

# Create your views here.
class CustomerListView(ListView):
    """
    受講者一覧を表示
    """
    template_name = 'lessonmgmt/customer_list.html'
    model = Customer

class CustomerCreateView(CreateView):
    """
    受講者新規追加
    """
    template_name = 'lessonmgmt/customer_update.html'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('lessonmgmt:customer_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」を作成しました'.format(form.instance))
        return result

class CustomerUpdateView(UpdateView):
    """
    受講者の情報修正
    """
    template_name = 'lessonmgmt/customer_update.html'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('lessonmgmt:customer_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '「{}」を更新しました'.format(form.instance))
        return result

class CustomerDeleteView(DeleteView):
    """
    受講者の削除
    """
    template_name = 'lessonmgmt/customer_confirm_delete.html'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('lessonmgmt:customer_list')

    def delete(self, request, *args, **kwargs):
        try:
            result = super().delete(request, *args, **kwargs)
        except models.ProtectedError:
            messages.error(
                self.request, '「{}」は削除できませんでした'.format(self.object))
            return redirect('lessonmgmt:customer_list')

        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result
