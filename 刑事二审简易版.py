#Inital format
import json
import re
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import csv

dict_crime_second_instances = {} #{'id':{'当事人':'', '审理经过':'',  '本院认为':'', '裁判结果':''}...}
dict_crime_second_instance_tmp = {'docName': '','上诉人诉称':'', '审理经过':'',  '本院认为':'', '裁判结果':'','公诉机关称':''} #提取模板
filename = u'C://Users//Administrator//Desktop//深度学习入门//把手网数据集//6.1课题四案件评查与减假暂//把手案例网数据_small//dataset_small//criminal.json'
file = open(filename,'r', encoding = 'utf-8')

while 1:
    line = file.readline()
    if not line:
        break
    try: # right = 646
        if(json.loads(line)['procedureId'] == "二审"):
            #print(json.loads(line).keys())
            dict_crime_second_instances[json.loads(line)['id']] = {} #{...{'id':{}}}
            for key in dict_crime_second_instance_tmp.keys():
                #防止不匹配导致提取信息不足
                try:
                    dict_crime_second_instances[json.loads(line)['id']][key] = json.loads(line)[key]
                except:
                    continue
    except: # wrong = 0
        pass

#这一块针对第一类情况：只看“裁判结果”的“驳回上诉”
initial_pair = len(dict_crime_second_instances.keys())
match_success_pair = 0

dict_crime_second_instances = \
{k:v for k,v in dict_crime_second_instances.items() if ('裁判结果' not in v.keys()) or (re.findall(r"驳回.*[上抗]诉", v['裁判结果']) == [])}

remain_pair = len(dict_crime_second_instances.keys())
match_success_pair += (initial_pair - remain_pair)

#这一块针对第二类情况：先看是否有申请撤回，一旦发现申请撤回，那么只要给了允许撤回，就说明匹配上了
remove_list = []
for key, value in dict_crime_second_instances.items():
    if '审理经过' in value.keys() and '裁判结果' in value.keys():
        if re.findall(r"(申请|自愿).*撤回", value['审理经过']) != []:
            if re.findall(r"准[允许].*撤回", value['裁判结果']) != []:
                remove_list.append(key)
                match_success_pair += 1

for i in remove_list:
    dict_crime_second_instances.pop(i)  #剩下来89/646项

remove_list = []
for key, value in dict_crime_second_instances.items():
    if '上诉人诉称' in value.keys() and '裁判结果' in value.keys():
        if re.findall(r"申请.*撤回", value['上诉人诉称']) != []:
            if re.findall(r"准[允许予].*撤回", value['裁判结果']) != []:
                remove_list.append(key)
                match_success_pair += 1

for i in remove_list:
    dict_crime_second_instances.pop(i)  #剩下来86/646项
