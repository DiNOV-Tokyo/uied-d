import cv2
import json

# filename without extension
filename = "hc"
filename_img = "./data/input/" + filename + ".jpg"
filename_json = "./data/output/merge/" + filename + ".json"
filename_html = "./data/output/merge/" + filename + ".html"
filename_css = "./data/output/merge/" + filename + ".css"
with open(filename_json, "r") as f:
    jon_dat = json.load(f)

a = json.dumps(jon_dat)
element_num = a.count('"id":') - 2

with open(filename_html, "w") as f3:
    f3.writelines('<!DOCTYPE html>\n')
    f3.writelines('<html lang="ja">\n')
    f3.writelines('<head><meta charset="utf-8">\n')
    f3.writelines('<title>タイトル</title>\n')
    f3.writelines('<link rel="stylesheet" href="' + filename + '.css">\n')
    f3.writelines('</head><body>\n')

with open(filename_css, "w") as f2:
    f2.writelines(".pbox{\n")
    f2.writelines("display: flex;\n")
    f2.writelines("border: solid 1px white;\n")
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
    cv2.imwrite("./pic/out_sample1" + str(i) + ".jpg", img1)

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
            f3.writelines('<div class="pbox">\n')
            for div_list_idx in div_list:
                print(div_list_idx)
                # 色の検出
                # 図形の中心を計算
                x_c = int((int(jon_dat["compos"][div_list_idx]["position"]["column_max"]) + int(jon_dat["compos"][div_list_idx]["position"]["column_min"])) / 2 )
                y_c = int((int(jon_dat["compos"][div_list_idx]["position"]["row_max"]) + int(jon_dat["compos"][div_list_idx]["position"]["row_min"])) / 2 ) 
                x_left = int(jon_dat["compos"][div_list_idx]["position"]["column_min"])
                y_top = int(jon_dat["compos"][div_list_idx]["position"]["row_min"])

                f3.writelines('<div class="square' + str(div_list_idx) + '" style="position: absolute; top: ' + str(y_top) + 'px; left:' + str(x_left) + 'px; "></div>\n')

                pos = (y_c, x_c)
                print(pos)
                img = cv2.imread(filename_img, cv2.IMREAD_UNCHANGED)
                color = list(img[pos])
#                print(color)
                #print(color[0])
                s_width = str(jon_dat["compos"][div_list_idx]["width"])
                s_height = str(jon_dat["compos"][div_list_idx]["height"])

                print("No." + str(div_list_idx) + ":  width=" + s_width + " height=" + s_height + " Pos_x=" + str(x_c) + " Pos_y=" + str(y_c))
                
                with open(filename_css, "a") as f2:
                    f2.writelines(".square" + str(div_list_idx) + "{\n")
                    f2.writelines("width:" + s_width + "px;\n" )
                    f2.writelines("height:" + s_height + "px;\n" )
                    color_str = "background: #" + format(color[2], 'x').zfill(2) + format(color[1], 'x').zfill(2) + format(color[0], 'x').zfill(2) + ";\n"
#                    color_str = "background: #ffffff;\n"
                    f2.writelines(color_str)
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
