import fitbit
import json
import datetime
import time
import sys

def loadConfig_TokenFile(C_filename):
    f2 = open(C_filename, 'r')
    jsonData2 = json.load(f2)
    param = {}
    param['client_id'] = jsonData2['client_id']
    param['client_secret'] = jsonData2['client_secret']
    T_filename = jsonData2['token_file']

    f1 = open(T_filename, 'r')
    jsonData1 = json.load(f1)
    param['access_token'] = jsonData1['access_token']
    param['refresh_token'] = jsonData1['refresh_token']
    param['expires_at'] = jsonData1['expires_at']

    return param

def saveAsCSV(filename, data):
    csv_file = open(filename, 'w')
    
    for var in range(0, len(data)):
        csv_file.write(data[var]['time'])
        csv_file.write(",")
        csv_file.write(str(data[var]['value']))
        csv_file.write("\n")
    
    csv_file.close()

if __name__ == '__main__':
    # 取得したい心拍数データの日付    
    date = '2018-11-11'
    csv_filename = 'HR_{0}.csv'.format(date)

    config_filename = 'config.json'
    param = loadConfig_TokenFile(config_filename)

    dt = datetime.datetime.now()
    expire_dt =  datetime.datetime.fromtimestamp(param['expires_at'])
    if dt >= expire_dt:
        s = str(expire_dt)
        print('トークンの有効期限 {0} を過ぎてしまいました!'.format(s))
        print('新しいトークンを入手してください!')
        sys.exit()
    
    ac = fitbit.Fitbit(param['client_id'], param['client_secret'], param['access_token'], param['refresh_token'])

    # 心拍数を取得(1秒ごと)
    data_sec = ac.intraday_time_series('activities/heart', date, detail_level='1sec') #'1sec', '1min', or '15min'
    heart_sec = data_sec["activities-heart-intraday"]["dataset"]
    print(heart_sec[:10])
    saveAsCSV(csv_filename, heart_sec)

