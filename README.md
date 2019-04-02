# Django Simple App

### 概要
- レッスンの受講履歴管理のサンプルアプリケーションを開発。
- レッスンの料金体系の管理，受講者の受講履歴管理，レポートの作成機能を実装。

### 開発方針
- 無駄なSQLが発行されないように実装
- SQLはデータの抽出，挿入の基本機能のみを用い，GroupBy句などの機能はPython側で実装。理由は，特になし。

### 利用ライブラリ
- django-bootstrap4
- django-pandas
- numpy
- pandas
- python-dateutil
