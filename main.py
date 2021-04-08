import pandas as pd
import datetime
import numpy as np

#myfile = r"C:\Users\Christine\Desktop\ECE 412 -PGE CAPSTONE\Dryer Study\rbsam_y1_part-1-of-4\RBSAM_Y1_PART 1 OF 4.TXT"
myfile = r"C:\Users\X260\PycharmProjects\Xtine_RBSA_Cleaner\RBSAM_Y1_PART 4 OF 4.TXT"
#outputFolder = r"C:\Users\Christine\Desktop\houseProfiles\\"
outputFolder = r"C:\Users\X260\PycharmProjects\Xtine_RBSA_Cleaner\house_profiles_4\\"

df = pd.read_csv(myfile,sep='\t',header=(0))
#print(df)
df['time'] = pd.to_datetime(df['time'], format= '%d%b%y:%H:%M:%S')

#want just these columns
dg = df[['siteid','time','Dryer kWh (Appliance)','Service kWh']]
#print(dg)

#want just these rows - turn 'time' column into an index
data_frame = dg.set_index('time')
dh = data_frame[(data_frame.index >= '2012-12-02 00:00:00') & (data_frame.index <= '2013-02-23 23:45:00')]
#print(dh)

#want to math: ((Service kWh - Dryer kWh)/0.25)*1000
di = (((dh['Service kWh']-dh['Dryer kWh (Appliance)'])/0.25)*1000).to_frame('Watt')
#print (di)

#want to combine "siteid" column with "Watt' column
di['siteid'] = dh['siteid']
#print(di)


#create dictionary
d = {}
x = 0

for index, row in di.iterrows():
    house = row['siteid']
    delta = index - datetime.datetime.fromisoformat('2012-12-02 00:00:00')
    week = (delta.days // 7) + 1
#    print('time ', str(index), ' delta ', delta, ' week ', week)
    name = str(int(house)) + '_house_profile_' + str(week)
#    print(name)
    d[name] = pd.DataFrame()

#print(d)

#for k, v in d.items():
#    print('aaaaa')
#    print(k, '  ', v)

for index, row in di.iterrows():
    house = row['siteid']
    delta = index - datetime.datetime.fromisoformat('2012-12-02 00:00:00')
    week = (delta.days // 7) + 1
    name = str(int(house)) + '_house_profile_' + str(week)
    offsetDays = 42 - week * 7
    offsetTime = index + datetime.timedelta(days=offsetDays)
    d[name] = d[name].append(pd.DataFrame([[offsetTime, row['Watt']]]))
#    if x >= 10:
#        break
#    x += 1
#    print(d[name])

for k, v in d.items():
    print('aaaaa')
    print(k, '  ', v)
    outputFilePath = outputFolder + k + '.csv'
    v.to_csv(outputFilePath, index = False, header = False)