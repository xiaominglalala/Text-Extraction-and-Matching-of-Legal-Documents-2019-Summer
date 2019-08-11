###Initial framework
import json
import re
###导入文本文件并把感兴趣的部分存入到相应的大字典里面，大字典的key是案件的id号，每个key对应的value又是一个小字典，每个小字典包含
###当事人，审理经过，公诉机关称，裁判结果
dict_crime_first_instances = {}
dict_crime_first_instance_tmp = {'当事人': '', '审理经过': '',  '公诉机关称':'', '裁判结果':''}
filename = u'C://Users//Administrator//Desktop//深度学习入门//把手网数据集//6.1课题四案件评查与减假暂//把手案例网数据_small//dataset_small//criminal.json'
file = open(filename,'r', encoding = 'utf-8')

###提取每一个案件并建立好大字典
while 1:
    line = file.readline()
    try:
        if(json.loads(line)['procedureId'] == "一审"):
            dict_crime_first_instances[json.loads(line)['id']] = {}
            for key in dict_crime_first_instance_tmp.keys():
                dict_crime_first_instances[json.loads(line)['id']][key] = json.loads(line)[key]
    except:
        pass
    if not line:
        break

###提取刑事一审诉求
dict_crime_first_instance_appeal = {}  #建立一个诉求字典，key为案件id，value为相应的诉求字符串

#从“审理经过”中初步提取
error_list1 = []       #错误列表1
for key, value in dict_crime_first_instances.items():
    try:
        dict_crime_first_instance_appeal[key] = re.findall(r"指控被告人.*犯.*罪|被告人.*罪|被告人.*某.*一案|被告人.*一案|指控.*罪", value['审理经过'])[0]
    except:
        error_list1.append((key, value))

#将已经提取过的诉求进行简化使其只包含关键词
error_list2 = []       #错误列表2
for key, value in dict_crime_first_instance_appeal.items():
    try:
        dict_crime_first_instance_appeal[key] = re.findall(r"(?<=犯).*罪|(?<=某).*一案|(?<=某).*罪|(?<=涉嫌).*罪|(?<=因).*一案|(?<=被告人).*一案", value)[0]
    except:
        error_list2.append((key, value))

#对于错误列表1中的尝试从“当事人”项中提取并放入到诉求中
for i in error_list1:
    try:
        dict_crime_first_instance_appeal[i[0]] = re.findall(r"(?<=因).*罪|(?<=犯).*罪", i[1]['当事人'])[0]
    except:
        try:
            error_list2.append((i[0], i[1]['当事人']))
        except:
            pass
        pass    