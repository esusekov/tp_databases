__author__ = 'egor'

def column_to_list(column):
    result_list = []
    for el in column:
        result_list.append(el[0])
    return result_list