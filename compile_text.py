import os
import cv2
import json
import sys
import collections
import pickle
import element_reorder as er

args = sys.argv
# filename without extension
filename = "br"
filename = args[1]
filename_img = "./data/input/" + filename + ".jpg"
filename_json = "./data/output/merge/" + filename + ".json"
filename_element_json = "./data/output/merge/" + filename + "_element.json"
out_dir = "./data/output/merge/" + filename
filename_html = out_dir + "/" + filename + ".html"
filename_css = out_dir + "/" + filename + ".css"
pic_dir = out_dir + "/" + filename + "_pic"
rel_pic_dir = "./" + filename + "_pic"

print("load json file : " + filename_json + "\n")

if not os.path.exists(out_dir):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(out_dir)

if not os.path.exists(pic_dir):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(pic_dir)


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
            if int(jon_dat["compos"][k]["height"]) > 150 and int(jon_dat["compos"][k]["width"]) > 150:
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


# htmlファイルのタブ数のカウント
tab_num = 0
# num : 次のtabの数
# pre_ui: 次は？　<div>:True, </div>:False 
tab_json={
    "num": 0,
    "pre_ui": False,
}

# html ファイルのタブを調整する
def tab_str(next_ui):
    # next_ui : 次の来るのが開始タグ(<div>など)のとき　True
    # next_ui : 次の来るのが終了タグ(</div>など)のとき　False
    if tab_json["pre_ui"] == True and next_ui == True:
        current_tab = "\t" * tab_json["num"]
        tab_json["num"] = tab_json["num"] + 1
        tab_json["pre_ui"] = True
    elif tab_json["pre_ui"] == True and next_ui == False:
        tab_json["num"] = tab_json["num"] - 2
        current_tab = "\t" * tab_json["num"]
        tab_json["pre_ui"] = False
    elif tab_json["pre_ui"] == False and next_ui == True:
        current_tab = "\t" * tab_json["num"]
        tab_json["num"] = tab_json["num"] + 1
        tab_json["pre_ui"] = True
    elif tab_json["pre_ui"] == False and next_ui == False:
        tab_json["num"] = tab_json["num"] - 1
        current_tab = "\t" * tab_json["num"]
        tab_json["pre_ui"] = False

    return current_tab

# ブロックの属性を返す
def block_prop(block_num, block_type, block_list, color, txt_size, padding):
    first_block = True
    for block in block_list:
        if first_block:
            first_block_num = block
            block_top = jon_dat["compos"][first_block_num]["position"]["row_min"]
            block_bottom = jon_dat["compos"][first_block_num]["position"]["row_max"]
            block_left = jon_dat["compos"][first_block_num]["position"]["column_min"]
            block_right = jon_dat["compos"][first_block_num]["position"]["column_max"]
            first_block = False
        
        if block_bottom < jon_dat["compos"][block]["position"]["row_max"]:
            block_bottom = jon_dat["compos"][block]["position"]["row_max"]
        
        if block_left > jon_dat["compos"][block]["position"]["column_min"]:
            block_left = jon_dat["compos"][block]["position"]["column_min"]

        if block_right < jon_dat["compos"][block]["position"]["column_max"]:
            block_right = jon_dat["compos"][block]["position"]["column_max"]
        
    response = {
        "block_num": block_num, 
        "block_type": block_type,
        "block_width_center": int((block_left + block_right)/2),
        "block_height_center": int((block_top + block_bottom)/2),
        "block_width": int((block_right - block_left)/2),
        "block_height": int((block_bottom - block_top)/2),
        "block_left": block_left, 
        "block_top": block_top, 
        "block_right": block_right, 
        "block_bottom": block_bottom, 
        "block_list": block_list,
        "color": color,
        "txt_size": int(txt_size * 0.6),
        "padding": padding,
        "div_num": 0,
        "col_num": 0,
        }

    return json.dumps(response)


def area_color(idx):
    # 色の抽出
    # 色の抽出は図形の中心ではなく、端っこにした場合。初期のころに使ったが、実際は使わず。
    #x_col = x_left + 2
    #y_col = y_top + 2
    # 色の抽出は図形のマトリックス状のドット位置の色を抽出。最も多い点数の色を背景色とする。
    # 色の検出
    # 図形の中心を計算
    x_c = int((int(jon_dat["compos"][idx]["position"]["column_max"]) + int(jon_dat["compos"][idx]["position"]["column_min"])) / 2 )
    y_c = int((int(jon_dat["compos"][idx]["position"]["row_max"]) + int(jon_dat["compos"][idx]["position"]["row_min"])) / 2 ) 
    img_width = jon_dat["compos"][idx]["width"]
    img_height = jon_dat["compos"][idx]["height"]
    #　分割数
    d_num = 7
    d_x = int(img_width / d_num)
    d_y = int(img_height / d_num)
    # 抽出ポジション初期値
    init_x_col = int(d_x / 2 + jon_dat["compos"][idx]["position"]["column_min"])
    init_y_col = int(d_y / 2 + jon_dat["compos"][idx]["position"]["row_min"])
    x_col = init_x_col
    y_col = init_y_col

    # その領域で最も多い色を見つけて、それをその領域の色とする。
    img_colors = []
    img_dict = {}
    for kx in range(d_num-1):

        for ky in range(d_num-1):
            pos = (y_col, x_col)
            img = cv2.imread(filename_img, cv2.IMREAD_UNCHANGED)
            img_list = list(img[pos])
            img_dict =  {**img_dict, **{str(kx)+str(ky) : str(img_list[0])+str(img_list[1])+str(img_list[2])}}
            img_colors.append(str(img_list[0]).zfill(3)+str(img_list[1]).zfill(3)+str(img_list[2]).zfill(3))
            y_col = y_col + d_y

        x_col = x_col + d_x
        y_col = init_y_col

    c = collections.Counter(img_colors)
    # その領域で最も多い色
    most_color = c.most_common()[0][0]
    # 【注意】色は、B G R の順で出力される
    m_color = [int(most_color[:3]), int(most_color[3:6]), int(most_color[6:])]

    return m_color


def text_color(idx):
    # 色の抽出
    # 色の抽出は図形の中心ではなく、端っこにした場合。初期のころに使ったが、実際は使わず。
    #x_col = x_left + 2
    #y_col = y_top + 2
    # 色の抽出は図形のマトリックス状のドット位置の色を抽出。最も多い点数の色を背景色とする。
    # 色の検出
    # 図形の中心を計算
    x_c = int((int(jon_dat["compos"][idx]["position"]["column_max"]) + int(jon_dat["compos"][idx]["position"]["column_min"])) / 2 )
    y_c = int((int(jon_dat["compos"][idx]["position"]["row_max"]) + int(jon_dat["compos"][idx]["position"]["row_min"])) / 2 ) 
    img_width = jon_dat["compos"][idx]["width"]
    img_height = jon_dat["compos"][idx]["height"]
    #　分割数
    d_num = 7
    d_x = int(img_width / d_num)
    d_y = int(img_height / d_num)
    # 抽出ポジション初期値
    init_x_col = int(d_x / 2 + jon_dat["compos"][idx]["position"]["column_min"])
    init_y_col = int(d_y / 2 + jon_dat["compos"][idx]["position"]["row_min"])
    x_col = init_x_col
    y_col = init_y_col

    # その領域で最も多い色を見つけて、それをその領域の色とする。
    img_colors = []
    img_dict = {}
    for kx in range(d_num-1):

        for ky in range(d_num-1):
            pos = (y_col, x_col)
            img = cv2.imread(filename_img, cv2.IMREAD_UNCHANGED)
            img_list = list(img[pos])
            img_dict =  {**img_dict, **{str(kx)+str(ky) : str(img_list[0])+str(img_list[1])+str(img_list[2])}}
            img_colors.append(str(img_list[0]).zfill(3)+str(img_list[1]).zfill(3)+str(img_list[2]).zfill(3))
            y_col = y_col + d_y

        x_col = x_col + d_x
        y_col = init_y_col

    c = collections.Counter(img_colors)
    # その領域で最も多い色
    most_color = c.most_common()[0][0]
    # 【注意】色は、B G R の順で出力される
    m_color = [int(most_color[:3]), int(most_color[3:6]), int(most_color[6:])]

    col_threshold = int((int(most_color[:3]) + int(most_color[3:6]) + int(most_color[6:]))/3)

    img_width = jon_dat["compos"][idx]["width"]
    img_height = jon_dat["compos"][idx]["height"]
    # その領域で2番目に多い色を探す
    # まず、二値化　-> 2番目に多い色を探す。それを文字の色にする
    img_colors = []
    img_dict = {}
    img_gray = cv2.imread(filename_img, cv2.IMREAD_GRAYSCALE)
    #　分割数
    d_num = 5
    d_x = int(img_width / d_num)
    d_y = int(img_height / d_num)

    # グレースケールに変換
    # 閾値の設定
    # 領域の背景によって変更する。
    if col_threshold > 180:
        threshold = 220
    else:
        threshold = 100

    # 二値化(閾値thresholdを超えた画素を255にする。)
    ret, img_thresh = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)

    x_col = init_x_col
    y_col = init_y_col
    for kx in range(d_num-1):

        for ky in range(d_num-1):
            pos = (y_col, x_col)
            img_dict =  {**img_dict, **{str(kx)+str(ky) : str(img_thresh[pos])}}
            img_colors.append(str(img_thresh[pos]))
            y_col = y_col + d_y

        x_col = x_col + d_x
        y_col = init_y_col

    c = collections.Counter(img_colors)

    if len(c) > 1:
        #二値化後も2色（白黒）だったとき
        second_color = c.most_common()[1][0]
    else:
        #二値化の結果、一色だけになったとき
        second_color = c.most_common()[0][0]

    if second_color == "255":
        txt_color = "white"
    else:
        txt_color = "black"

    return txt_color


def css_write(element, class_list):
    
    class_n = ""
    for class_name in class_list:
        class_n = class_n + " ." + class_name

    # CSS 入力   
    with open(filename_css, "a") as f2:
        f2.writelines(class_n + "{\n")
        f2.writelines("color: " + element["color"] + ";\n")
        f2.writelines("font-size: " + str(int(int(txt_height)*0.75)) + "px;\n")
        f2.writelines("}\n\n")



################################################################################################################
######                    Process Start                                                                #########
################################################################################################################

# UIエレメントのリスト
element_list = []

# JSONファイルを修正
arrange_json(filename_json)

# JSONファイルを読込
with open(filename_json, "r") as f:
    jon_dat = json.load(f)

a = json.dumps(jon_dat)
element_num = a.count('"id":')
element_cnt = 0


next_div = False
pre_row_min = 0
pre_row_max = jon_dat["compos"][0]["position"]["row_max"]
div_list = []

print("element_num = " + str(element_num))
print("############             検出された画像をファイル保存                 ########")

for i in range(element_num):
    print(i)
    if jon_dat["compos"][i]["class"] == "Image":
        x_c = int((int(jon_dat["compos"][i]["position"]["column_max"]) + int(jon_dat["compos"][i]["position"]["column_min"])) / 2 )
        y_c = int((int(jon_dat["compos"][i]["position"]["row_max"]) + int(jon_dat["compos"][i]["position"]["row_min"])) / 2 ) 

        s_width = str(jon_dat["compos"][i]["width"])
        s_height = str(jon_dat["compos"][i]["height"])

        col_left = jon_dat["compos"][i]["position"]["column_min"]
        col_right = jon_dat["compos"][i]["position"]["column_max"]
        row_top = jon_dat["compos"][i]["position"]["row_min"]
        row_bottom = jon_dat["compos"][i]["position"]["row_max"]
        
        img = cv2.imread(filename_img)
        img1 = img[row_top : row_bottom, col_left : col_right]
        cv2.imwrite(pic_dir + "/img" + str(i) + ".jpg", img1)


print("#########             element の block (div) をつくる                  ###########")
# JSONファイル内のコンテントのリスト　（最初に全コンテントを登録しておき、検出済みのものから削除していく）
content_list = list(range(element_num))

# 連続した同じサイズのテキストの番号(id)のリスト
txt_num_list = []

# JSONファイル内の最初に出てくるテキストかどうか
txt_flg = True
cnt = 0

for i in range(element_num):

    # classが画像の場合
    if jon_dat["compos"][i]["class"] == "Image":

        a_color = area_color(i)
        img_num_list = [i]

        # テキストのサイズ （これは意味がないが、テキストのリストの情報と併せるため）
        txt_size = jon_dat["compos"][i]["height"]

        padding = 0

        block_prop_response = block_prop(element_cnt, "Image", img_num_list, a_color, txt_size, padding)
        element_list.append(block_prop_response)
        element_cnt = element_cnt + 1
        content_list.remove(i)


    # classがテキストの場合
    if jon_dat["compos"][i]["class"] == "Text":

        if i in content_list:
            txt_num_list.append(i)
            content_list.remove(i)

            pre_txt_height = jon_dat["compos"][i]["height"]
            pre_txt_row_min = jon_dat["compos"][i]["position"]["row_min"]
            pre_txt_column_min = jon_dat["compos"][i]["position"]["column_min"]

            # リストにあるコンテントを全スキャン
            # 同じブロックに入れるべきか判断する
            for j in content_list:

                txt_height = jon_dat["compos"][j]["height"]
                txt_row_min = jon_dat["compos"][j]["position"]["row_min"]
                txt_column_min = jon_dat["compos"][j]["position"]["column_min"]

                # 検討中のテキストとほぼ同じサイズ、なおかつ、大きく離れていないなら、リストに番号を加える。（= 同じブロック内にあるとみなす。）
                if abs(pre_txt_height - txt_height) < 4 and abs(pre_txt_row_min - txt_row_min) < 100 and abs(pre_txt_column_min - txt_column_min) < 100:
                    # 同じブロックのリストに加える
                    txt_num_list.append(j)
                    # 検討するコンテントリストから除外する
                    content_list.remove(j)

            # テキストの文字色を求める。
            txt_color= text_color(i)

            # テキストのサイズ
            txt_size = jon_dat["compos"][i]["height"]

            # 前のリストの最後の文字列と、今回のリストの最初の文字列との間隔を求める。
            # 前のリストの最後の文字列の番号
    #        last_txt_num = int(txt_num_list[0]) - 1
            # 今回のリストの最初の文字列の番号
    #        first_txt_num = int(txt_num_list[0])
    #        padding = int(jon_dat["compos"][first_txt_num]["position"]["row_min"]) - int(jon_dat["compos"][last_txt_num]["position"]["row_max"])
    #        if padding <  0:
    #            padding = 0
            padding = 30

            block_prop_response = block_prop(element_cnt, "Text", txt_num_list, txt_color, txt_size, padding)
            element_list.append(block_prop_response)
            element_cnt = element_cnt + 1

            txt_num_list = []

            cnt = cnt+ 1

            if content_list == []:
                break

print("block_num = " + str(cnt+1))

print("==================     Blockを画面上で左上から右下に並ぶように並び替え       ==================")

# UIブロックの配置をリストで表現
# ブロック番号をリストの要素にして、リストの構成をそのまま、div, colで表現
# [[1,2],[3,4]],[5,6]
# 1と2、3と4は同じColumn。[1,2]と[3,4]、[5,6]は同じdiv

#with open(filename_element_json, mode='wt', encoding='utf-8') as fe:
#        fe.writelines(element_list)

with open(filename_element_json, mode='wt', encoding='utf-8') as fe:
    json.dump(element_list, fe, ensure_ascii=False, indent=2)


block_layout = []

first_element_flg = True
for element in element_list:

    element_json = json.loads(element)

    print("block = " + str(element_json["block_num"]))
    if first_element_flg:
        block_layout.append(element_json["block_num"])
        first_element_flg = False

    else:
        # 今検証中のブロックが、スキャンしたブロックに対してどちらがわにあるか？のフラッグ
        cnt = er.list_count(block_layout)
        idx = element_json["block_num"]
        cnt_tmp = 0
        not_in_list_flg = False
        not_in_same_row_flg = True
        in_same_row_flg = False

        for block_num0 in block_layout:
            print(block_num0)
            # 同じrow内で、どのcolに入るか調べる
            block_num0_idx = block_layout.index(block_num0)
            if isinstance(block_num0, list):
                block_list_send = block_num0
            else:
                block_list_send = [block_num0]

            block_list_return, in_same_row_flg = er.list_reorder(idx, block_list_send, element_list)

            if in_same_row_flg:
                not_in_same_row_flg = False

            block_layout.remove(block_num0)
            block_layout.insert(block_num0_idx, block_list_return)

            cnt_tmp = cnt_tmp + 1

            if block_list_send == block_list_return:
                if idx not in block_list_send:
                    not_in_list_flg = True
                else:
                    not_in_list_flg = False
                pass
            else:
                break

        # 同じrowでリストの最後につける
        if not_in_list_flg and cnt_tmp == cnt:

            if not not_in_same_row_flg:
                block_layout.append(idx)
            else:
                # 次のrowに行くべきか調べる
                print("Different row")
                block_layout = [block_layout, block_list_send]

    print(block_layout)

print("=======================   Reordered Block List    ====================")
print(block_layout)

print("======================= 左上から右下へBlock番号の付け替え ========================")
div_num = 0
col_num = 0
element_result = []
cnt = 0
for k in block_layout:
    if isinstance(k, list):
        for m in k:
            element_json = json.loads(element_list[m])
            element_json["block_num"] = cnt
            element_json["div_num"] = div_num
            element_json["col_num"] = col_num
            element_result.append(element_json)
            cnt = cnt + 1

    else:
        element_json = json.loads(element_list[k])
        element_json["block_num"] = cnt
        element_json["div_num"] = div_num
        element_json["col_num"] = col_num
        element_result.append(element_json)
        cnt = cnt + 1

    col_num = col_num + 1


print("=================      # html / css の生成      ======================")

with open(filename_html, "a") as f3:
    tb = tab_str(True)
    f3.writelines(tb + '<div class="main-inner">\n')

# 背景色を読み取る
pos = (20, 20)
img = cv2.imread(filename_img, cv2.IMREAD_UNCHANGED)
color = list(img[pos])
color_str = "#" + format(color[2], 'x').zfill(2) + format(color[1], 'x').zfill(2) + format(color[0], 'x').zfill(2)
class_list = []
class_str = ""

with open(filename_html, "w") as f3:
    f3.writelines('<!DOCTYPE html>\n')
    f3.writelines('<html lang="ja">\n')
    f3.writelines('<head><meta charset="utf-8">\n')
    f3.writelines('<title>タイトル</title>\n')
    f3.writelines('<link rel="stylesheet" href="' + filename + '.css">\n')
    f3.writelines('</head>\n')
    f3.writelines('<body bgcolor="' + color_str + '">\n')
    class_str = "main"
    class_list.append(class_str)
    tb = tab_str(True)
    f3.writelines(tb + '<' + class_str +'>\n')

a = json.dumps(element_result)
element_num = a.count('block_num') 
    

pre_div_num = 0
pre_col_num = 0
cnt = 0
for j in range(element_num):

    cnt = cnt + 1

    element = element_result[j]

    # 最初の要素か？
    if j == 0:
        with open(filename_html, "a") as f3:
            class_str = "div" + str(cnt)
            class_list.append(class_str)
            tb = tab_str(True)
            f3.writelines(tb + '<div class="' + class_str + '">\n')
        pre_div_num == element["div_num"]

        with open(filename_html, "a") as f3:
            class_str = "col" + str(cnt)
            class_list.append(class_str)
            tb = tab_str(True)
            f3.writelines(tb + '<div class="' + class_str + '">\n')
        pre_col_num == element["col_num"]

        with open(filename_css, "w") as f2:
            f2.writelines("main .div1 {\n")
            f2.writelines("\t width: 1400px;\n")
            f2.writelines("\t margin: 0 auto;\n")
            f2.writelines("\t display: -webkit-box;\n")
            f2.writelines("\t display: -ms-flexbox;\n")
            f2.writelines("\t display: flex;\n")
            f2.writelines("\t -webkit-box-align: center;\n")
            f2.writelines("\t -ms-flex-align: center;\n")
            f2.writelines("\t align-items: center;\n")
            f2.writelines("}\n")


    # 2番目以降の要素か？
    else:
        if pre_col_num == element["col_num"]:
            pass
        else:
            # 次のdivに行くとき
            if pre_col_num < element["col_num"]:
                with open(filename_html, "a") as f3:
                    class_list.pop(-1)
                    tb = tab_str(False)
                    f3.writelines(tb + '</div>\n')
                    class_str = "col" + str(cnt)
                    class_list.append(class_str)
                    tb = tab_str(True)
                    f3.writelines(tb + '<div class="' + class_str + '">\n')
        
        pre_col_num = element["col_num"]

        if pre_div_num == element["div_num"]:
            pass
        else:
            # 新しい div に移るとき
            with open(filename_html, "a") as f3:
                class_list.pop(-1)
                tb = tab_str(False)
                f3.writelines(tb + '</div>\n')
                class_list.pop(-1)
                tb = tab_str(False)
                f3.writelines(tb + '</div>\n')
                class_str = "div" + str(cnt)
                class_list.append(class_str)
                tb = tab_str(True)
                f3.writelines(tb + '<div class="' + class_str + '">\n')

                class_str = "col" + str(cnt)
                class_list.append(class_str)
                tb = tab_str(True)
                f3.writelines(tb + '<div class="' + class_str + '">\n')

            with open(filename_css, "a") as f2:
                css_str = "main"
                for class_l in class_list[1:2]:
                    css_str = css_str + " ." + class_l

                f2.writelines(css_str + " {\n")
                f2.writelines("\t width: 1000px;\n")
                f2.writelines("\t margin: 0 auto;\n")
                f2.writelines("\t display: -webkit-box;\n")
                f2.writelines("\t display: -ms-flexbox;\n")
                f2.writelines("\t display: flex;\n")
                f2.writelines("\t -webkit-box-align: center;\n")
                f2.writelines("\t -ms-flex-align: center;\n")
                f2.writelines("\t align-items: center;\n")
                f2.writelines("}\n")


        pre_div_num = element["div_num"]


    if element["block_type"] == "Image":
        with open(filename_html, "a") as f3:
            class_str = "figure-area" + str(cnt)
            class_list.append(class_str)
            tb = tab_str(True)
            f3.writelines(tb + '<div class="' + class_str + '">\n')
            img_num = element["block_list"][0]
            tb = tab_str(True)
            f3.writelines(tb + '<figure class="pc"><img src="' + rel_pic_dir + "/img" + str(img_num) + '.jpg" alt="スマートフォン表示"></figure>\n')
            class_list.pop(-1)
            tb = tab_str(False)
            f3.writelines(tb + '</div>\n')

    elif element["block_type"] == "Text":
        with open(filename_html, "a") as f3:
            class_str = "sentence-area" + str(cnt)
            class_list.append(class_str)
            tb = tab_str(True)
            f3.writelines(tb +'<div class="' + class_str + '">\n')

            with open(filename_css, "a") as f2:
                css_str = "main"
                for class_l in class_list[1:]:
                    css_str = css_str + " ." + class_l
                f2.writelines(css_str + "{\n")
                f2.writelines("\t margin-top: " + str(element["padding"]) +  "px;\n")
                f2.writelines("\t width: 100%;\n")
                f2.writelines("\t color: " + element["color"] + ";\n")
                f2.writelines("\t font-size: " + str(element["txt_size"]) + "px;\n")
                f2.writelines("}\n")

            for k in element["block_list"]:
                tb = tab_str(True)
                f3.writelines(tb + '<div>\n')
                tb = tab_str(True)
                f3.writelines(tb + jon_dat["compos"][k]["text_content"] + '\n')
                tb = tab_str(False)
                f3.writelines(tb + '</div>\n')

            class_list.pop(-1)
            tb = tab_str(False)
            f3.writelines(tb + '</div>\n')
            

with open(filename_html, "a") as f3:
    class_list.pop(-1)
    tb = tab_str(False)
    f3.writelines(tb + '</div>\n')
    tb = tab_str(False)
    f3.writelines(tb + '</div>\n')
    tb = tab_str(False)
    f3.writelines(tb + '</main>\n')
    tb = tab_str(False)
    f3.writelines(tb + '</body>\n')

print(element_list)
#print("\n")
#print(element_result)