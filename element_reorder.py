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
    in_list_flg = False
    # 同じrowにあるかどうかのflg
    in_same_row_flg = False
    # 同じcolumnにあるかどうかのflg
    in_same_col_flg = False

    for i in comp_list:

        block_in_json = json.loads(all_block[i])

        if abs(block_in_json["block_left"] - block_idx_json["block_left"]) < 150:
            print(comp_list)
            print("idx = " + str(idx))
            in_same_col_flg = True
            # 同じcolumnに入っている -> 順番を検出
            if block_in_json["block_top"] > block_idx_json["block_bottom"] and abs(block_in_json["block_top"] - block_idx_json["block_bottom"]) < 100:
                # 調査中のブロックが、ループを回して走査しているブロックより前にある
                result_list.append(idx)
                result_list.append(i)
                in_list_flg = True

        if not in_list_flg:
            # まだリストに入れていない　＝　同じColumnにあって、調査中のブロックが、ループを回して走査しているブロックより後ろにある
            result_list.append(i)

        print("Top check : " + str(block_in_json["block_num"] ) + " of " + str(block_in_json["block_top"]) + "   and  " + str(block_idx_json["block_num"]) + "  of " + str(block_idx_json["block_top"]))
        # 同じrowにあるかチェック
        # if abs(block_in_json["block_top"] - block_idx_json["block_top"]) < 50:
        if ((block_in_json["block_height_center"] < block_idx_json["block_bottom"]) and (block_in_json["block_height_center"] > block_idx_json["block_top"])) or ((block_idx_json["block_height_center"] < block_in_json["block_bottom"]) and (block_idx_json["block_height_center"] > block_in_json["block_top"])) :
            print("Same row")
            print("same top = " + str(block_in_json["block_num"] ) + "   in_num = " + str(block_idx_json["block_num"] ))
            # 同じrowにある
            in_same_row_flg = True

    #　同じColumnにあるか？
    if abs(block_in_json["block_left"] - block_idx_json["block_left"]) < 100:
        # 同じcolumnに入っている -> 順番を検出
        if block_in_json["block_bottom"] < block_idx_json["block_top"] and abs(block_in_json["block_bottom"] - block_idx_json["block_top"]) < 60:
            # block_in より後ろにある。
            if not in_list_flg:
                result_list.append(idx)

    print(result_list)
    return result_list, in_same_row_flg, in_same_col_flg


# リストの中にリストがあるかチェック
def isNextList(next_list):

    next_list_flg = False

    for in_list in next_list:

        if isinstance(in_list, list):

            next_list_flg = True

    return next_list_flg


# リストの中に要素があるかチェック
def isInList(chk_list, idx):

    in_list_flg = False

    for in_list in chk_list:

        if isinstance(in_list, list):

            for in_list1 in in_list:

                if isinstance(in_list1, list):
                    for in_list2 in in_list1:
                        if in_list2 == idx:
                            in_list_flg = True
                else:
                    if in_list1 == idx:
                        in_list_flg = True

        else:
            if in_list == idx:
                in_list_flg = True

    return in_list_flg
