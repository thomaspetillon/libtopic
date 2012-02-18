#!/usr/bin/env python
#Topic list module
#Provide helper for list management

# Returns a list containing only distinct elements from the input list
def get_distinct_list(list):
    result = []
    for item in list:
        if not result.__contains__(item):
            result.append(item)
    return result

# Flattens a list (each element of the input list is a list, output is a one-dimension list)
def flatten_list(list):
    result = []
    for inner_list in list:
        for element in inner_list:
            result.append(element)
    return result

# Makes a list from a single instance (that can be null)
def make_list(source):
    list = []
    if source:
        list.append(source)
    return list

# Returns a list containing only distinct elements from the two input list, joined
def join_lists(list1,list2):
    results = []
    for obj in list1:
        if not obj in results:
            results.append(obj)
    for obj in list2:
        if not obj in results:
            results.append(obj)
    return results

        
def order_list_by_field(list,field_name,asc=True):
    dict = {}
    for item in list:
        field_value = getattr(item,field_name)
        if not field_value in dict.keys():
            dict[field_value] = []
        dict[field_value].append(item)
    items = dict.items()
    items.sort()
    if not asc:
        items.reverse()
    result = []
    for key,value in items:
        result.extend(value)
    return result

