import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import time 	   # for sleep between pings
import os          # to check if config file exists
import threading 
import itertools
import sys

# valori default costanti del programma
# pings = 10 # numero di ping da inviare
# step  = 0.005  # step con il quale aumento il tempo di attesa tra un ping e l'altro
# accuracy  = 0.500
# hard_wait = 2

def configure():
	if os.path.exists('fingerprint.config'):
		with open('fingerprint.config', 'r') as f:
			try:
				for line in f:
					if line.startswith('pings'):
						pings = int(line.split()[1])
						print(pings)
					if line.startswith('step'):
						step = float(line.split()[1])
						print(step)
					if line.startswith('accuracy'):
						accuracy = float(line.split()[1])
						print(accuracy)
					if line.startswith('hard_wait'):
						hard_wait = float(line.split()[1])
						print(hard_wait)
				return {"pings":pings, "step":step, "accuracy":accuracy, "hard_wait":hard_wait}

			except ValueError:
				print("Something wrong in the configuration file!")
	else:
		return {"pings":10, "step":0.05, "accuracy":20, "hard_wait":2}

def ping(host, n):

	# Option for the number of packets as a function of
	param = '-n' if platform.system().lower()=='windows' else '-c'

	# Building the command.
	command = ['ping', param, str(n), host]

	output = subprocess.check_output(command)

	# avg ping time
	time = output.decode('utf8').splitlines()[n + 4].split('/')[4]
	return float(time)

def idleTimeout(host, config):
	#send pings to install flow rule
	start_time = ping(host, 1)
	print("start_time: " + str(start_time))

	#send pings to calculate avg ping time
	avg_time = ping(host, config["pings"])
	print("avg_time: " + str(avg_time))

	# while ping time equals avg_time add step to wait 
	wait = 2
	count = 0
	ping_time = ping(host, 1)
	print("ping_time: " + str(ping_time))
	while count < 2:
		wait = wait + config["step"]
		if wait > 15:
			# idle timeout is infinite
			return 0
		time.sleep(wait)
		ping_time = ping(host, 1)
		if ping_time > (avg_time + config["accuracy"]):
			count = count + 1
		print("ping_time: " + str(ping_time) + " , idle: " + str(wait))

	idle_timeout = wait
	print("idle_timeout: " + str(idle_timeout))
	return idle_timeout

def hardTimeout(host, idle_timeout, config):
	#send pings to install flow rule
	start_time = ping(host, 4)

	#send pings to calculate avg ping time
	avg_time = ping(host, config["pings"])

	hard_timeout = 0
	while ping(host, 1) < (avg_time + config["accuracy"]):
		hard_timeout = hard_timeout + config["hard_wait"]
		if hard_timeout > 40:
			return 0
		time.sleep(config["hard_wait"])

	return hard_timeout

def cotroller():
	# default timeout values for different controllers
	# ancora da fare esperimenti per trovare i valori
	print("------------------------------------------------------------")
	print("|  Controller    |  idle_timeout (s)  |  hard_timeout (s)  |")
	print("-----------------+--------------------+---------------------")
	print("|  OpenDaylight  |                 0  |                 0  |")
	print("|  Floodlight    |                 5  |                 0  |")
	print("|  POX           |                10  |                30  |")
	print("|  Ryu           |                 0  |                 0  |")
	print("|  Beacon        |                 5  |                 0  |")
	print("------------------------------------------------------------")

def animate():
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if done:
			break
		sys.stdout.flush()
		sys.stdout.write('\rpinging...' + c)
		sys.stdout.flush()
		time.sleep(0.1)
	sys.stdout.write('\rDone!      \n')

if __name__ == "__main__":
	#configure costants
	config = configure()

	# ask IP to ping
	host = raw_input('IP address of host to ping: ')

	done = False
	t = threading.Thread(target=animate)
	t.start()

	idle_timeout = idleTimeout(host, config)
	hard_timeout = hardTimeout(host, idle_timeout, config)
	
	done = True
	time.sleep(.1)

	print("The idle_timeout of the cotroller is: " + str(idle_timeout))
	print("The hard_timeout of the cotroller is: " + str(hard_timeout))

	cotroller()
