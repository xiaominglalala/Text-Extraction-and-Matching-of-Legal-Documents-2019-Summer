#Inital format
import json
import re

dict_crime_first_instances = {} #{'id':{'当事人':'', '审理经过':'',  '本院认为':'', '裁判结果':''}...}
dict_crime_first_instance_tmp = {'当事人':'', '审理经过':'',  '本院认为':'', '裁判结果':'','公诉机关称':''} #提取模板
filename = u'C://Users//BenWong//Desktop//yanyan//project//Justice-project//test_1//criminal.json'  #文件地址
file = open(filename,'r', encoding = 'utf-8')

while 1:
    line = file.readline()
    if not line:
        break
    try:
        if(json.loads(line)['procedureId'] == "一审"):
            dict_crime_first_instances[json.loads(line)['id']] = {} #{...{'id':{}}}
            for key in dict_crime_first_instance_tmp.keys():
                #防止不匹配导致提取信息不足
                try:
                    dict_crime_first_instances[json.loads(line)['id']][key] = json.loads(line)[key]
                except:
                    continue
    except:
        pass

#刑事一审诉请提取
dict_crime_first_instance_appeal = {}
#从"审理经过"中初步提取
error_list1 = []    #错误列表1
for key, value in dict_crime_first_instances.items():
    try:
        #{...'id':'诉请句'}；用的是审理经过的value作为string
        dict_crime_first_instance_appeal[key] = re.findall(r"指控被告人.*犯.*罪|被告人.*罪|被告人.*某.*一案|被告人.*一案|指控.*罪", value['审理经过'])[0]
    except:
        error_list1.append((key, value))
        #print((key,value))


#将已经提取过的诉求进行简化使其只包含关键词
error_list2 = []       #错误列表2
for key, value in dict_crime_first_instance_appeal.items():
    try:
        dict_crime_first_instance_appeal[key] = re.findall(r"(?<=犯).*罪|(?<=某).*一案|(?<=某).*罪|(?<=涉嫌).*罪|(?<=因).*一案|(?<=被告人).*一案", value)[0]
    except:
        error_list2.append((key, value))

#对于错误列表1中的尝试从“当事人”项中提取并放入到诉求中
for i in error_list1[:]:
    try:
        #i[0]为id
        dict_crime_first_instance_appeal[i[0]] = re.findall(r"因涉嫌.*(?=现羁押.*)|因涉嫌.*(?=现关押.*)|证据指控被告人.*构成.*罪|证据指控被告人.*犯.*罪|认为被告人.*构成.*罪|起诉书指控.*犯.*罪", i[1]['当事人'])[0]
        error_list1.remove(i)
        #print(dict_crime_first_instance_appeal[i[0]])#debug
    except:
        try:
            error_list2.append((i[0], i[1]['当事人']))
        except:
            pass
        pass
# print("\n")
# for i in error_list2:
#     print(i)
#debug

#对于错误列表1中的尝试从“公诉机关称”项中提取并放入到诉求中
for i in error_list1[:]:
    try:
        dict_crime_first_instance_appeal[i[0]] = re.findall(r"(?<=指控).*犯.*罪|因涉嫌.*(?=现关押.*)|证据指控被告人.*构成.*罪|证据指控被告人.*犯.*罪|认为被告人.*构成.*罪|起诉书指控.*犯.*罪", i[1]['公诉机关称'])[0]
        error_list1.remove(i)
    except:
        try:
            error_list2.append((i[0], i[1]['公诉机关称']))
        except:
            pass
        pass

#刑事一审回应提取
dict_crime_first_instance_reply = {}

error_list3 = []
for key, value in dict_crime_first_instances.items():
    try:
        try:
        #{...'id':'诉请句'}；用的是审理经过的value作为string
            dict_crime_first_instance_reply[key] = re.findall(r"；.*犯.*罪|(?<=被告人)*犯.*罪|某.*犯.*罪(?=判处.*)", value['裁判结果'])
        except:
            error_list3.append((key,value))
    except:
        error_list3.append((key, value))
#debug
for i in dict_crime_first_instance_reply.items():
    print(i)