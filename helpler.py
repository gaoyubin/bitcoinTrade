import time

def ts_to_time(ts):
    x = time.localtime(ts)

    return time.strftime('%Y-%m-%d %H:%M:%S', x)

if __name__ == "__main__":
    print(ts_to_time(1499184000))
