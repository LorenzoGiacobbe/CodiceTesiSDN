import os

def check():
        filename = raw_input('Insert name of file containing the targets (or h for help): ')
        while filename == 'h':
                os.system('python of-check.py -h')
                filename = raw_input('Insert name of file containing the targets (or h for help): ')

        result = raw_input('Where do you want to save the result? ')
        os.system('python of-check.py ' + filename + " " + result)

def enum():
        filename = raw_input('Insert name of file containing the targets (or h for help): ')
        while filename == 'h':
                os.system('python of-enum.py -h')
                filename = raw_input('Insert name of file containing the targets (or h for help): ')

        os.system('python of-enum.py ' + filename)

def displayHelp():

        print ("\r")
        print (" ------------------------------------------------------------------------------------------")
        print (" | Check targets             | Checks if the targets use the Openflow protocol            |")
        print (" | Enumerate targets         | Enumerates the targets and tells their role in the network |")
        print (" | Timeout Inference         | Fingerprints controller through Timeout Values Inference   |")
        print (" | Processing Time Inference | Fingerprints controller through Processing Time Inference  |")
        print (" ------------------------------------------------------------------------------------------")
        print ("\r")

if __name__ == "__main__":
        menu = {}
        menu['1']="Check targets"
        menu['2']="Enumerate targets"
        menu['3']="Timeout Inference"
        menu['4']="Processing Time Inference"
        menu['5']="Help"
        menu['6']="Exit"
        while True:
                options=sorted(menu.keys())
                # options.sort()
                for entry in options:
                        print (entry + '. ' + menu[entry])

                # Menu selection
                selection = raw_input("Please Select: ")
                if selection == '1':
                        check()
                if selection == '2':
                        enum()
                if selection == '3':
                        os.system("python fp-timeout.py")
                if selection == '4':
                        os.system("python fp-processing_time.py")
                if selection == '5':
                        displayHelp()
                if selection == '6':
                        break
