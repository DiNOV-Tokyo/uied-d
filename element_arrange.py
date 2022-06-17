import json


# オリジナルのjsonファイルを少々アレンジ Arrange Json

def arrange_json(filename_json):
    print("#########     オリジナルのjsonファイルを少々アレンジ Arrange Json       ###########")
    # 画像のサイズで　画像/画像ではない　を判別する。（簡易にするための一時的な処理）
    with open(filename_json, "r") as f:
        jon_dat = json.load(f)

        a = json.dumps(jon_dat)
        element_num = a.count('"id":')
        element_cnt = 0

        arranged_element = []
        # 一旦、大きさが250以上の検出物のみをImageとする。
        # Image, Text のみをデータとして保存
        for k in range(element_num):
            if int(jon_dat["compos"][k]["height"]) > 140 and int(jon_dat["compos"][k]["width"]) > 140:
                # もしchildrenがいたら、そのchildrenはImageとしない。
                if "children" in jon_dat["compos"][k]:
                    for children_num in jon_dat["compos"][k]["children"]:
                        jon_dat["compos"][children_num]["height"] = 10
                        jon_dat["compos"][children_num]["width"] = 10
                        jon_dat["compos"][children_num]["class"] = "Nan"
                    jon_dat["compos"][k]["children"] = []

                jon_dat["compos"][k]["class"] = "Image"
                jon_dat["compos"][k]["id"] = element_cnt
                arranged_element.append(jon_dat["compos"][k])
                element_cnt = element_cnt + 1

            if jon_dat["compos"][k]["class"] == "Text":
                jon_dat["compos"][k]["id"] = element_cnt
                arranged_element.append(jon_dat["compos"][k])
                element_cnt = element_cnt + 1

    result = {
        "compos": arranged_element,
        "img_shape": jon_dat["img_shape"],
        }

    with open(filename_json, mode='wt', encoding='utf-8') as f0:
        json.dump(result, f0, ensure_ascii=False, indent=2)

    return "OK"
