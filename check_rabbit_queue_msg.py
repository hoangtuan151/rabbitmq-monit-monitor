#!/usr/bin/python2.7

import sys
import subprocess

# Default threshold
MAX_NUMBER_MESSAGE_IN_QUEUE = 100

# Specific threshold
QUEUE_CONFIG = {
	'queue_name_1': 100,
	'queue_name_2': 50
}


RABBITMQ_CHECK_COMMAND = ['/bin/bash', '-c', 'HOME=/root /home/rabbitmq_server-3.5.2/sbin/rabbitmqctl list_queues name messages']

exit_code = 1
try:
	result = subprocess.check_output(RABBITMQ_CHECK_COMMAND, stderr=subprocess.STDOUT)
	result = result.decode('utf-8')
	list_line = result.split('\n')
	dict_queue = {}
	for line in list_line:
		arr = line.split('\t')
		if len(arr) == 2 and arr[1].isdigit():
			dict_queue[arr[0]] = int(arr[1])

	queue_error = {}
	for queue in dict_queue:
		if queue in QUEUE_CONFIG:
			if dict_queue[queue] >= QUEUE_CONFIG[queue]:
				queue_error[queue] = dict_queue[queue]
		else:
			if dict_queue[queue] >= MAX_NUMBER_MESSAGE_IN_QUEUE:
				queue_error[queue] = dict_queue[queue]

	if queue_error:
		print('Queue have too many message')
		for queue in queue_error:
			print(queue + " : " + str(dict_queue[queue]))
	else:
		exit_code = 0
		print('Queue OK')

except subprocess.CalledProcessError as ex:
	print('Run command rabbitmqctl failed: %r' % ex)
except Exception as e:
	print('Exception when run script check queue: %r' % e)

sys.exit(exit_code)
