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
def deep_list_reorder(idx, comp_list, all_block):

    print("================= comp_list =================")
    print(comp_list)

    result_list = []

    block_idx_json = json.loads(all_block[idx])
    in_list_flg = False

    # 前のループでの is_forehead_flg
    pre_is_forehead_flg
    # 調査した要素数
    no_cnt = 0
    # 調査するリスト内の総要素数
    no_elemt = len(comp_list)

    for i in comp_list:

        # 同じcolumnにあるかどうかのflg
        in_same_col_flg = False
        # 調査中の要素より前にあるかどうかのflg
        is_forehead_flg = False

        block_comp_json = json.loads(all_block[i])

        no_cnt = no_cnt + 1

        # 同じcolumnに入っているか？
        if abs(block_comp_json["block_left"] - block_idx_json["block_left"]) < 150:

            in_same_col_flg = True

            # 同じcolumnに入っている -> 順番を検出
            if block_comp_json["block_top"] > block_idx_json["block_bottom"] and abs(block_comp_json["block_top"] - block_idx_json["block_bottom"]) < 300:
                # 調査中のブロックが、ループを回して走査しているブロックより前にある
                is_forehead_flg = True

            elif block_comp_json["block_bottom"] < block_idx_json["block_top"] and abs(block_comp_json["block_bottom"] - block_idx_json["block_top"]) < 300:
                # 調査中のブロックが、ループを回して走査しているブロックより後ろにある
                is_forehead_flg = False

        if in_same_col_flg and not is_forehead_flg and no_cnt == no_elemt:
            result_list.append(i)
            result_list.append(idx)
        elif in_same_col_flg and not pre_is_forehead_flg and is_forehead_flg:
            result_list.append(idx)
            result_list.append(i)
        else:
            result_list.append(i)

        pre_is_forehead_flg = is_forehead_flg

        print("i = " + str(i) + "  idx=" + str(idx) + "  cnt=" + str(no_cnt) + "  no_elemt=" + str(no_elemt)) 
        print("in_same_flg=" + str(in_same_col_flg) + "    is_forehead_flg" + str(is_forehead_flg))
        print(result_list)
                
        in_same_row_flg = False

        n=input()
    return result_list, in_same_row_flg, in_same_col_flg



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
    # 調査中の要素より前にあるかどうかのflg
    is_forehead_flg = False
    # 調査した要素数
    no_cnt = 0
    # 調査するリスト内の総要素数
    no_elemt = len(comp_list)

    for i in comp_list:

        block_comp_json = json.loads(all_block[i])

        no_cnt = no_cnt + 1

        # 同じcolumnに入っているか？
        if abs(block_comp_json["block_left"] - block_idx_json["block_left"]) < 150:

            in_same_col_flg = True

            # 同じcolumnに入っている -> 順番を検出
            if block_comp_json["block_top"] > block_idx_json["block_bottom"] and abs(block_comp_json["block_top"] - block_idx_json["block_bottom"]) < 300:
                # 調査中のブロックが、ループを回して走査しているブロックより前にある
                is_forehead_flg = True

                if idx not in result_list and not in_list_flg:
                    print("i = " + str(i))
                    result_list.append(idx)
                    print(" ###  FRONT ####")
                    print(result_list)
                    in_list_flg = True
                if i not in result_list and not in_list_flg: 
                    print("i = " + str(i))
                    result_list.append(i)
                    print(" ###  FRONT ####")
                    print(result_list)
#                    n = input()
                    in_list_flg = True

            elif block_comp_json["block_bottom"] < block_idx_json["block_top"] and abs(block_comp_json["block_bottom"] - block_idx_json["block_top"]) < 300:
                is_forehead_flg = False
                print(" ###  HRER ####")
                # 調査中のブロックが、ループを回して走査しているブロックより後ろにある
                if i not in result_list:
                    result_list.append(i)
                    result_list.append(idx)
                    print(result_list)
                    #n = input()

                    in_list_flg = True
                #break

        print("in_list_flg = " + str(in_list_flg))
        if not in_list_flg:
            # まだリストに入れていない　＝　同じColumnにあって、調査中のブロックが、ループを回して走査しているブロックより後ろにある
            result_list.append(i)
            print("add to result_list")
            print(result_list)

        print(result_list)
        print("Top check : " + str(block_comp_json["block_num"] ) + " of " + str(block_comp_json["block_top"]) + "   and  " + str(block_idx_json["block_num"]) + "  of " + str(block_idx_json["block_top"]))
        # 同じrowにあるかチェック
        # if abs(block_comp_json["block_top"] - block_idx_json["block_top"]) < 50:
        if ((block_comp_json["block_height_center"] < block_idx_json["block_bottom"]) and (block_comp_json["block_height_center"] > block_idx_json["block_top"])) or ((block_idx_json["block_height_center"] < block_comp_json["block_bottom"]) and (block_idx_json["block_height_center"] > block_comp_json["block_top"])) :
            print("Same row")
            print("same top = " + str(block_comp_json["block_num"] ) + "   in_num = " + str(block_idx_json["block_num"] ))
            # 同じrowにある
            in_same_row_flg = True

    #　同じColumnにあるか？
    if abs(block_comp_json["block_left"] - block_idx_json["block_left"]) < 100:
        # 同じcolumnに入っている -> 順番を検出
        if block_comp_json["block_bottom"] < block_idx_json["block_top"] and abs(block_comp_json["block_bottom"] - block_idx_json["block_top"]) < 80:
            # block_in より後ろにある。
            print("same col, append last")
            if not in_list_flg:
                result_list.append(idx)

    print("======== Return result==========")
    print(result_list)
    print("======== Return result==========")
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



# idx : 検討するブロック番号
# comp_list : 検討するブロックのリスト
# all_block : ブロックの全リスト
# return : idx のブロックが含まれたリスト

# Col のリスト生成

def col_list_reorder(idx, comp_list, all_block):

    result_list = []

    # 検討する要素を読み込む
    block_idx_json = json.loads(all_block[idx])

    in_list_flg = False
    # 同じrowにあるかどうかのflg
    in_same_row_flg = False
    # 同じcolumnにあるかどうかのflg
    in_same_col_flg = False
    # 調査中の要素より前にあるかどうかのflg
    is_forehead_flg = False
    
    # 調査した要素数
    no_cnt = 0
    # 調査するCol リスト内の総要素数
    no_elemt = len(comp_list)

    for i in comp_list:

        block_comp_json = json.loads(all_block[i])

        no_cnt = no_cnt + 1

        # 同じcolumnに入っているか？
        if abs(block_comp_json["block_left"] - block_idx_json["block_left"]) < 150:

            # 同じcolumnに入っている -> 順番を検出
            if block_comp_json["block_top"] > block_idx_json["block_bottom"] and abs(block_comp_json["block_top"] - block_idx_json["block_bottom"]) < 300:
                # 調査中のブロックが、ループを回して走査しているブロックより前にある
                is_forehead_flg = True
                in_same_col_flg = True

            elif block_comp_json["block_bottom"] < block_idx_json["block_top"] and abs(block_comp_json["block_bottom"] - block_idx_json["block_top"]) < 300:
                # 調査中のブロックが、ループを回して走査しているブロックより後ろにある
                is_forehead_flg = False
                in_same_col_flg = True
        
        # 同じcolumnに入っていないけれども、先にある。
        else:
            is_forehead_flg = True
            in_same_col_flg = False

    return in_same_row_flg, in_same_col_flg, is_forehead_flg
#    return result_list, in_same_row_flg, in_same_col_flg, is_forehead_flg
