#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'lessonmgmt'
urlpatterns = [
    # メニュー
    path('menu/', views.menu_view.MenuView.as_view(), name='menu_list'),
    # 顧客一覧
    path('customer/', views.customer_view.CustomerListView.as_view(), name='customer_list'), # 一覧
    path('customer/add/', views.customer_view.CustomerCreateView.as_view(), name='customer_add'), # 新規登録
    path('customer/update/<uuid:pk>/', views.customer_view.CustomerUpdateView.as_view(), name='customer_update'), # 修正
    path('customer/delete/<uuid:pk>/', views.customer_view.CustomerDeleteView.as_view(), name='customer_delete'), # 削除
    # ジャンル一覧
    path('lesson/', views.lesson_view.LessonListView.as_view(), name='lesson_list'), # 一覧
    path('lesson/add/', views.lesson_view.LessonCreateView.as_view(), name='lesson_add'), # 登録
    path('lesson/update/<uuid:pk>/', views.lesson_view.LessonUpdateView.as_view(), name='lesson_update'), # 修正
    path('lesson/delete/<uuid:pk>/', views.lesson_view.LessonDeleteView.as_view(), name='lesson_delete'),  # 削除
    # 受講履歴一覧
    path('lessonhistory/', views.lessonhistory_view.LessonHistoryListView.as_view(), name='lessonhistory_list'),  # 一覧
    path('lessonhistory/add/', views.lessonhistory_view.LessonHistoryCreateView.as_view(), name='lessonhistory_add'), # 登録
    path('lessonhistory/edit/<uuid:pk>/', views.lessonhistory_view.LessonHistoryUpdateView.as_view(), name='lessonhistory_update'), # 修正
    path('lessonhistory/delete/<uuid:pk>/', views.lessonhistory_view.LessonHistoryDeleteView.as_view(), name='lessonhistory_delete'),  # 削除
    # 請求一覧
    path('invoice/', views.invoice_view.InvoiceView.as_view(), name='invoice_search_form'),   # 検索フォーム
    path('invoice/filter', views.invoice_view.InvoiceFilterView.as_view(), name='invoice_filter'),   # 検索結果画面
    # レポート
    path('report/', views.report_view.ReportView.as_view(), name='report_search_form'),   # 検索フォーム
    path('report/genre_gender_age', views.report_view.GenreGenderAgeFilterView.as_view(), name='report_genre_gender_age'),   # ジャンル年齢レポート画面
]
