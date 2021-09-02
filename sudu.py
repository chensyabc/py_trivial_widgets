# Total set of 1 to 9
total_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9])


# Verify if shudu is resolved
def verify_sudu(sudu_arr_verify):
    is_resolved = True
    for i in range(9):
        sudu_line = sudu_arr_verify[i]
        sudu_line_remove_dup = list(set(sudu_line))
        if 0 in sudu_line_remove_dup:
            is_resolved = False
            break
        if len(sudu_line_remove_dup) < 9:
            is_resolved = False
            break
    return is_resolved


def get_sudu_possible_answer(sudu_arr_verify):
    unresolved = {}
    # Row Go Through
    for i in range(9):
        sudu_row = sudu_arr_verify[i]
        if 0 in sudu_row:
            for j in range(len(sudu_row)):
                if sudu_row[j] == 0:
                    unresolved.update({(i, j): list(set(total_set - set(sudu_row)))})
    # Column Go Through
    for i in range(9):
        sudu_column = []
        for k in range(9):
            sudu_column.append(sudu_arr_verify[k][i])
        if 0 in sudu_column:
            for j in range(len(sudu_column)):
                if sudu_column[j] == 0:
                    # only update since Row go Through will add all possibilities
                    if (j, i) in unresolved:
                        possible_from_column = list(set(total_set - set(sudu_column)))
                        possible_merge = list(set(possible_from_column) & set(unresolved[(j, i)]))
                        unresolved.update({(j, i): possible_merge})
    # Square Go Through
    for i in range(9):
        sudu_column = []
        row_base = i - i % 3
        column_base = (i % 3)*3
        for k in range(3):
            for m in range(3):
                sudu_column.append(sudu_arr_verify[row_base + k][column_base + m])
        if 0 in sudu_column:
            possible_from_column = list(set(total_set - set(sudu_column)))
            for n in range(3):
                for p in range(3):
                    # only update since Row go Through will add all possibilities
                    if (row_base + n, column_base + p) in unresolved:
                        possible_merge = list(set(possible_from_column) & set(unresolved[(row_base + n, column_base + p)]))
                        unresolved.update({(row_base + n, column_base + p): possible_merge})
    # print('------- Possible Answer: ', unresolved)
    arrange_sudu_possible_answer(unresolved)
    # print('Arrange Possible Answer: ', unresolved)
    return unresolved


def arrange_sudu_possible_answer(unresolved):
    for possible_answer in unresolved.keys():
        row_num = possible_answer[0]
        column_num = possible_answer[1]
        # Remove for other columns possible if only one answer for this line
        if len(unresolved[possible_answer]) == 1:
            for i in range(9):
                try:
                    if column_num != i and (row_num, i) in unresolved and unresolved[possible_answer][0] in unresolved[(row_num, i)] and len(unresolved[(row_num, i)]) > 1:
                        unresolved[(row_num, i)].remove(unresolved[possible_answer][0])
                        # print('Log in arrange_sudu_possible_answer: ', (row_num, i), ' remove value ', unresolved[possible_answer][0], ' from ', possible_answer, ' to be ', unresolved[(row_num, i)])
                except:
                    print('Error in arrange_sudu_possible_answer: ', (row_num, i), possible_answer)


# If this cell only has one possible answer, then make it this answer
def replace_sudu_answer_onlyone(sudu_arr_replace, unresolved=None):
    if not unresolved:
        unresolved = get_sudu_possible_answer(sudu_arr_replace)
    i = 0
    resolved = []
    for item in unresolved.keys():
        row_num = item[0]
        column_num = item[1]
        if len(unresolved[item]) == 1:
            i += 1
            resolved.append(item)
            sudu_arr_replace[row_num][column_num] = unresolved[item][0]
    # print('replace_sudu_answer_onlyone count: ', i, ' resolved: ', resolved, sep='')
    return sudu_arr_replace


# Process row: if there's a number(s) in all row unresolved cells, then this cell's answer is that number(s).
# This will make possible answer scope smaller or directly get answer of unresolved cell(s).
def replace_sudu_answer_complex(sudu_arr_replace, unresolved=None):
    if not unresolved:
        unresolved = get_sudu_possible_answer(sudu_arr_replace)
    count = 0
    resolved = []
    for i in range(9):
        line_all_answers = []
        for j in range(9):
            if (i, j) in unresolved:
                # get this line all column answers
                line_all_answers.extend(unresolved[(i, j)])
        each_line = {}
        for answer in line_all_answers:
            if answer in each_line.keys():
                each_line.update({answer: each_line[answer]+1})
            else:
                each_line.update({answer: 1})
        ordered_each_line = sorted(each_line.items(), key=lambda e: e[1])
        for item in ordered_each_line:
            if item[1] == 1:
                value = item[0]
                for k in range(9):
                    if (i, k) in unresolved and value in unresolved[(i, k)]:
                        count += 1
                        resolved.append(((i, k), value))
                        sudu_arr_replace[i][k] = value
        # find the only one number of this line
    # print('replace_sudu_answer_complex count: ', count, ' resolved: ', resolved, sep='')
    return sudu_arr_replace


# Process row: if there's a number(s) in all column unresolved cells, then this cell's answer is that number(s).
# This will make possible answer scope smaller or directly get answer of unresolved cell(s).
def replace_sudu_answer_complex_column(sudu_arr_replace, unresolved=None):
    if not unresolved:
        unresolved = get_sudu_possible_answer(sudu_arr_replace)
    count = 0
    resolved = []
    for i in range(9):
        line_all_answers = []
        for j in range(9):
            if (j, i) in unresolved:
                # get this line all column answers
                line_all_answers.extend(unresolved[(j, i)])
        each_line = {}
        for answer in line_all_answers:
            if answer in each_line.keys():
                each_line.update({answer: each_line[answer]+1})
            else:
                each_line.update({answer: 1})
        ordered_each_line = sorted(each_line.items(), key=lambda e: e[1])
        for item in ordered_each_line:
            if item[1] == 1:
                value = item[0]
                for k in range(9):
                    if (k, i) in unresolved and value in unresolved[(k, i)]:
                        count += 1
                        resolved.append(((k, i), value))
                        sudu_arr_replace[k][i] = value
        # find the only one number of this line
    # print('replace_sudu_answer_complex column count: ', count, ' resolved: ', resolved, sep='')
    return sudu_arr_replace


# Process row: if there's a number(s) in the square(3*3) unresolved cells, then this cell's answer is that number(s).
# This will make possible answer scope smaller or directly get answer of unresolved cell(s).
def replace_sudu_answer_complex_square(sudu_arr_replace, unresolved=None):
    if not unresolved:
        unresolved = get_sudu_possible_answer(sudu_arr_replace)
    count = 0
    resolved = []
    for i in range(9):
        line_all_answers = []
        row_base = i - i % 3
        column_base = (i % 3)*3
        # get this line all column answers
        for j in range(3):
            for k in range(3):
                if (row_base + j, column_base + k) in unresolved:
                    line_all_answers.extend(unresolved[(row_base + j, column_base + k)])
        each_line = {}
        for answer in line_all_answers:
            if answer in each_line.keys():
                each_line.update({answer: each_line[answer]+1})
            else:
                each_line.update({answer: 1})
        ordered_each_line = sorted(each_line.items(), key=lambda e: e[1])
        for item in ordered_each_line:
            if item[1] == 1:
                value = item[0]
                for j in range(3):
                    for k in range(3):
                        if (row_base + j, column_base + k) in unresolved and value in unresolved[(row_base + j, column_base + k)]:
                            count += 1
                            resolved.append(((row_base + j, column_base + k), value))
                            sudu_arr_replace[row_base + j][column_base + k] = value
        # find the only one number of this line
    # print('replace_sudu_answer_complex square count: ', count, ' resolved: ', resolved, sep='')
    return sudu_arr_replace


def sudu_try_answer(sudu_arr_need_resolve, i, possible_answer=None):
    if i > 15:
        return
    try_resolve = replace_sudu_answer_onlyone(sudu_arr_need_resolve)
    try_resolve = replace_sudu_answer_complex(sudu_arr_need_resolve)
    try_resolve = replace_sudu_answer_complex_column(sudu_arr_need_resolve)
    try_resolve = replace_sudu_answer_complex_square(sudu_arr_need_resolve)
    is_resolved = verify_sudu(sudu_arr_need_resolve)
    # print('Is Sudu Resolved? ', is_resolved, ', Round ', i + 1, sep='')
    if not is_resolved:
        sudu_try_answer(try_resolve, i+1)
    else:
        for line in sudu_arr_need_resolve:
            print(*line, sep=' ')


if __name__ == '__main__':
    sudu_arr = []
    # for i in range(9):
    #     current_arr = list(map(int, input().split()))
    #     sudu_arr.append(current_arr)
    sudu_arr = [[6, 1, 0, 4, 3, 0, 0, 0, 0],
        [3, 9, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 6, 0, 0, 3],
        [0, 0, 8, 6, 0, 2, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 4, 0, 0],
        [0, 6, 7, 3, 0, 0, 5, 0, 8],
        [0, 0, 0, 1, 6, 0, 0, 0, 2],
        [8, 0, 0, 9, 2, 0, 0, 6, 0],
        [4, 0, 0, 5, 7, 0, 0, 0, 0]]
    sudu_try_answer(sudu_arr, 0)
