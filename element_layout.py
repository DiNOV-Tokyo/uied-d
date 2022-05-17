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

                                block_list_return, in_same_row_flg, in_same_col_flg = er.list_reorder(idx, block_list_send, element_list)
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