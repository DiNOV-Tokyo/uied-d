import os
import cv2
import json
import sys
import collections

args = sys.argv
# filename without extension
filename = "br"
filename = args[1]
filename_img = "./data/input/" + filename + ".jpg"
filename_json = "./data/output/merge/" + filename + ".json"
out_dir = "./data/output/merge/" + filename
filename_html = out_dir + "/" + filename + ".html"
filename_css = out_dir + "/" + filename + ".css"
pic_dir = out_dir + "/" + filename + "_pic"
rel_pic_dir = "./" + filename + "_pic"

if not os.path.exists(out_dir):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(out_dir)

if not os.path.exists(pic_dir):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(pic_dir)

with open(filename_json, "r") as f:
    jon_dat = json.load(f)

a = json.dumps(jon_dat)
element_num = a.count('"id":') -1

# 背景色を読み取る
pos = (20, 20)
img = cv2.imread(filename_img, cv2.IMREAD_UNCHANGED)
color = list(img[pos])
color_str = "#" + format(color[2], 'x').zfill(2) + format(color[1], 'x').zfill(2) + format(color[0], 'x').zfill(2)
print("color=" + str(color_str))
print(element_num)
with open(filename_html, "w") as f3:
    f3.writelines('<!DOCTYPE html>\n')
    f3.writelines('<html lang="ja">\n')
    f3.writelines('<head><meta charset="utf-8">\n')
    f3.writelines('<title>タイトル</title>\n')
    f3.writelines('<link rel="stylesheet" href="' + filename + '.css">\n')
    f3.writelines('</head><body bgcolor="' + color_str + '">\n')

with open(filename_css, "w") as f2:
    f2.writelines(".pbox{\n")
    f2.writelines("display: flex;\n")
    f2.writelines("border: solid 1px transparent;\n")
    f2.writelines("padding: 5px;\n")
    f2.writelines("}\n")

next_div = False
pre_row_min = 0
pre_row_max = jon_dat["compos"][0]["position"]["row_max"]
div_list = []

for i in range(element_num):
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
    cv2.imwrite(pic_dir + "/out_sample1" + str(i) + ".jpg", img1)


# 連続した同じサイズのテキストの番号(id)のリスト
txt_num_list = []

# JSONファイル内の最初に出てくるテキストかどうか
txt_flg = True
cnt = 0

for i in range(element_num):

    next_min = jon_dat["compos"][i+1]["position"]["row_min"]
    now_min = jon_dat["compos"][i]["position"]["row_min"]
    now_height = jon_dat["compos"][i]["height"]

    # まずは、classがテキストの場合のみを考慮する。
    if jon_dat["compos"][i]["class"] == "Text":
        print("txt")
        if txt_flg:
            pre_txt_height = jon_dat["compos"][i]["height"]
            txt_flg = False
            print("pre_txt" + str(pre_txt_height))

        txt_height = jon_dat["compos"][i]["height"]
        # ひとつ前のテキストとほぼ同じサイズなら、リストに番号を加える。
        if abs(pre_txt_height - txt_height) < 5:
            txt_num_list.append(i)

        # ひとつ前のテキストと異なるサイズなら、１つ前までのテキストをhtmlファイルに書き出し。新たにリストを作る。
        else:
            print(txt_num_list)

            # 前のリストの最後の文字列と、今回のリストの最初の文字列との間隔を求める。
            # 前のリストの最後の文字列の番号
            last_txt_num = int(txt_num_list[0]) - 1
            # 今回のリストの最初の文字列の番号
            first_txt_num = int(txt_num_list[0])
            d_height = int(jon_dat["compos"][first_txt_num]["position"]["row_min"]) - int(jon_dat["compos"][last_txt_num]["position"]["row_max"])
            if d_height <  0:
                d_height = 0

            # HTML 入力
            with open(filename_html, "a") as f3:
               f3.writelines('<div class="sentence-area' + str(cnt) + '">\n')

               for j in txt_num_list:
                    f3.writelines('\t <div>\n')
                    f3.writelines('\t' + jon_dat["compos"][j]["text_content"] + '\n')
                    f3.writelines('\t </div>\n')
                    print(jon_dat["compos"][j]["text_content"])

               f3.writelines('</div>\n')
               
            # CSS 入力   
            with open(filename_css, "a") as f2:
                f2.writelines(".sentence-area" + str(cnt) + "{\n")
#                f2.writelines("position: absolute;\n" )
#                f2.writelines("top:" + s_top + "px;\n" )
#                f2.writelines("left:" + s_left + "px;\n" )
#                f2.writelines("width:" + s_width + "px;\n" )
#                f2.writelines("height:" + s_height + "px;\n" )
#                color_str = "background: rgba(" + format(color[2]).zfill(3) + ","  + format(color[1]).zfill(3) + "," + format(color[0]).zfill(3) + ", 0.95 );\n"
#                f2.writelines(color_str)
#                f2.writelines("color: " + txt_color + ";\n")
                f2.writelines("margin-top: " + str(d_height) + "px;\n")
                f2.writelines("color: green;\n")
                f2.writelines("font-size: " + str(int(int(txt_height)*0.75)) + "px;\n")
#                f2.writelines("z-index: " + str(z_index) + ";\n")
                f2.writelines("}\n\n")
  

            cnt = cnt+ 1

            txt_num_list = []
            txt_num_list.append(i)
            pre_txt_height = jon_dat["compos"][i]["height"]


