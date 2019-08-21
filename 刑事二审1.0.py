#Inital format
import json
import re

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
            dict_crime_second_instances[json.loads(line)['id']] = {} #{...{'id':{}}}
            if '一审公诉机关称' in json.loads(line).keys():
                dict_crime_second_instances[json.loads(line)['id']]['公诉机关称'] = json.loads(line)['一审公诉机关称']
                #此处的小处理是因为发现有一些是“一审公诉机关称”，所以用“公诉机关称”来对应
            
            for key in dict_crime_second_instance_tmp.keys():
                #防止不匹配导致提取信息不足
                try:
                    dict_crime_second_instances[json.loads(line)['id']][key] = json.loads(line)[key]
                except:
                    continue
    except: # wrong = 0
        pass
    
#这一块针对第一类情况：只看“裁判结果”的“驳回上诉”，认为一旦“驳回上诉”，则回应了所有诉求
initial_pair = len(dict_crime_second_instances.keys())
#可以发现这里的初始案件总数为635<646,是因为有一些相同的id,所以我们仍然把他们当做同一案件处理
match_success_pair = 0
step = 1

dict_crime_second_instances = \
{k:v for k,v in dict_crime_second_instances.items() if ('裁判结果' not in v.keys()) or (re.findall(r"驳回.*[上抗]诉", v['裁判结果']) == [])}

remain_pair = len(dict_crime_second_instances.keys())
match_success_pair += (initial_pair - remain_pair)

print('Successfully matched pairs:')
print('Step', step, ':', match_success_pair)
#共有457个案件在这里匹配成功

#这一块针对第二类情况：先看是否有申请撤回，一旦发现申请撤回，那么只要“裁判结果”给了允许撤回，就说明匹配上了
remove_list = []
step += 1
for key, value in dict_crime_second_instances.items():
    if '审理经过' in value.keys() and '裁判结果' in value.keys():
        if re.findall(r"(申请|自愿).*撤回", value['审理经过']) != []:
            if re.findall(r"准[允许].*撤回", value['裁判结果']) != []:
                remove_list.append(key)
                match_success_pair += 1

for i in remove_list:
    dict_crime_second_instances.pop(i)  #剩下来89项

print('Step', step, ':', match_success_pair)

remove_list = []
step += 1
for key, value in dict_crime_second_instances.items():
    if '上诉人诉称' in value.keys() and '裁判结果' in value.keys():
        if re.findall(r"申请.*撤回", value['上诉人诉称']) != []:
            if re.findall(r"准[允许予].*撤回", value['裁判结果']) != []:
                remove_list.append(key)
                match_success_pair += 1

for i in remove_list:
    dict_crime_second_instances.pop(i)  #剩下来86项

print('Step', step, ':', match_success_pair)

#对于含有‘审理经过’：不服（提取出案号），最后‘裁判结果’看一下是否体现对这种诉求的维持、撤销
remove_list = []
step += 1
for key, value in dict_crime_second_instances.items():
    if '审理经过' in value.keys() and '裁判结果' in value.keys():
        if re.findall(r"（\d*）.*初字第\d*号刑事.*?判决|刑.*初字第\d*号刑事.*?判决", value['审理经过']) != [] and re.findall(r"不服|上诉|抗诉", value['审理经过']) != []:
            instance_no = re.findall(r"（\d*）.*初字第\d*号刑事.*?判决|刑.*初字第\d*号刑事.*?判决", value['审理经过'])[0]
            if re.findall('撤销|维持|变更.*' + instance_no, value['裁判结果']) != []:
                remove_list.append(key)
                match_success_pair += 1

for i in remove_list:
    dict_crime_second_instances.pop(i)
    
print('Step', step, ':', match_success_pair)

#剩下来的一些基本是不含有“审理经过”的，所以根据“公诉机关称”来进行提取，规则与前面是一样了，所以直接组合代码
remove_list = []
step += 1

for key, value in dict_crime_second_instances.items():
    if '公诉机关称' in value.keys() and '裁判结果' in value.keys():
        if re.findall(r".*撤回", value['公诉机关称']) != []:
            if re.findall(r"准[允许予].*撤回", value['裁判结果']) != []:
                remove_list.append(key)
                match_success_pair += 1
    
        if re.findall(r"（\d*）.*初字第\d*号刑事.*?判决|刑.*初字第\d*号刑事.*?判决", value['公诉机关称']) != [] and re.findall(r"不服|上诉|抗诉", value['公诉机关称']) != []:
                instance_no = re.findall(r"（\d*）.*初字第\d*号刑事.*?判决|刑.*初字第\d*号刑事.*?判决", value['公诉机关称'])[0]
                if re.findall('撤销|维持|变更.*' + instance_no, value['裁判结果']) != []:
                    remove_list.append(key)
                    match_success_pair += 1
    
for i in remove_list:
    dict_crime_second_instances.pop(i)
    
print('Step', step, ':', match_success_pair)

#剩下的是无法分辨的
print("Items hard to recogonize:", len(dict_crime_second_instances.keys()))
'''
for key, value in dict_crime_second_instances.items():
    print(value.keys())
'''

'''
发现最后剩下来的那个，只有“本院认为”以及“裁判结果”，我认为这都不太适合作为诉请的提取项，
为了防止对现有数据的“过拟合”，不再增加新的处理代码，把这种情况当成一种无法分辨的情况。
'''

print("Total second instances:", initial_pair, 'VS',"Successfully matched pairs:", match_success_pair)
