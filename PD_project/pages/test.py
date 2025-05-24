from queues import Varqueue
import threading


pin= Varqueue()

print("append 5 4 3 2 1")
pin.add(5)
pin.add(4)
pin.add(3)
pin.add(2)
pin.add(1)

print("sensor wait")

thread = threading.Thread(target=pin.loop, daemon=True)
thread.start()

while True:
    pass
