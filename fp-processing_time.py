import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import time        # for sleep between pings
import os          # to check if config file exists
import threading
import itertools
import sys

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
                                return {"pings":pings, "step":step, "accuracy":accuracy}

                        except ValueError:
                                print("Something wrong in the configuration file!")
        else:
                return {"pings":10, "step":0.5, "accuracy":10}

def ping(host, n):

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command.
        command = ['ping', param, str(n), host]

        output = subprocess.check_output(command)
        # avg ping time
        time = output.decode('utf8').splitlines()[n + 4].split('/')[4]
        return float(time)

def times(host, config):
        #send pings to install flow rule
        start_time = ping(host, 4)

        #send pings to calculate avg ping time
        avg_time = ping(host, config["pings"])

        # while ping time equals avg_time add step to wait 
        wait = 0
        while ping(host, 1) < (avg_time + config["accuracy"]):
                wait = wait + config["step"]
                if wait > 15:
                        # idle timeout is infinite
                        return {"idle_timeout":0, "avg_time":avg_time}
                time.sleep(wait)

        idle_timeout = wait
        return {"idle_timeout":idle_timeout, "avg_time":avg_time}

def processingTime(host, idle_timeout, avg_time, config):
        avg_ping_time = 0
        if idle_timeout == 0:
                return 0
        for x in range(config["pings"]):
                time.sleep(idle_timeout + 3)
                avg_ping_time += ping(host, 1)

        avg_ping_time = avg_ping_time / config["pings"]

        # avg_ping_time = ping_RTT + flow entry processing time
        # avg_time = ping_RTT
        processing_time = avg_ping_time - avg_time
        return processing_time

def cotroller():
        # default timeout values for different controllers
        print("-------------------------------------")
        print("|  Controller    |  processing_time |")
        print("-----------------+-------------------")
        print("|  Floodlight    |            13.0  |")
        print("|  Ryu           |               -  |")
        print("-------------------------------------")

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

        times = times(host, config)
        idle_timeout = times["idle_timeout"]
        avg_time = times["avg_time"]

        processing_time = processingTime(host, idle_timeout,avg_time, config)

        done = True
        time.sleep(.1)

        if processing_time == 0:
                print("Not possible to calculate processing time because idle-timeout is 0")
        else:
                print("The processing time of the Controller is: " + str(processing_time))

        cotroller()