import os
import cv2
import json
import sys
import collections
import pickle


def list_count(cnt_list):
    cnt = 0
    for i in cnt_list:
        if isinstance(i, list):
            for j in i:

                if isinstance(j, list):
                    pass
                else:
                    cnt = cnt + 1
            else:
                cnt = cnt + 1
        else:
            cnt = cnt + 1

    return cnt

# idx : 検討するブロック番号
# comp_list : 検討するブロックのリスト
# all_block : ブロックの全リスト
# return : idx のブロックが含まれたリスト
def list_reorder(idx, comp_list, all_block):

    result_list = []

    block_idx_json = json.loads(all_block[idx])
    list_in_flg = False
    # 同じrowにあるかどうかのflg
    in_same_row_flg = False

    for i in comp_list:

        block_in_json = json.loads(all_block[i])

        if abs(block_in_json["block_left"] - block_idx_json["block_left"]) < 150:
            # 同じcolumnに入っている -> 順番を検出
            if block_in_json["block_top"] > block_idx_json["block_bottom"] and abs(block_in_json["block_top"] - block_idx_json["block_bottom"]) < 100:

                result_list.append(idx)
                result_list.append(i)
                list_in_flg = True

        if not list_in_flg:
            result_list.append(i)

        if abs(block_in_json["block_top"] - block_idx_json["block_top"]) < 50:
            print("Same row")
            print("same top = " + str(block_in_json["block_num"] ) + "   in_num = " + str(block_idx_json["block_num"] ))
            # 同じrowにある
            in_same_row_flg = True


    if abs(block_in_json["block_left"] - block_idx_json["block_left"]) < 100:
        # 同じcolumnに入っている -> 順番を検出
        if block_in_json["block_bottom"] < block_idx_json["block_top"] and abs(block_in_json["block_bottom"] - block_idx_json["block_top"]) < 60:
            # block_in より後ろにある。
            if not list_in_flg:
                result_list.append(idx)

    print(in_same_row_flg)
    return result_list, in_same_row_flg


