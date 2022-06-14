import json
import element_reorder as er


# UIブロックの配置をリストで表現
# ブロック番号をリストの要素にして、リストの構成をそのまま、div, colで表現
# [[1,2],[3,4]],[5,6]
# 1と2、3と4は同じColumn。[1,2]と[3,4]、[5,6]は同じdiv

#with open(filename_element_json, mode='wt', encoding='utf-8') as fe:
#        fe.writelines(element_list)

def layout_arrange(element_list):
    block_layout = []

    first_element_flg = True
    for element in element_list:

        next_loop_flg = False
        element_json = json.loads(element)

        cnt = len(block_layout)
        print("========================================================================================")
        print("block = " + str(element_json["block_num"]) + "  Scan START : cnt = " + str(cnt))
        # 一番最初のエレメントをまずリストに加える。
        if first_element_flg:
            block_layout.append(element_json["block_num"])
            first_element_flg = False

        else:
    #        cnt = len(block_layout)
            idx = element_json["block_num"]
            cnt_tmp = 0
            not_in_list_flg = False
            not_in_same_row_flg = True
            in_same_row_flg = False


            for block_num0 in block_layout:
                print(block_num0)

                block_num0_idx = block_layout.index(block_num0)
                # 同じrow内で、どのcolに入るか調べる
                if isinstance(block_num0, list):
                    
                    cnt_tmp1 = 0
                    cnt1 = er.list_count(block_num0)
                    print("Show block")
                    print(block_num0)
                    print(type(block_num0))

                    # リストの中にリストがあるか？　あれば、もう一回リストに入って作業
                    if er.isNextList(block_num0):
                        # 入れ子リストのカウンター
                        in_cnt = 0
                        for block_num1 in block_num0:

                            print(block_num0)
                            if isinstance(block_num1, list):
                                print("Deepest-LIST SCAN START")
                                block_list_send = block_num1
                                block_num1_idx = block_num0.index(block_num1)

                                block_list_return, in_same_row_flg, in_same_col_flg = er.deep_list_reorder(idx, block_list_send, element_list)
                                cnt_tmp1 = cnt_tmp1 + 1
                                cnt_tmp = cnt_tmp + 1
                                in_cnt = in_cnt + 1

                                if in_same_row_flg:
                                    not_in_same_row_flg = False

                                if block_list_send == block_list_return:
                                    if idx not in block_list_send:
                                        not_in_list_flg = True
                                    else:
                                        not_in_list_flg = False
                                    print("PASS")
                                    pass
                                else:
                                    next_loop_flg = True
                                    block_num0.remove(block_num1)
                                    block_num0.insert(block_num1_idx, block_list_return)
                                    print(block_layout)
                                    break
                                print("Deepest-LIST SCAN END")

                        # 同じrowでリストの最後につける
                        if not_in_list_flg and cnt_tmp1 == cnt1 and in_same_col_flg:
                            #cnt_tmp = cnt_tmp + 1
                            next_loop_flg = True
                            block_num0.append(idx)
                            break

                    else:
                        print("NOT Deepest-LIST SCAN START")

                        block_list_send = block_num0

                        block_list_return, in_same_row_flg, in_same_col_flg = er.list_reorder(idx, block_list_send, element_list)
                        print("block_list_return : " + str(idx) + "    in_same_row_flg :" + str(in_same_row_flg) + "    in_same_col_flg : " + str(in_same_col_flg))
                        cnt_tmp = cnt_tmp + 1

                        if in_same_row_flg:
                            not_in_same_row_flg = False

                        block_layout.remove(block_num0)
                        block_layout.insert(block_num0_idx, block_list_return)


                        print("HHHHHHHHH")
                        print(block_layout)
                        if block_list_send == block_list_return:
                            if idx not in block_list_send:
                                not_in_list_flg = True
                            else:
                                not_in_list_flg = False
                            pass
                        else:
                            next_loop_flg = True
                            not_in_list_flg = False
                            break

                    print("block_layout")
                    if next_loop_flg:
    #                    next_loop_flg = False
                        break

                else:
                    block_list_send = [block_num0]

                    block_list_return, in_same_row_flg, in_same_col_flg = er.list_reorder(idx, block_list_send, element_list)
                    cnt_tmp = cnt_tmp + 1

                    if in_same_row_flg:
                        not_in_same_row_flg = False

                    block_layout.remove(block_num0)
                    block_layout.insert(block_num0_idx, block_list_return)


                    if block_list_send == block_list_return:
                        if idx not in block_list_send:
                            not_in_list_flg = True
                        else:
                            not_in_list_flg = False
                        pass
                    else:
                        not_in_list_flg = False
                        break

    #            if next_loop_flg:
    #3                next_loop_flg = False
    #                break

    #        print("block_layout")
    #        if next_loop_flg:
    #            next_loop_flg = False
    #            break

            print("idx = " + str(idx) + "  not_in_list_flg = " + str(not_in_list_flg) + "   cnt_tmp = " + str(cnt_tmp) + "  cnt = " + str(cnt))
            # 同じrowでリストの最後につける
            if not_in_list_flg and cnt_tmp >= cnt and not er.isInList(block_layout, idx):
    #        if not_in_list_flg and cnt_tmp == cnt:
                print(block_layout)

                # 同じrowにあるとき
                if not not_in_same_row_flg:
                    print("[end] Same row")
                    #cnt_tmp = cnt_tmp + 1
                    #block_layout.append([idx])
                    if len(block_layout) == 1:
                        block_layout.append([idx])
                    else:
                        # block_layoutの形で次のレイアウトがきまる。
                        # [[*], [*]],[*] の時、[[*], [*]],[[*],[*]] にしたい。
                        # [*], [*], [*] の時、[*], [*], [*], [*] にしたい。
                        
                        least_2_block = str(block_layout[len(block_layout)-2])
                        print(least_2_block)
                        if ']]' in least_2_block:
                            print("LEAST 2 Block")
                            least_block = block_layout[len(block_layout)-1]
                            print(least_block)
                            block_layout.remove(least_block)
                            print(block_layout)
                            block_layout.append([least_block, [idx]])
                        else:
                            print("Simple append")
                            block_layout.append([idx])
                else:
                    # 次のrowに行くとき
                    print("[end] Different row")
                    block_layout = [block_layout, [idx]]

        print("idx = " + str(element_json["block_num"]))
        print(block_layout)


    if "[[[" in str(block_layout):
        pass
    else:
        block_layout = [block_layout]


    return block_layout



def layout_arrange2(element_list):
    block_layout = []

    first_element_flg = True
    for element in element_list:

        next_loop_flg = False
        element_json = json.loads(element)

        cnt = len(block_layout)
        print("========================================================================================")
        print("block = " + str(element_json["block_num"]) + "  Scan START : cnt = " + str(cnt))
        # 一番最初のエレメントをまずリストに加える。
        if first_element_flg:
            block_layout.append([element_json["block_num"]])
            print(block_layout)
            n=input()
            first_element_flg = False

        else:
    #        cnt = len(block_layout)
            idx = element_json["block_num"]
            cnt_tmp = 0
            not_in_list_flg = False
            not_in_same_row_flg = True
            in_same_row_flg = False


            for block_num0 in block_layout:
                print(block_num0)

                block_num0_idx = block_layout.index(block_num0)
                # 同じrow内で、どのcolに入るか調べる
                if isinstance(block_num0, list):
                    
                    cnt_tmp1 = 0
                    cnt1 = er.list_count(block_num0)
                    print("Show block")
                    print(block_num0)
                    print(type(block_num0))

                    # リストの中にリストがあるか？　あれば、もう一回リストに入って作業
                    if er.isNextList(block_num0):
                        # 入れ子リストのカウンター
                        in_cnt = 0
                        for block_num1 in block_num0:

                            print(block_num0)
                            if isinstance(block_num1, list):
                                print("Deepest-LIST SCAN START")
                                block_list_send = block_num1
                                block_num1_idx = block_num0.index(block_num1)

                                block_list_return, in_same_row_flg, in_same_col_flg = er.deep_list_reorder(idx, block_list_send, element_list)
                                cnt_tmp1 = cnt_tmp1 + 1
                                cnt_tmp = cnt_tmp + 1
                                in_cnt = in_cnt + 1

                                if in_same_row_flg:
                                    not_in_same_row_flg = False

                                if block_list_send == block_list_return:
                                    if idx not in block_list_send:
                                        not_in_list_flg = True
                                    else:
                                        not_in_list_flg = False
                                    print("PASS")
                                    pass
                                else:
                                    next_loop_flg = True
                                    block_num0.remove(block_num1)
                                    block_num0.insert(block_num1_idx, block_list_return)
                                    print(block_layout)
                                    break
                                print("Deepest-LIST SCAN END")

                        # 同じrowでリストの最後につける
                        if not_in_list_flg and cnt_tmp1 == cnt1 and in_same_col_flg:
                            #cnt_tmp = cnt_tmp + 1
                            next_loop_flg = True
                            block_num0.append(idx)
                            break

                    else:
                        print("NOT Deepest-LIST SCAN START")

                        block_list_send = block_num0

                        block_list_return, in_same_row_flg, in_same_col_flg = er.list_reorder(idx, block_list_send, element_list)
                        print("block_list_return : " + str(idx) + "    in_same_row_flg :" + str(in_same_row_flg) + "    in_same_col_flg : " + str(in_same_col_flg))
                        cnt_tmp = cnt_tmp + 1

                        if in_same_row_flg:
                            not_in_same_row_flg = False

                        block_layout.remove(block_num0)
                        block_layout.insert(block_num0_idx, block_list_return)


                        print("HHHHHHHHH")
                        print(block_layout)
                        if block_list_send == block_list_return:
                            if idx not in block_list_send:
                                not_in_list_flg = True
                            else:
                                not_in_list_flg = False
                            pass
                        else:
                            next_loop_flg = True
                            not_in_list_flg = False
                            break

                    print("block_layout")
                    if next_loop_flg:
    #                    next_loop_flg = False
                        break

                else:
                    block_list_send = [block_num0]

                    block_list_return, in_same_row_flg, in_same_col_flg = er.list_reorder(idx, block_list_send, element_list)
                    cnt_tmp = cnt_tmp + 1

                    if in_same_row_flg:
                        not_in_same_row_flg = False

                    block_layout.remove(block_num0)
                    block_layout.insert(block_num0_idx, block_list_return)


                    if block_list_send == block_list_return:
                        if idx not in block_list_send:
                            not_in_list_flg = True
                        else:
                            not_in_list_flg = False
                        pass
                    else:
                        not_in_list_flg = False
                        break

    #            if next_loop_flg:
    #3                next_loop_flg = False
    #                break

    #        print("block_layout")
    #        if next_loop_flg:
    #            next_loop_flg = False
    #            break

            print("idx = " + str(idx) + "  not_in_list_flg = " + str(not_in_list_flg) + "   cnt_tmp = " + str(cnt_tmp) + "  cnt = " + str(cnt))
            # 同じrowでリストの最後につける
            if not_in_list_flg and cnt_tmp >= cnt and not er.isInList(block_layout, idx):
    #        if not_in_list_flg and cnt_tmp == cnt:
                print(block_layout)

                # 同じrowにあるとき
                if not not_in_same_row_flg:
                    print("[end] Same row")
                    #cnt_tmp = cnt_tmp + 1
                    #block_layout.append([idx])
                    if len(block_layout) == 1:
                        block_layout.append([idx])
                    else:
                        # block_layoutの形で次のレイアウトがきまる。
                        # [[*], [*]],[*] の時、[[*], [*]],[[*],[*]] にしたい。
                        # [*], [*], [*] の時、[*], [*], [*], [*] にしたい。
                        
                        least_2_block = str(block_layout[len(block_layout)-2])
                        print(least_2_block)
                        if ']]' in least_2_block:
                            print("LEAST 2 Block")
                            least_block = block_layout[len(block_layout)-1]
                            print(least_block)
                            block_layout.remove(least_block)
                            print(block_layout)
                            block_layout.append([least_block, [idx]])
                        else:
                            print("Simple append")
                            block_layout.append([idx])
                else:
                    # 次のrowに行くとき
                    print("[end] Different row")
                    block_layout = [block_layout, [idx]]

        print("idx = " + str(element_json["block_num"]))
        print(block_layout)


    if "[[[" in str(block_layout):
        pass
    else:
        block_layout = [block_layout]


    return block_layout



def layout_number(element_list, block_layout):

    div_num = 0
    col_num = 0
    element_result = []
    cnt = 0
#    print("len block = " + str(len(block_layout)))
    for k in block_layout:
#        print(k)
        if isinstance(k, list):
#            print("List")
#            print(k)
            for m in k:
                if isinstance(m, list):
                    for n in m:
                        element_json = json.loads(element_list[n])
                        element_json["block_num"] = cnt
                        element_json["div_num"] = div_num
                        element_json["col_num"] = col_num
                        element_result.append(element_json)
                        cnt = cnt + 1
    #                col_num = col_num + 1
 #                   print("In deep col")

                else:
                    element_json = json.loads(element_list[m])
                    element_json["block_num"] = cnt
                    element_json["div_num"] = div_num
                    element_json["col_num"] = col_num
                    element_result.append(element_json)
                    cnt = cnt + 1
#                    print("In deep col 2")
                col_num = col_num + 1

  #          print("div=" + str(div_num) + "  col=" + str(col_num))
  #          print(k)
        else:
   #         print("Non-List")
   #         print(k)
            element_json = json.loads(element_list[k])
            element_json["block_num"] = cnt
            element_json["div_num"] = div_num
            element_json["col_num"] = col_num
            element_result.append(element_json)
            cnt = cnt + 1

 #           print("div=" + str(div_num) + "  col=" + str(col_num))
  #          print(k)

        div_num = div_num + 1
        col_num = 0

    return element_result


def all_layout_reorder(element_list):
    block_layout = []

    first_element_flg = True
    for element in element_list:

        element_json = json.loads(element)

        # 一番最初のエレメントをまずリストに加える。
        if first_element_flg:
            block_layout.append([[element_json["block_num"]]])
            first_element_flg = False
            print(block_layout)
        else:
            idx = element_json["block_num"]
            # すでに作ったblockの中にあるかどうか？
            is_in_block_flg = False

            cnt_row = 0
            no_row = len(block_layout)
            # block_layout の row を検討していく
            for block_rows in block_layout:
                print("\n\n==========================================")
                print("今から ============")
                print(block_rows)
                print("について、==========")
                print("\t block_row idx= " + str(idx))
                print("を調べます。============\n")
                #n=input()
                cnt_row = cnt_row + 1

                is_in_block_flg, block_layout_return, in_same_row_flg, in_same_col_flg, is_forehead_flg = row_layout_reorder(idx, block_rows, element_list, is_in_block_flg)
                

                print("diff _ all")
                print("[cnt_row / no_row] ; is_in_block_flg, in_same_row_flg, in_same_col_flg, is_forehead_flg  :  [" + str(cnt_row) + " / " + str(no_row) + "] ;    " + str(is_in_block_flg) + " : " + str(in_same_row_flg) + " : " + str(in_same_col_flg) + " : " + str(is_forehead_flg) )
                print(block_layout_return)
                print(block_rows)
                print(block_layout_return != block_rows)

                if block_layout_return != block_rows:
                    index0 = block_layout.index(block_rows)
                    block_layout.remove(block_rows)
                    block_layout.insert(index0, block_layout_return)
                else:
                    if not in_same_row_flg and is_forehead_flg:
                        print("[cnt_row / no_row] ; is_in_block_flg, in_same_row_flg, in_same_col_flg, is_forehead_flg  :  [" + str(cnt_row) + " / " + str(no_row) + "] ;    " + str(is_in_block_flg) + " : " + str(in_same_row_flg) + " : " + str(in_same_col_flg) + " : " + str(is_forehead_flg) )

                        print("ここに入っている？")
                        #n = input()
                        if cnt_row != no_row:
                            if not is_in_block_flg:
                                index0 = block_layout.index(block_rows)
                                block_layout.remove(block_rows)
                                block_layout.insert(index0, [[idx]])
                                is_in_block_flg = True
                                block_layout.insert(index0+1, block_rows)
                        else:
                            block_layout.remove(block_rows)
                            if not is_in_block_flg:
                                block_layout.append([[idx]])
                                is_in_block_flg = True
                            block_layout.append(block_rows)
                    elif not in_same_row_flg and cnt_row == no_row:
                        #block_layout.append(block_layout_return)
                        if not is_in_block_flg:
                            block_layout.append([[idx]])
                            is_in_block_flg = True

                print("最終Blockの途中経過  block_row_layout end " + str(idx))
                print(block_layout)
                #n=input()

    return block_layout


def row_layout_reorder(idx, block_rows, element_list, is_in_block_flg):
    
    block_layout_row = []
    
    cnt_col = 0
    no_col = len(block_rows)
    print(block_rows)
    #n=input()
    # block_layout の cols を検討していく
    for block_col in block_rows:
        
        cnt_col = cnt_col + 1
        print("考える　colはこちら ---------------")
        print(block_col)
        print("\t idx は　" + str(idx) + "-----------")
        
        is_in_block_flg, block_layout_return, in_same_row_flg, in_same_col_flg, is_forehead_flg = col_layout_reorder(idx, block_col, element_list, is_in_block_flg)

        print("diff _ row")
        print("[cnt_col / no_col] ; is_in_block_flg, in_same_row_flg, in_same_col_flg, is_forehead_flg  :  [" + str(cnt_col) + " / " + str(no_col) + "] ;    " + str(is_in_block_flg) + " : " + str(in_same_row_flg) + " : " + str(in_same_col_flg) + " : " + str(is_forehead_flg) )
        print(block_layout_return)
        print(block_col)
        print(block_layout_return == block_col)

        if block_layout_return != block_col and not is_forehead_flg:
            block_layout_row.append(block_layout_return)
            print("Row block のここです １")
        elif block_layout_return != block_col and is_forehead_flg:
            block_layout_row.remove(block_col)
            block_layout_row.append(block_layout_return)
            block_layout_row.append(block_col)
            print("Row block のここです ２")
        else:
            if in_same_row_flg and cnt_col == no_col and not is_forehead_flg:
                block_layout_row.append(block_layout_return)
                if not is_in_block_flg:
                    block_layout_row.append([idx])
                    is_in_block_flg = True
                print("Row block のここです ３")
            elif in_same_row_flg and cnt_col == no_col and is_forehead_flg:
                if not is_in_block_flg:
                    block_layout_row.append([idx])
                    is_in_block_flg = True
                block_layout_row.append(block_layout_return)
                print("Row block のここです ４")

#            elif not in_same_row_flg and cnt_col == no_col and is_forehead_flg:
#                print("ここです。")
#                if not is_in_block_flg:
#                    block_layout_row.append([idx])
#                    is_in_block_flg = True
#                block_layout_row.append(block_layout_return)
            elif in_same_row_flg and is_forehead_flg:
                if not is_in_block_flg:
                    block_layout_row.append([idx])
                    is_in_block_flg = True
                block_layout_row.append(block_layout_return)
                print("Row block のここです ５")
            elif not in_same_row_flg and is_forehead_flg:
                print("[cnt_col / no_col] ; is_in_block_flg, in_same_row_flg, in_same_col_flg, is_forehead_flg  :  [" + str(cnt_col) + " / " + str(no_col) + "] ;    " + str(is_in_block_flg) + " : " + str(in_same_row_flg) + " : " + str(in_same_col_flg) + " : " + str(is_forehead_flg) )

                print("Row block のここです ６")
                block_layout_row.append(block_col)
                #break
            else:
                block_layout_row.append(block_col)
                print("Row block のここです ７")


        print("Row block の途中経過= ")
        print(block_layout_row)
        #n = input()

    print("return block_layout row = ")
    print(block_layout_row)
    #n=input()

    return is_in_block_flg, block_layout_row, in_same_row_flg, in_same_col_flg, is_forehead_flg


# idx : 検討するブロック番号
# block_col : 検討するブロックのリスト
# element_list : ブロックの全リスト
# return : idx のブロックが含まれたリスト

# Col のリスト生成

def col_layout_reorder(idx, block_col, element_list, is_in_block_flg):

    block_layout_col = []

    # 検討する要素を読み込む
    block_idx_json = json.loads(element_list[idx])

  #  print("idx = " + str(idx))

    # 同じrowにあるかどうかのflg
    in_same_row_flg = False
    # 同じcolumnにあるかどうかのflg
    in_same_col_flg = False
    # 調査中の要素より前にあるかどうかのflg
    is_forehead_flg = False
    # 前回の調査で、調査中の要素より前にあるかどうかのflg
    pre_is_forehead_flg = False

    # 調査した要素数
    no_cnt = 0
    # 調査するCol リスト内の総要素数
    print(block_col)
    no_elemt = len(block_col)

    for i in block_col:

        block_comp_json = json.loads(element_list[i])

        no_cnt = no_cnt + 1

        # 以下の評価方法、評価基準は、要見直し！！！

        # 同じrowに入っているか？ この判断は難しい・・・・
#        if abs(block_comp_json["block_height_center"] - block_idx_json["block_height_center"]) < 200:
        if (abs(block_comp_json["block_height_center"] - block_idx_json["block_height_center"]) < 200) or (abs(block_comp_json["block_top"] - block_idx_json["block_top"]) < 30) or (abs(block_comp_json["block_bottom"] - block_idx_json["block_bottom"]) < 30):
            #if (block_comp_json["block_bottom"] > block_idx_json["block_height_center"]) and (block_comp_json["block_top"] < block_idx_json["block_height_center"]):
            #    in_same_row_flg = True
            #if (block_comp_json["block_height_center"] < block_idx_json["block_bottom"]) and (block_comp_json["block_height_center"] > block_idx_json["block_top"]):
            #    in_same_row_flg = True
            in_same_row_flg = True
            diff_val = 80
#            if (block_comp_json["block_bottom"] + 150 < block_idx_json["block_height_center"]) or (block_comp_json["block_top"] > 150 + block_idx_json["block_height_center"]):
            if (block_comp_json["block_top"] - block_idx_json["block_bottom"]) > diff_val or (block_idx_json["block_top"] - block_comp_json["block_bottom"]) > diff_val :
                in_same_row_flg = False

        else:
            in_same_row_flg = False

        # 同じcolumnに入っているか？
        if (abs(block_comp_json["block_left"] - block_idx_json["block_left"]) < 40) or (abs(block_comp_json["block_width_center"] - block_idx_json["block_width_center"]) < 120) :
#        if (abs(block_comp_json["block_width_center"] - block_idx_json["block_width_center"]) < 120) or (abs(block_comp_json["block_left"] - block_idx_json["block_left"]) < 40):
            in_same_col_flg = True

            # 前後関係の検出
            if block_comp_json["block_top"] > block_idx_json["block_bottom"] and abs(block_comp_json["block_top"] - block_idx_json["block_bottom"]) < 300:
                # 調査中のブロックが、ループを回して走査しているブロックより前にある
                is_forehead_flg = True
                print("ここか？　１")

            elif block_comp_json["block_bottom"] < block_idx_json["block_top"] and abs(block_comp_json["block_bottom"] - block_idx_json["block_top"]) < 300:
                # 調査中のブロックが、ループを回して走査しているブロックより後ろにある
                is_forehead_flg = False
        
        # 同じcolumnに入っていなくて、先にある。
        elif (block_comp_json["block_top"] > block_idx_json["block_bottom"]) and (block_comp_json["block_right"] > block_idx_json["block_left"]): 
            is_forehead_flg = True
            print("ここか？　２")
            print("comp = " + str(block_comp_json["block_num"]) + "   idx = " + str(block_idx_json["block_num"]))
            print("top = " + str(block_comp_json["block_top"]) + "   Bottom = " + str(block_idx_json["block_bottom"]))
            #n = input()
        # 同じcolumnに入っていなくて、先にある。
        elif (block_comp_json["block_left"] > block_idx_json["block_right"]) and (block_comp_json["block_bottom"] > block_idx_json["block_bottom"]) :
            is_forehead_flg = True
            print("ここか？　３")

        # 同じcolumnに入っていなくて、後にある。
        else:
            is_forehead_flg = False
            in_same_col_flg = False


        # block_layout に要素を入力

        # 全col要素を検査終わっていないが、すでに要素の順番が確定したときの処理
        # 同じrow,　同じcol, 前後が確定したとき
        if in_same_row_flg and in_same_col_flg and not pre_is_forehead_flg and is_forehead_flg:
            block_layout_col.append(idx) 
            block_layout_col.append(i) 
            is_in_block_flg = True
            break

        block_layout_col.append(i) 

        pre_is_forehead_flg = is_forehead_flg


    # block_layout に要素を入力

    # 全col要素を検査終わったときの処理
    # 同じrow,　同じcolにあり、
    if in_same_row_flg and in_same_col_flg and no_cnt == no_elemt and not is_in_block_flg:
        # block_layout の中をすべて検査し終わったとき
        if not is_forehead_flg:
            # 後にあり・・・
            block_layout_col.append(idx) 
            is_in_block_flg = True
        else:
            # 前にあり・・・
            block_layout_col.remove(i) 
            block_layout_col.append(idx) 
            block_layout_col.append(i) 
            is_in_block_flg = True

    print("return block_layout col = ")
    print(block_layout_col)
    print("==========================")

    return is_in_block_flg, block_layout_col, in_same_row_flg, in_same_col_flg, is_forehead_flg
