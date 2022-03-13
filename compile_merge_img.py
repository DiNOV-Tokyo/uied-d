import os
import cv2
import json
import sys

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
element_num = a.count('"id":') - 2

# 背景色を読み取る
pos = (20, 20)
img = cv2.imread(filename_img, cv2.IMREAD_UNCHANGED)
color = list(img[pos])
color_str = "#" + format(color[2], 'x').zfill(2) + format(color[1], 'x').zfill(2) + format(color[0], 'x').zfill(2)
print("color=" + str(color_str))

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

    print("No." + str(i) + ":  width=" + s_width + " height=" + s_height + " Pos_x=" + str(x_c) + " Pos_y=" + str(y_c))

for i in range(element_num):
    print("No. " + str(i) + "  next: " + str(jon_dat["compos"][i+1]["position"]["row_min"]) + "   now: " + str(jon_dat["compos"][i]["position"]["row_min"]))
    next_min = jon_dat["compos"][i+1]["position"]["row_min"]
    now_min = jon_dat["compos"][i]["position"]["row_min"]
    now_height = jon_dat["compos"][i]["height"]

    # div 次の段
    if next_min > now_min + now_height:

#    if jon_dat["compos"][i+1]["position"]["row_min"] > jon_dat["compos"][i]["position"]["row_max"]:
        div_list.append(i)
        print(div_list)

        with open(filename_html, "a") as f3:
            z_inded = 0
            f3.writelines('<div class="pbox">\n')
            for div_list_idx in div_list:
                print(div_list_idx)
                # 色の検出
                # 図形の中心を計算
                x_c = int((int(jon_dat["compos"][div_list_idx]["position"]["column_max"]) + int(jon_dat["compos"][div_list_idx]["position"]["column_min"])) / 2 )
                y_c = int((int(jon_dat["compos"][div_list_idx]["position"]["row_max"]) + int(jon_dat["compos"][div_list_idx]["position"]["row_min"])) / 2 ) 
                x_left = int(jon_dat["compos"][div_list_idx]["position"]["column_min"])
                y_top = int(jon_dat["compos"][div_list_idx]["position"]["row_min"])

                # 現状では、画像は、SeekBar で検出される。SeekBarのとき、画像を表示するようにする。
                if jon_dat["compos"][div_list_idx]["class"] == "SeekBar":
                    #f3.writelines('<div><img src="./pic/out_sample1' + str(div_list_idx) + '.jpg" style="position: absolute; top: ' + str(y_top) + 'px; left:' + str(x_left) + 'px; "></div>\n')
                    f3.writelines('<div class="square' + str(div_list_idx) + '">' + '<img src="' + rel_pic_dir + '/out_sample1' + str(div_list_idx) + '.jpg" style="top: ' + str(y_top) + 'px; left:' + str(x_left) + 'px; "></div>\n')
                    z_index = 100
                elif jon_dat["compos"][div_list_idx]["class"] == "Spinner":
                    #f3.writelines('<div><img src="./pic/out_sample1' + str(div_list_idx) + '.jpg" style="position: absolute; top: ' + str(y_top) + 'px; left:' + str(x_left) + 'px; "></div>\n')
                    f3.writelines('<div class="square' + str(div_list_idx) + '">' + '<img src="' + rel_pic_dir + '/out_sample1' + str(div_list_idx) + '.jpg" style="top: ' + str(y_top) + 'px; left:' + str(x_left) + 'px; "></div>\n')
                    z_index = 80
                else:
#                    f3.writelines('<div class="square' + str(div_list_idx) + '" style="position: absolute; top: ' + str(y_top) + 'px; left:' + str(x_left) + 'px; ">\n')
                    f3.writelines('<div class="square' + str(div_list_idx) + '" style="top: ' + str(y_top) + 'px; left:' + str(x_left) + 'px; ">\n')
                    z_index = 10


                if jon_dat["compos"][div_list_idx]["class"] == "Text":
                    f3.writelines(jon_dat["compos"][div_list_idx]["text_content"] + '\n')
                    z_index = 200

                f3.writelines('</div>\n')

                # 色の抽出
                # 色の抽出は図形の中心ではなく、端っこにした。
                x_c = x_left + 2
                y_c = y_top + 2
                # 色の抽出は図形の中心ではなく、端っこにした。
                img_width = jon_dat["compos"][div_list_idx]["width"]
                img_height = jon_dat["compos"][div_list_idx]["height"]
                #　分割数
                d_num = 6 
                d_x = int(img_width / d_num)
                d_y = int(img_height / d_num)
                # 抽出ポジション初期値
                #init_x_col = int(d_x / 2)
                #init_y_col = int(d_y / 2)
                init_x_col = int(d_x / 2 + jon_dat["compos"][div_list_idx]["position"]["column_min"])
                init_y_col = int(d_y / 2 + jon_dat["compos"][div_list_idx]["position"]["row_min"])
                x_col = init_x_col
                y_col = init_y_col

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

                import collections
                print(img_colors)
                c = collections.Counter(img_colors)
                most_color = c.most_common()[0][0]
                color = [int(most_color[:3]), int(most_color[3:6]), int(most_color[6:])]
                print(color)

                # もっとも単純な色抽出
#                pos = (y_c, x_c)
#                img = cv2.imread(filename_img, cv2.IMREAD_UNCHANGED)
#                color = list(img[pos])

                # CSS make and save
                s_width = str(jon_dat["compos"][div_list_idx]["width"])
                s_height = str(jon_dat["compos"][div_list_idx]["height"])
                s_left = str(int(jon_dat["compos"][div_list_idx]["position"]["column_min"]))
                s_top = str(int(jon_dat["compos"][div_list_idx]["position"]["row_min"]))

                print("No." + str(div_list_idx) + ":  width=" + s_width + " height=" + s_height + " Pos_x=" + s_left + " Pos_y=" + s_top)
                
                with open(filename_css, "a") as f2:
                    f2.writelines(".square" + str(div_list_idx) + "{\n")
#                    f2.writelines("opacity: 0.25;\n" )
                    f2.writelines("position: absolute;\n" )
                    f2.writelines("top:" + s_top + "px;\n" )
                    f2.writelines("left:" + s_left + "px;\n" )
                    f2.writelines("width:" + s_width + "px;\n" )
                    f2.writelines("height:" + s_height + "px;\n" )
                    color_str = "background: #" + format(color[2], 'x').zfill(2) + format(color[1], 'x').zfill(2) + format(color[0], 'x').zfill(2) + ";\n"
                    color_str = "background: rgba(" + format(color[2]).zfill(3) + ","  + format(color[1]).zfill(3) + "," + format(color[0]).zfill(3) + ", 0.95 );\n"
#                    color_str = "background: rgba(" + format(color[2], 'o').zfill(3) + ","  + format(color[1], 'o').zfill(3) + "," + format(color[0], 'o').zfill(3) + ", 0.55 );\n"
                    f2.writelines(color_str)
                    f2.writelines("color: black;\n")
                    f2.writelines("font-size: " + str(int(int(s_height)*0.76)) + "px;\n")
                    f2.writelines("z-index: " + str(z_index) + ";\n")
                    f2.writelines("}\n\n")

 
            f3.writelines("</div>\n")

        # 比較する基準を入替
        #pre_row_max = jon_dat["compos"][i]["position"]["row_min"]
        # リストをリセット
        div_list = []
        print("Next div")
    # div 同じ段
    else:
        # リストに追加
        div_list.append(i)


with open(filename_html, "a") as f3:
    f3.writelines('</body>')