import csv
from get_criminal_appel_reply import *

filename1 = u'C://Users//BenWong//Desktop//Justice-project//罪名.csv'
csv_reader = csv.reader(open(filename1,'r', encoding='UTF-8-sig'))
accusations = []
for row in csv_reader:
    accusations.append(row[0])

right = 0
total = 0
for key, value in dict_crime_first_instance_appeal.items():
    total += 1
    match_list_appeal = [0 for i in range(len(accusations))]
    match_list_reply = [0 for i in range(len(accusations))]
    for extracted_appeal in value:
        for i in range(len(accusations)):
            if (re.search(accusations[i], extracted_appeal) != None):
                match_list_appeal[i] = 1
    for extracted_reply in dict_crime_first_instance_reply[key]:
        for i in range(len(accusations)):
            if (re.search(accusations[i], extracted_reply) != None):
                match_list_reply[i] = 1
    flag = True
    for index in range(len(match_list_appeal)):
        if match_list_appeal[index] == 1:
            if match_list_reply[index] != 1:
                flag = False
                break
    if flag:
        right += 1

print('match:', right, 'total:', total, 'match_rate:', right/total*100, '%' )
