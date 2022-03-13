import cv2
import json

filename_img = "./data/output/ip/web.jpg"
filename = "./data/output/ip/web.json"
filename_html = "./data/output/ip/web.html"
filename_css = "./data/output/ip/web.css"
with open(filename, "r") as f:
    jon_dat = json.load(f)

with open(filename_html, "w") as f3:
    f3.writelines('<!DOCTYPE html>\n')
    f3.writelines('<html lang="ja">\n')
    f3.writelines('<head><meta charset="utf-8">\n')
    f3.writelines('<title>サイトタイトル</title>\n')
    f3.writelines('<link rel="stylesheet" href="cw.css">\n')
    f3.writelines('</head><body>\n')

with open(filename_css, "w") as f2:
    f2.writelines(".pbox{\n")
    f2.writelines("display: flex;\n")
    f2.writelines("border: solid 1px white;\n")
    f2.writelines("padding: 5px;\n")
    f2.writelines("}\n")

next_div = False
pre_row_min = 0
pre_row_max = jon_dat["compos"][0]["row_max"]
div_list = []
diff = 20
for i in range(5):
    print("  next: " + str(jon_dat["compos"][i+1]["row_min"]) + "   now: " + str(jon_dat["compos"][i]["row_min"]))
    next_min = jon_dat["compos"][i+1]["row_min"]
    now_min = jon_dat["compos"][i]["row_min"]
    now_height = jon_dat["compos"][i]["height"]

    # div 次の段
    if next_min > now_min + now_height:

#    if jon_dat["compos"][i+1]["row_min"] > jon_dat["compos"][i]["row_max"]:
        div_list.append(i)
        print(div_list)

        with open(filename_html, "a") as f3:
            f3.writelines('<div class="pbox">\n')
            for div_list_idx in div_list:

                # 色の検出
                # 図形の中心を計算
                x_c = int((int(jon_dat["compos"][div_list_idx]["column_max"]) + int(jon_dat["compos"][div_list_idx]["column_min"])) / 2 )
                y_c = int((int(jon_dat["compos"][div_list_idx]["row_max"]) + int(jon_dat["compos"][div_list_idx]["row_min"])) / 2 ) 

#                f3.writelines('<img src="rect.jpg" width="' + str(jon_dat["compos"][i]["width"]) + '" height="' + str(jon_dat["compos"][i]["height"]) + '">\n')
                f3.writelines('<div class="square' + str(div_list_idx) + '" style="position: relative; left:' + str(x_c) + 'px; "></div>\n')

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
                    if color_str = "background: #ffffff;\n":
                        color_str = "background: #555555;":
                    f2.writelines(color_str)
                    f2.writelines("}\n\n")



            f3.writelines("</div>\n")

        # 比較する基準を入替
        pre_row_max = jon_dat["compos"][i]["row_min"]
        # リストをリセット
        div_list = []
        print("Next div")
    # div 同じ段
    else:
        # リストに追加
        div_list.append(i)


with open(filename_html, "a") as f3:
    f3.writelines('</body>')
