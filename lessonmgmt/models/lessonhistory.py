#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import pandas as pd
from django.db import models
from django.utils import timezone
from django.core import validators

# Create your models here.
class LessonHistory(models.Model):
    """
    受講履歴クラス

    :param lessonhistory_id: 受講履歴ID(Primary Key)
    :type lessonhistory_id: UUID
    :param customerName: 受講者名, ForeignKey
    :type customerName: str
    :param lessonName: ジャンル名, ForeignKey
    :type lessonName: str
    :praam lessonDate: 受講日
    :type lessonDate: Date
    :param lessonHours: 受講時間
    :type lessonHours: int
    """
    lessonhistory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customerName = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name='顧客名') # [teldren] 主キーのcustomer id が登録される。
    lessonName = models.ForeignKey('Lesson', on_delete=models.PROTECT, verbose_name='ジャンル名') # [teldren] 主キーのLesson id が登録される。
    lessonDate = models.DateField('受講日', default=timezone.now)
    lessonHours = models.IntegerField('受講時間', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(12)])

    def get_pandas_dataframe(self):
        """
        DataFrame型に変換して出力する。
        出力する際，関連するCustomer, Lessonに関する情報も付与する。
        """
        df = pd.DataFrame( [[self.lessonhistory_id, self.customerName.name,
                             self.customerName.customer_id, self.customerName.gender,
                             self.customerName.age, self.lessonName.lessonName,
                             self.lessonName.lesson_id, self.lessonName.basicCharge,
                             self.lessonName.includeHour, self.lessonName.hourlyRate,
                             self.lessonDate, self.lessonHours]],
                           columns=['lessonhistory_id', 'customerName',
                                    'customerName_id', 'customerName_gender',
                                    'customerName_age', 'lessonName',
                                    'lessonName_id', 'lessonName_basicCharge',
                                    'lessonName_includeHour', 'lessonName_hourlyRate',
                                    'lessonDate', 'lessonHours'])
        return df

    def __str__(self):
        return self.customerName.name
