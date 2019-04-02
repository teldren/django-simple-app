#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
from django.db import models

# Create your models here.
class Customer(models.Model):
    """
    受講者クラス

    :param customer_id: 受講者ID(Primary Key)
    :type customer_id: UUID
    :param name: 受講者名
    :type name: str
    :param gender: 性別
    :type gender: choice
    :param age: 年齢
    :type age: int
    """
    GENDER_CHOICES = (
        (u'male', u'男性'),
        (u'female', u'女性'),
    )

    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('名前', max_length=50) # [teldren] 同姓同名時は，受講履歴登録時の名前選択で区別がつかなくなる。
    gender = models.CharField('性別', max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField('年齢')

    def __str__(self):
        return self.name

