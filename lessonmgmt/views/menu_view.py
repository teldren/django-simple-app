#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

# Create your views here.
class MenuView(TemplateView):
    template_name = 'lessonmgmt/menu_list.html'
