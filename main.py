import pandas as pd
import datetime
import numpy as np

myfile = r"C:\Users\X260\PycharmProjects\Xtine_RBSA_Cleaner\RBSAM_Y1_PART 4 OF 4.TXT"
outputFolder = r"C:\Users\X260\PycharmProjects\Xtine_RBSA_Cleaner\house_profiles_4\\"

df = pd.read_csv(myfile,sep='\t',header=(0))
df['time'] = pd.to_datetime(df['time'], format= '%d%b%y:%H:%M:%S')

# Want just these columns:
dg = df[['siteid','time','Dryer kWh (Appliance)','Service kWh']]

# Want just these rows - turn 'time' column into an index:
data_frame = dg.set_index('time')
dh = data_frame[(data_frame.index >= '2012-12-02 00:00:00') & (data_frame.index <= '2013-02-23 23:45:00')]

# Want to math: ((Service kWh - Dryer kWh)/0.25)*1000
di = (((dh['Service kWh']-dh['Dryer kWh (Appliance)'])/0.25)*1000).to_frame('Watt')

# Want to combine "siteid" column with "Watt' column:
di['siteid'] = dh['siteid']


# Create dictionary:
d = {}
x = 0

for index, row in di.iterrows():
    house = row['siteid']
    delta = index - datetime.datetime.fromisoformat('2012-12-02 00:00:00')
    week = (delta.days // 7) + 1
    name = str(int(house)) + '_house_profile_' + str(week)
    d[name] = pd.DataFrame()


for index, row in di.iterrows():
    house = row['siteid']
    delta = index - datetime.datetime.fromisoformat('2012-12-02 00:00:00')
    week = (delta.days // 7) + 1
    name = str(int(house)) + '_house_profile_' + str(week)
    offsetDays = 42 - week * 7
    offsetTime = index + datetime.timedelta(days=offsetDays)
    d[name] = d[name].append(pd.DataFrame([[offsetTime, row['Watt']]]))


for k, v in d.items():
    print('aaaaa')
    print(k, '  ', v)
    outputFilePath = outputFolder + k + '.csv'
    v.to_csv(outputFilePath, index = False, header = False)