
f = open("attendance.txt",'r')
# print(f.name)

arrayOfRollNos = []
i = 1
for lines in f.readlines():
    if i%2 ==0:
        arrayOfRollNos.append(lines.split(" ")[0])
        i=i+1
    else:
        i=i+1
        continue

print(arrayOfRollNos)


import pandas as pd
from pandas import DataFrame

df = pd.read_csv('reference.csv')
print(df.head())

df['Attendance'] = 0
print(df.head())

# print(df[df['RollNo.']==200001003]['Attendance'].values[0])

col = ['S.No.','RollNo.','Name','Attendance']
outputdf = pd.DataFrame(columns = col)

j=1
for eachrollno in df['RollNo.']:
    if str(eachrollno) in arrayOfRollNos:
        print(eachrollno)
        outputdf.loc[j] = [df[df['RollNo.']==eachrollno]['S.No.'].values[0],df[df['RollNo.']==eachrollno]['RollNo.'].values[0],df[df['RollNo.']==eachrollno]['Name'].values[0],1]
        
    else:
        outputdf.loc[j] = [df[df['RollNo.']==eachrollno]['S.No.'].values[0],df[df['RollNo.']==eachrollno]['RollNo.'].values[0],df[df['RollNo.']==eachrollno]['Name'].values[0],0]
        
    j=j+1

print(outputdf)

outputfinal = outputdf.to_csv('final-attendance.csv',index=None,header=True)
