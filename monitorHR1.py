import fitbit
import json
import datetime
import time
import sys
import threading

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

def worker():
    # global ac
    # data_sec = ac.intraday_time_series('activities/heart', date, detail_level='1sec')
    # heart_sec = data_sec["activities-heart-intraday"]["dataset"]
    # print('[{0}] {1}, {2}\n'.format(time.time(), heart_sec[-1]['time'], heart_sec[-1]['value']))
    print(time.time())

def schedule(interval, f, wait=True):
    base_time = time.time()
    next_time = 0
    c = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        
        c = c + 1
        if c >= 10:
            break
        
        next_time = ((time.time() - base_time) % interval) or interval
        print(next_time)
        time.sleep(next_time)

if __name__ == '__main__':
    dt = datetime.datetime.now()
    date = dt.strftime('%Y-%m-%d')

    csv_filename = 'monitor_HR_{0}.csv'.format(date)

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

    schedule(5, 10, worker)


