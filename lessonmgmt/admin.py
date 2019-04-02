#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from lessonmgmt.models.customer import *
from lessonmgmt.models.lesson import *
from lessonmgmt.models.lessonhistory import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Lesson)
admin.site.register(LessonHistory)
