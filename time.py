import time
wait_time = 1
max_attempt = 5
current_attemp =0
while current_attemp< max_attempt:
	print("Attempt ",current_attemp+1,"-wait time ",wait_time)
	time.sleep(wait_time)
	wait_time=wait_time*2
	current_attemp+=1
	

import time

wait_time = 1
max_attempt = 5

for current_attempt in range(max_attempt):
    print("Attempt", current_attempt + 1, "- wait time", wait_time)
    time.sleep(wait_time)
    wait_time *= 2 