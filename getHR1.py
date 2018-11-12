import fitbit

if __name__ == '__main__':
    client_id = '22D5WJ'
    client_secret = '82d281cf8d5b8c19720f20c04571d691'
    access_token =  'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkQ1V0oiLCJzdWIiOiI2WFFDSlMiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTQyMDIzOTUwLCJpYXQiOjE1NDE5OTUxNTB9.hQ493ERXC6o9CtIk96wIGzAf9CZNmGVRCNm5aQdJOrQ'
    refresh_token = '78018639dd15c4ea6e6fa912b670e98db38d381ca07b0f4317ca463b99db9a8b'
    
    date = '2018-11-11'

    ac = fitbit.Fitbit(client_id, client_secret, access_token, refresh_token)

    # 心拍数を取得(1秒ごと)
    data_sec = ac.intraday_time_series('activities/heart', date, detail_level='1sec') #'1sec', '1min', or '15min'
    heart_sec = data_sec["activities-heart-intraday"]["dataset"]
    print(heart_sec[:10])
