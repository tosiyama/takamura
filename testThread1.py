import threading
import time

def count_func(name, interval):
    count = 0
    for _ in range(5):
        time.sleep(interval)
        count += 1
        print('{0}: {1}'.format(name, count))

if __name__ == '__main__':
    t1 = threading.Thread(target=count_func, args=('t1', 1))
    t2 = threading.Thread(target=count_func, args=('t2', 2))
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    t1.join()
    t2.join()


