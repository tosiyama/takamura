import threading
import datetime
import time

def worker():
    dt =  datetime.datetime.fromtimestamp(time.time())
    print('[{0}]'.format(str(dt)))

if __name__ == '__main__':
    base_time = 0
    next_time = 0
    c = 0
    while True:
        base_time = time.time()
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        t.join()

        c += 1
        if c >= 5:
            break
        
        next_time = 10 - (time.time() - base_time)
        print(next_time)
        time.sleep(next_time)
    
