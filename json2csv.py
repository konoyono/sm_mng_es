import pprint
import json
import glob
import codecs


def get_dict_hierarchy(target_dict, root_path, sep):
    if isinstance(target_dict, dict):
        for key in target_dict.keys():
            value = target_dict[key]
            target_path = root_path + sep + key
            # valueが辞書じゃない場合にはパスを返す。
            if not isinstance(value, dict):
                yield target_path[1:]
            # 辞書の場合にはもう一度探索する。
            else:
                yield from get_dict_hierarchy(value, target_path, sep)


def dig_dict(target_dict, target_branch, sep):
    limbs = target_branch.split(sep)
    leaf = target_dict
    for one_limb in limbs:
        leaf = leaf[one_limb]
    return leaf


# 変換したいJSONファイルを読み込む
for path in glob.glob("/Users/okada-toshiki/Desktop/result/result1000.json"):
    with open(path, 'r') as f:
        res = json.load(f)
        flat_dict = {}
        for one_branch in list(get_dict_hierarchy(res, '', '_')):
            flat_dict[one_branch] = dig_dict(res, one_branch, '_')
        header = ",".join(map(str, flat_dict.keys()))

        values = ""
        for v in flat_dict.values():
            if ',' in v:
                v = '"' + v + '"'
            if values == "":
                values = v
            else:
                values += ',' + v

print(header, file=codecs.open(
    '/Users/okada-toshiki/Desktop/csv_test.csv', 'a', 'utf-8'))

print(values, file=codecs.open(
    '/Users/okada-toshiki/Desktop/csv_test.csv', 'a', 'utf-8'))
