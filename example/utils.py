import time


# Helper to simulate heavy work
def heavy_computation(seconds=0.1):
    start_time = time.time()
    while True:
        if time.time() - start_time > seconds:
            break
