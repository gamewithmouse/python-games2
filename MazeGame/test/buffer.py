import random
import time

#버터 테스트
buffer = [0] * 10


while True:
    buffer.append(random.randint(1, 9))
    print(buffer.pop(0), "result", buffer, "buffer")

    time.sleep(0.1)