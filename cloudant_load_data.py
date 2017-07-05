#!/usr/bin/env python                                                           
# -*- coding:utf-8 -*-                                                          
#
# SJIS,改行コードCRLF のCSVファイルを
# UTF-8 Unix形式改行コード LF に変換して、
# JSON形式で、Cloudantへロードする
#
#

import sys
import json
import codecs
import uuid
import time
from cloudant.client import Cloudant
from cloudant.query import Query

#==================================
# ロード先データベース名
output_db = 'sample'

# インプットCSVファイル名
input_file = 'sample.csv'
output_file = input_file + ".utf-8"
#==================================

# Cloudant認証情報の取得
f = open('./vcap-local.json', 'r')
cred = json.load(f)
f.close()

print "クラウダントへの接続"
client = Cloudant(cred['services']['cloudantNoSQLDB'][0]['credentials']['username'], 
                  cred['services']['cloudantNoSQLDB'][0]['credentials']['password'], 
                  url=cred['services']['cloudantNoSQLDB'][0]['credentials']['url'])
client.connect()


# DBが存在していたら削除
print "既存データベース ", output_db ," の作成"
try:
    db = client[output_db]
    if db.exists():
        client.delete_database(output_db)
except:
    pass


# DBを新規作成
print "新規データベース ", output_db ," の作成"
try: 
    db = client.create_database(output_db)
    print "データベース作成成功"
except:
    print "データベース作成失敗"
    sys.exit()


# 文字コード変換など前処理結果を中間ファイルへ出力
fin = codecs.open(input_file, "r", "shift_jis")
fout = codecs.open(output_file, "w", "utf-8")
line_no = 0
while True:
    try:
        line = fin.readline()
        if line == "":
            break
        line = line.rstrip('\r\n') + "\n"
        line = line.replace('"','')
        fout.write(line)
        line_no = line_no + 1
    except Exception as e:
        print "Line = ", line_no, " Error message: ", e
        pass


# エクセルシートからのCSVデータを読んでDBへ登録する
reader = codecs.open(output_file, 'r', 'utf-8')
lines = reader.readlines()
print lines[0]

wait_cnt = 0
line_no = 0
for line in lines:

    # ヘッダ行をスキップ
    if line_no == 0:
        line_no = line_no + 1
        continue

    # デバック表示
    print line_no,line.rstrip('\n')

    # 配列へ展開
    al = line.split(',')
    line_no = line_no + 1

    # Cloudant Liteプランの書き込み速度制限に対応
    wait_cnt = wait_cnt + 1
    if wait_cnt > 9:
        wait_cnt = 0
        time.sleep(1)

    # DOC作成と書込み
    id = str(uuid.uuid4())
    json_doc = {
        #"_id": id,
        "_id": al[0],
        "jusho_CD": al[0],
        "todofuken_CD": al[1],
        "sichoson_CD": al[2],
        "chyoiki_CD": al[3],
        "zip_code": al[4],
        "jigyosyo_flag": al[5],
        "haishi_flag": al[6],
        "todoufuken": al[7],
        "todoufuken_kana": al[8],
        "sicyoson": al[9],
        "sicyoson_kana": al[10],
        "cyoiki": al[11],
        "cyoiki_kana": al[12],
        "cyoiki_hosoku": al[13],
        "kyoto_tori_na": al[14],
        "aza_cyo_me": al[15],
        "aza_cyo_me_kana": al[16],
        "hosoku": al[17],
        "jigyosyo_mei": al[18],
        "jigyosyo_mei_kana": al[19],
        "jigyosyo_jyusyo": al[20]
        #"sin_jyusyo_kana": al[21]
     }

    # 書込み
    cdoc = db.create_document(json_doc)
    #if cdoc.exists():
    #    print "SUCCESS!!"

client.disconnect()

