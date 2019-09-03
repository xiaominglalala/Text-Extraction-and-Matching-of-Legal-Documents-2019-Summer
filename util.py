###util
import json
import re
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def easy_case1(dict,easy_dict,error):
    dict_new = {}
    for key, value in dict.items():
        try:
            if (re.findall(r"驳回[^。]*", value['裁判结果']) != []):
                easy_dict.update({key:re.findall(r"驳回[^。]*", value['裁判结果'])})
            else:
                dict_new.update({key:value})
        except:
            error.update({key:value})
    return dict_new

def easy_case2(dict,easy_dict,error):
    dict_new = {}
    for key, value in dict.items():
        try:
            if (re.findall(r"撤回[^。]*", value['裁判结果']) != []):
                easy_dict.update({key:re.findall(r"撤回[^。]*", value['裁判结果'])})
            else:
                dict_new.update({key:value})
        except:
            error.update({key:value})
    return dict_new

# def complex_case(dict, appeal, reply):
#     match_list_appeal = [0,0,0,0]#[赔偿，诉讼费，改判，判罚错误]
#     a = ['裁判结果','本院认为']
#     for key, value in dict.items():
#         if '原告诉称' in value.keys():
#             if re.findall(r"诉讼费", value['原告诉称']) != []:
#             if re.findall(r"诉讼费", value['原告诉称']) != []:
#                 match_list_appeal[1] = 1
#                 if re.findall('撤销|维持|变更.*' + instance_no, value['裁判结果']) != []:
#                     remove_list.append(key)
#                     match_success_pair += 1
#
#     for i in remove_list:
#         dict_crime_second_instances.pop(i)

def empty(c):
    return (c != [[]] and c != [] and c != [[],[]] and c != [[],[],[]] and c !=[[],[],[],[]] )

def find_appeal_class(input):
    all_class = ['赔偿/偿还', '诉讼费', '责任', '改判']
    c_0 = []
    c_1 = []
    c_2 = []
    c_3 = []
    #c_4 = []
    for value in input:
        c_0.append(re.findall(r"支付|返还|偿还|赔偿|分割共同财产",value))
        c_1.append(re.findall(r"诉讼费|受理费|涉诉费",value))
        c_2.append(re.findall(r"离婚|承担连带责任",value))
        c_3.append(re.findall(r"改判|撤销原判|依法撤销|依法改判|撤销原审判决|撤销[^。]*号民事判决|原审判决[^。]*存在[^。]*错误", value))
        #c_4.append(re.findall(r"申请再审",value))
    match_list_appeal = [empty(c_0), empty(c_1), empty(c_2), empty(c_3)]
    return match_list_appeal



def find_reply_class(input):
    all_class = ['赔偿/偿还', '诉讼费', '责任' ,'改判']
    c_0 = []
    c_1 = []
    c_2 = []
    c_3 = []
    #c_4 = []
    c_0.append(re.findall(r"支付|返还|偿还|赔偿", input))
    c_1.append(re.findall(r"诉讼费|受理费|涉诉费", input))
    c_2.append(re.findall(r"离婚|承担连带责任", input))
    c_3.append(re.findall(r"撤销|维持|变更", input))
    #c_4.append(re.findall(r"发回[^。]*法院重审|法院再审本案", input))
    match_list_reply = [empty(c_0), empty(c_1), empty(c_2), empty(c_3)]
    return match_list_reply

def match(appeal, reply):
    for i in range(len(appeal)):
        if appeal[i] == True and reply[i] == False:
            return False
    return True

def main(dict_civil_instances, l_1, l_2, complex_appeal, class_appeal, class_reply, _format, error_a,error_b):
    for key, value in dict_civil_instances.items():
        if l_1 in value.keys() and l_2 in value.keys():
            complex_appeal[key] = re.findall(_format,value[l_1])
            class_appeal[key] = find_appeal_class(complex_appeal[key])
            # complex_reply[key] = re.findall( r"", value[l_2])
            class_reply[key] = find_reply_class(value[l_2])
            if match(class_appeal[key], class_reply[key]) == False:
                error_a.update({key: value})
            else:
                continue
        else:
            error_b.update({key: value})

def solve_error_xxx(error_xxx,error_xx,complex_appeal,class_appeal,class_reply,pop_list):
    for key, value in error_xxx.items():
        if "审理经过" in value.keys() and "裁判结果" in value.keys():
            complex_appeal[key] = "改判"
            class_appeal[key] = [False, False, False, True]
            class_reply[key] = find_reply_class(value["裁判结果"])
            if match(class_appeal[key], class_reply[key]) == False:
                error_xx.update({key: value})
            pop_list.append(key)
        else:
            continue

    for i in pop_list:
        error_xxx.pop(i)


def solve_error_x(error_x,error_xx,complex_appeal,class_appeal,class_reply,pop_list,label,_format):
    for key, value in error_x.items():
        if label in value.keys() and "本院认为" in value.keys():
            complex_appeal[key] = re.findall(_format,value[label])
            class_appeal[key] = find_appeal_class(complex_appeal[key])
            class_reply[key] = find_reply_class(value["本院认为"])
            if match(class_appeal[key], class_reply[key]) == False:
                error_xx.update({key: value})
            pop_list.append(key)
        else:
            continue

    for i in pop_list:
        error_x.pop(i)