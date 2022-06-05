import os
import cv2
import json
import shutil
import sys
import collections
import pickle

def back_color(filename_img):
    # 背景色を読み取る
    pos = (20, 20)
    img = cv2.imread(filename_img, cv2.IMREAD_UNCHANGED)
    color = list(img[pos])
    color_str = "#" + format(color[2], 'x').zfill(2) + format(color[1], 'x').zfill(2) + format(color[0], 'x').zfill(2)

    return color_str

def area_color(filename_img, idx, jon_dat):
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


def text_color(filename_img, idx, jon_dat):
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
    d_num = 7
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
