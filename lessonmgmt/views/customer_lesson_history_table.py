#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django_pandas.io import read_frame
import pandas as pd
import json
import numpy as np
import datetime

from lessonmgmt.models.customer import *
from lessonmgmt.models.lesson import *
from lessonmgmt.models.lessonhistory import *
from dateutil.relativedelta import relativedelta

class CustomerLessonHistoryTable:
    """
    請求情報，レポート情報を取得するためのクラス

    :param select_month: 選択月
    :param startDate: 選択月初日
    :param endDate: 選択月末日
    :param all_table_df: 顧客一覧を受講履歴一覧とLeft Outer Joinした結果
    :param lesson_df: ジャンル一覧
    :param customers_df: 顧客一覧

    :param basicCharge_dict: 料金計算で利用するapply関数(calculate_invoice)で使う変数
    :param includeHour_dict: 料金計算で利用するapply関数(calculate_invoice)で使う変数
    :param hourlyRate_dict: 料金計算で利用するapply関数(calculate_invoice)で使う変数
    :param lessonHours_dict: 料金計算で利用するapply関数(calculate_invoice)で使う変数
    """
    def __init__(self, select_month):
        self.select_month = select_month
        self.startDate = datetime.datetime.strptime(select_month, '%Y-%m-%d')
        self.endDate = self.startDate + relativedelta(months=1) - relativedelta(days=1)
        self.all_table_df = None
        self.lesson_df = read_frame(Lesson.objects.all())

    def get_all_table(self):
        """
        顧客一覧を受講履歴一覧とLeft Outer Joinした結果を返す。
        顧客一覧と受講履歴一覧をDBより取得し，PandasのDataFrameへ変換。
        Pandasの機能を使って，Left Outer Joinを実施し，DataFrameを返す。

        Returns:
            DataFrame: self.all_table_df

        Columns of self.all_table_df:
            'customer_id', 'name', 'gender', 'age',
            'lessonName_id', 'lessonHours', 'lessonName',
            'lessonName_basicCharge', 'lessonName_includeHour',
            'lessonName_hourlyRate', 'Json_hourlyRate', 'Total_Price', 'index_val'
        """
        if self.all_table_df is not None:
            return self.all_table_df
        # [teldren] 顧客リスト
        self.customers_df = read_frame(Customer.objects.all())
        if len(self.customers_df.index) == 0:
            return pd.DataFrame()

        # [teldren] 受講履歴リスト，ジャンル情報付きで取得。対象月でフィルタリング。
        lessonhistories = LessonHistory.objects.filter(lessonDate__gte=self.startDate,
                                                       lessonDate__lte=self.endDate)\
                                               .select_related()\
                                               .order_by('lessonDate')
        # [teldren] 受講履歴がない場合，顧客一覧に受講無し情報を付与する
        lessonhistories_df = pd.DataFrame()
        if lessonhistories.count() == 0:
            df = self.customers_df
            df.loc[:,'lessonName'] = '-----'
            df.loc[:,'lessonHours'] = 0
            df.loc[:,'Total_Price'] = 0
            return df
        # [teldren] lessonhistoriesの検索結果をPandasのDataFrameへ変換する。
        for lessonhistory in lessonhistories:
            lessonhistories_df = pd.concat([lessonhistories_df,lessonhistory.get_pandas_dataframe()])

        # [teldren] 顧客リストと受講履歴リストを外部結合。受講履歴のない顧客も抽出するため。
        customer_lessonhistories_df = pd.merge(self.customers_df, lessonhistories_df,
                                               left_on='customer_id',
                                               right_on='customerName_id',
                                               how='left')
        # [teldren] 受講履歴のない顧客レコードのジャンル名，従量料金，レッスン時間がNaNになるため，'-----'，空Json，0とを代入。
        customer_lessonhistories_df = customer_lessonhistories_df.fillna({'lessonName':'-----',
                                                                          'lessonName_id':'Null',
                                                                          'lessonName_hourlyRate': '{}',
                                                                          'lessonHours': 0})
        # [teldren] 顧客id，ジャンルidで集計(GroupBy)
        df = customer_lessonhistories_df[['name', 'customer_id', 'gender', 'age',
                                          'lessonName_id', 'lessonHours']]\
                                          .groupby(['customer_id', 'name', 'gender', 'age', 'lessonName_id'])\
                                          .sum().reset_index()
        # [teldren] 上記集計結果へ結合するためのジャンル情報を抽出
        lessonInfo = customer_lessonhistories_df[['lessonName', 'lessonName_id',
                                                  'lessonName_basicCharge', 'lessonName_includeHour',
                                                  'lessonName_hourlyRate']].drop_duplicates()

        # [teldren] 従量課金情報を文字列からJson形式へ一括変換。結合前に，lessonInfoのhourlyRateをリスト形式に変換する。
        lessonInfo.loc[:,'Json_hourlyRate'] = lessonInfo.lessonName_hourlyRate.apply(self.str2json_hourlyrate)
        # [teldren] 集計結果とジャンル情報を結合
        df = pd.merge(df, lessonInfo, on='lessonName_id', how='left')
        df.loc[:,'Total_Price'] = 0
        # [teldren] apply関数calculate_report用のdictionaryとindexを用意
        self.basicCharge_dict = df.lessonName_basicCharge.to_dict()
        self.includeHour_dict = df.lessonName_includeHour.to_dict()
        self.hourlyRate_dict = df.Json_hourlyRate.to_dict()
        self.lessonHours_dict = df.lessonHours.to_dict()
        df.loc[:,'index_val'] = df.index
        df.loc[:,'Total_Price'] = df.index_val.apply(self.calculate_invoice)
        self.all_table_df = df

        return self.all_table_df

    def get_all_table_innerjoin(self):
        """
        顧客一覧と受講履歴のLeft Joinした結果を返す。
        """
        return self.get_all_table().dropna()

    def get_invoices(self):
        """
        全顧客の請求情報を返す。
        顧客情報がない場合，空のDataFrameが返る。

        Returns:
            DataFrame: invoices_df

        Columns of invoices_df:
            'customer_id', 'name', 'lessonHours', 'Total_Price', 'lessonName'
        """
        df = self.get_all_table()
        if len(df.index) == 0:
            return df

        invoices_df = df[['customer_id', 'name',
                          'lessonName', 'lessonHours', 'Total_Price']]\
                          .groupby(['customer_id', 'name'])\
                          .apply(self.groupby_name)\
                          .reset_index()
        return invoices_df

    def get_reports_genre_gender(self):
        """
        ジャンルと性別毎での売上を返す。

        Returns:
            DataFrame: rslt_df

        Columns of rslt_df:
            'lessonName', 'gender', 'lessonHours', 'customerCount', 'Total_Price'
        """
        genre_gender_master_df = self._create_genre_gender_master()
        df = self.get_all_table_innerjoin()
        if len(df.index) == 0:
            genre_gender_master_df['lessonHours'] = 0
            genre_gender_master_df['customerCount'] = 0
            genre_gender_master_df['Total_Price'] = 0
            return genre_gender_master_df
        df.loc[:,'customerCount'] = 0
        genre_gender_df = df.groupby(['lessonName', 'gender'])\
                            .agg({'lessonHours':'sum', 'customerCount':'count', 'Total_Price':'sum'})\
                            .reset_index()
        genre_gender_master_df = self._create_genre_gender_master()
        rslt_df = pd.merge(genre_gender_master_df, genre_gender_df,
                           left_on=['lessonName', 'gender'],
                           right_on=['lessonName', 'gender'], how='left')
        return rslt_df.fillna(0)

    def get_reports_genre_age(self):
        """
        ジャンル，性別毎，年齢毎での売上を返す。

        Returns:
            DataFrame: rslt_df

        Columns of rslt_df:
            'lessonName', 'gender', 'age', 'lessonHours', 'customerCount', 'Total_Price'
        """
        genre_gender_age_master_df = self._create_genre_gender_age_master()
        df = self.get_all_table_innerjoin()
        if len(df.index) == 0:
            genre_gender_age_master_df.loc[:,'lessonHours'] = 0
            genre_gender_age_master_df.loc[:,'customerCount'] = 0
            genre_gender_age_master_df.loc[:,'Total_Price'] = 0
            return genre_gender_age_master_df
        df.loc[:,'customerCount'] = 0
        #labels = [ "{0} - {1}".format(i, i + 9) for i in range(0, 100, 10) ]
        labels = [ "{0} 代".format(i) for i in range(0, 100, 10) ]
        cut_age = pd.cut(df.age, np.arange(0, 101, 10),
           include_lowest=True, right=False, labels=labels)
        genre_age_df = df.groupby(['lessonName', 'gender', cut_age])\
                         .agg({'lessonHours':'sum', 'customerCount':'count', 'Total_Price':'sum'})\
                         .reset_index()
        rslt_df = pd.merge(genre_gender_age_master_df, genre_age_df,
                           left_on=['lessonName', 'gender', 'age'],
                           right_on=['lessonName', 'gender', 'age'], how='left')
        return rslt_df.fillna(0)

    def calculate_invoice(self, idx):
        """
        料金計算をする，Pandasのapply用関数

        Returns:
            float: invoice
        """
        invoice = 0
        lessonHours = self.lessonHours_dict[idx]
        if lessonHours == 0:
            return invoice

        basicCharge = self.basicCharge_dict[idx]
        includeHour = self.includeHour_dict[idx]
        hourlyRate = self.hourlyRate_dict[idx]
        invoice = basicCharge
        not_find = True
        for rate in reversed(hourlyRate):
            if not_find:
                if lessonHours > rate['hour']:
                    invoice += (lessonHours-rate['hour'])*rate['rate']
                    before_hour = rate['hour']
                    not_find = False
            else:
                invoice += (before_hour - rate['hour'])*rate['rate']
                before_hour = rate['hour']
        # [teldren] 基本料金に含まれる時間分の料金を除く。
        invoice = invoice - includeHour*hourlyRate[0]['rate']
        if invoice < 0:
            invoice = 0
        return invoice


    def str2json_hourlyrate(self, hourlyrate):
        """
        従量課金情報の文字列をJson形式に変換する，Pandasのapply用関数。

        Returns:
            Json: hourlyrate_json
        """
        hourlyrate_json = json.loads(hourlyrate)
        return hourlyrate_json

    def groupby_name(self, ser):
        """
        ジャンル名を連結する，Pandasのapply用関数。

        Returns:
            Series: sum of 'lessonHours', sum 'Total_Price', and count of 'lessonName'
        """
        return pd.Series(dict(lessonHours=ser['lessonHours'].sum(),
                              Total_Price=ser['Total_Price'].sum(),
                              lessonName="%s(%s)" % ('/'.join(ser['lessonName']),
                                                     ser['lessonName'].count())))

    def _create_genre_gender_master(self):
        """
        ジャンルと性別の全組合せを返す

        Returns:
            DataFrame: Table of Genre and Gender

        Columns of return:
            'lessonName', 'gender'
        """
        gender_df = pd.DataFrame({'gender' : ['男性', '女性']})
        master_df = pd.merge(self.lesson_df.assign(tmp=1),
                             gender_df.assign(tmp=1),
                             how='outer')\
                      .drop('tmp',axis=1)
        return master_df[['lessonName', 'gender']]

    def _create_genre_gender_age_master(self):
        """
        ジャンル，性別，年齢の全組合せを返す

        Returns:
            DataFrame: Table of Genre and Gender and Age

        Columns of return:
            'lessonName', 'gender', 'age'
        """
        age_df = pd.DataFrame({'age' : [ "{0} 代".format(i) for i in range(0, 100, 10) ]})
        lesson_gender_df = self._create_genre_gender_master()
        master_df = pd.merge(lesson_gender_df.assign(tmp=1),
                             age_df.assign(tmp=1),
                             how='outer')\
                      .drop('tmp',axis=1)
        return master_df[['lessonName', 'gender', 'age']]
