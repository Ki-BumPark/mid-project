import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
#file_name 에 들어가는 파일은 의약품처방데이터 입니다.
#atcdata.csv 는 의약품 정보를 WHO 의 ATC 코드에 매핑시켜놓은 데이터입니다.
file_name = "NHIS_OPEN_T60_2018_PART3.csv"
ATC_file_name = "atcdata.csv"
#test.csv 는 의약품 처방 데이터를 위에서부터 10000행만 잘라서 만든 Demo용 데이터 입니다.
#한글이 포함된 CSV 를 READ 할때에는  encoding='ANSI' 옵션을 부여합니다.
df = pd.read_csv("test.csv")

#의약품 처방 데이터에서 해당 의약품의 약품일반성분명 코드만 떼어내어 저장합니다.
df_normal = df['약품일반성분명코드']


#ATC 코드 매핑 데이터를 READ 합니다.
#READ가 완료되면, 해당 데이터에서 약품일반성분명코드와 ATC 코드 데이터만 추출합니다.
#주성분코드는 약품일반성분명 코드를 의미합니다.
df_ATCdata = pd.read_csv(ATC_file_name)
df_ATC_map = df_ATCdata.loc[:, ['주성분코드', 'ATC코드']]
find_list = []

#'J01'은 항생제 (anti-biotics) 를 의미하는 WHO 의 ATC 코드입니다.
#원래는 J01과 J02 를 모두 분석해야 하지만, 현재 데모를 위하여 규모를 줄였습니다.
#ATC 코드 매핑 데이터에서 중복을 제거하여 j01_list 에 저장합니다.
df_ATC_find = df_ATC_map[df_ATC_map['ATC코드'].str.contains('J01')]
J01_list = df_ATC_find['ATC코드'].unique()

#J01_list에 있는 ATC 코드들과, 이 ATC 코드가 검색된 횟수를 저장할 딕셔너리를 만듭니다.
J01_dict={}
for i in J01_list:
    J01_dict[i] = 0
given_list=[]
count = 0

#의약품 처방 데이터에 있는 약품일반성분명코드를 ATC 매핑 데이터에서 찾습니다.
#만약 찾았다면, 중복된 결과를 모두 제거하여 given_list 에 저장합니다.
for i in df_normal:
    temp = df_ATC_map[df_ATC_map['주성분코드'].isin([i])]
    temp_uniq = temp['ATC코드'].unique()
    if len(temp_uniq)!= 0:
        given_list.append(temp_uniq[0])

#given_list를 확인하여 특정 약품이 검색된 횟수를 J01_dict에 반영합니다.
for i in given_list:
    if J01_dict.get(i) != None:
        J01_dict[i] = J01_dict[i]+1


#항감염제 (현재 데모에서는 항생제)의 목록과 호출 횟수를 포함한 j01_dict 를 출력합니다.
print(J01_dict)


#matplotlib 의 bar 메소드를 활용하여 처방된 항생제의 처방 횟수와 ATC 코드를 막대그래프로 시각화합니다.
x_list=[]
y_list =[]
for i in J01_dict:
    if J01_dict[i] != 0:
        x_list.append(i[3:])
        y_list.append(J01_dict[i])
        
plt.bar(x_list, y_list)
plt.title('Anti-biotics analysis', fontsize=20)
plt.ylabel('count', fontsize=14)
plt.xlabel('Anti-biotics ATC code with out "j01"', fontsize=14)
plt.show()
