# クラウダント データローダー

これは、郵便番号データをCloudantデータベースへロードするPythonのプログラムです。


# 機能

郵便番号データは、次のアドレスにあるzipファイルを展開したCSVファイルで、改行コードはDOS形式、漢字コードはシフトJISとなっています。このプログラムは、改行コードはUNIX形式、漢字コードをUTF-8の中間ファイルを生成して、JSON形式のデータとしてCloudantにロードします。

郵便番号データ: http://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html


# 入力ファイル名と出力先データベースの指定方法

cloudant_load_data.py の次の部分を変更することで、変更する事ができます。

~~~
import uuid
import time
from cloudant.client import Cloudant
from cloudant.query import Query

#==================================
# ロード先データベース名
output_db = 'hokkaido'

# インプットCSVファイル名
input_file = '01hokkai.csv'
output_file = input_file + ".utf-8"
#==================================

# Cloudant認証情報の取得
~~~

# Cloudant サービス資格情報

Cloudant へアクセスするには、Bluemixのサービス資格情報が必要です。Bluemix からCloudantのサービスを作成して、サービス資格情報をvcap-local.jsonにセットしてください。

次の様にファイル名を変更して、credentials 以下の内容を設定します。

~~~
mv vcap-local.json.sample vcap-local.json
~~~


# エラー処理

・入力ファイルに、UTF-8へ変換できない漢字コードが含まれていた場合、先頭から行番号とエラーメッセージをプリントして、次行からのロードを続行します。


