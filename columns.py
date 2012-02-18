#!/usr/bin/env python

def columnize_list(list,col_nb):    
    rows_dict = {}
    if len(list)==0:
        return []
    for i in range(0,len(list)):
        item      = list[i]
        row_index = i/col_nb
        if not rows_dict.has_key(row_index):
            rows_dict[row_index] = []
        rows_dict[row_index].append(item)
    rows = []
    for row_index in range(min(rows_dict.keys()),max(rows_dict.keys())+1):
        rows.append(rows_dict[row_index])
    return rows
        
    