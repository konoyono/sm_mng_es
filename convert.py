import json
import xmljson
from lxml.etree import parse
import glob
import subprocess
import os
import time

i=0

# 既存のインデックス情報を再作成
subprocess.call( 'curl -XDELETE "http://localhost:9200/stepmania"', shell=True )
subprocess.call( 'curl -XPUT "http://localhost:9200/stepmania" -H "Content-Type: application/json" -d @stepmania_mapping.json', shell=True )

# 前回作成時のデータを削除
for path in glob.glob("/Users/okada-toshiki/Desktop/result/*.json"):
    os.remove(path)

for path in glob.glob("/Users/okada-toshiki/Library/Preferences/StepMania 5/Upload/*.xml"):
    root = parse(path).getroot()

    # 自分以外のプレイデータが入ってる場合は削除
    # TODO: 現状、自分が2P側のデータしか入ってないので先頭の要素を削除しているが
    # 本来はUserID参照して自分のプレイデータのみ残すようにすべき
    if len(root[1]) == 2: root[1][0].getparent().remove(root[1][0])
    
    # 過去のディレクトリ構成時点でのプレイデータは無視
    if os.path.exists("/Users/okada-toshiki/Desktop/StepMania-5.0.12/" + root[1][0][0].attrib['Dir']) == False:
        continue

    # ダブルでのプレイデータは無視
    if root[1][0][1].attrib['StepsType'] == 'dance-double':
        continue

    # elasticsearch側でDate型として格納するため、日付だけ抜粋
    root[1][0][2][9].text = root[1][0][2][9].text.split(" ")[0]

    # boolean 型のクリアリザルト要素を追加
    if root[1][0][2][1].text == "Failed": root[1][0][2].set("Cleared", "false")
    else:                                 root[1][0][2].set("Cleared", "true")

    # smファイルから当該難易度のレベルを取得
    for path in glob.glob("/Users/okada-toshiki/Desktop/StepMania-5.0.12/" + root[1][0][0].attrib['Dir'] + "*.sm"):
        with open(path) as f:
            smlines = f.readlines()
            smline_num = 0

            for smline in smlines:
                if 'dance-single:' in smline:
                    if smlines[smline_num+2].rstrip(':\n').lstrip(' ') == root[1][0][1].attrib['Difficulty']:
                        root[1][0][1].set("Level", smlines[smline_num+3].rstrip(':\n').lstrip(' '))
                smline_num += 1
    
    # 結果をまとめたjsonをファイルに書き出す
    with open('/Users/okada-toshiki/Desktop/result/result' + str(i) + '.json', 'a') as fw:
        json.dump(xmljson.yahoo.data(root), fw, indent=2)
        
    i += 1

# elasticsearch への登録
for j in range(i):
    cmd = 'curl -XPOST "http://localhost:9200/stepmania/result" -H "Content-Type: application/json" --data-binary @/Users/okada-toshiki/Desktop/result/result' + str(j) + '.json'
    subprocess.call( cmd, shell=True )
