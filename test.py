import pandas as pd
import time

pd_SensConfig = pd.read_csv('SensorConfigInfo.csv')
pd_SensConfig['HUB ID'] = pd_SensConfig['HUB ID'].fillna('NO IP')
pd_SensConfig['Camera IP'] = pd_SensConfig['Camera IP'].fillna('NO IP')
pd_SensConfig['Channel'] = pd_SensConfig['Channel'].fillna(0)
pd_SensConfig['RT No'] = pd_SensConfig['RT No'].fillna(0)
pd_SensConfig['Preset'] = pd_SensConfig['Preset'].fillna(0)

CamList = pd_SensConfig['Camera IP'].unique()
pd_Camera = pd.DataFrame(CamList,columns=['IPAddr'])
pd_Camera['LastAccTime'] = pd.Series([time.perf_counter() for x in range(len(pd_Camera.index))])
print(pd_Camera)
time.sleep(1)
t1 = time.perf_counter()
CameraIP = "192.168.1.24"
t2 = pd_Camera.loc[(pd_Camera['IPAddr'] == CameraIP),'LastAccTime'].values[0]
CamIndex = pd_Camera.index[pd_Camera['IPAddr'] == CameraIP][0]
pd_Camera.iloc[CamIndex, pd_Camera.columns.get_loc('LastAccTime')] = t1
print(pd_Camera)
print('Time Lapsed', t1 - t2)