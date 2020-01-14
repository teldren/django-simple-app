#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
from django.db import models


# Create your models here.
class Lesson(models.Model):
    """
    受講者クラス

    :param lesson_id: ジャンルID(Primary Key)
    :type lesson_id: UUID
    :param lessonName: ジャンル名
    :type lessonName: str
    :param basicCharge: 基本料金
    :type basicCharge: int
    :param includeHour: 基本料金に含まれる時間
    :type includeHour: int
    :param hourlyRate: 従量課金情報。e.g. [{"hour" : 0, "rate" : 3500}, {"hour" : 20, "rate" : 3000}, {"hour" : 35, "rate" : 2800}]
    :type hourlyRate: str
    """
    lesson_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lessonName = models.CharField('ジャンル', max_length=100)
    basicCharge = models.IntegerField('基本料金')
    includeHour = models.IntegerField('インクルージョン時間', default=0)
    hourlyRate = models.CharField('従量料金', max_length=150, default='[{"hour" : 0, "rate" : 3500}]')

    def __str__(self):
        return self.lessonName

    # Push testのためのコメント記入。
