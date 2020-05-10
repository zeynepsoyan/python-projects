import os,socket


def ping_google():     #task1

    print("\nTASK1\n")
    print("Pinging 'google.com'...\n")

    os.system('ping -c 5 google.com >ping_google.txt')    #ping 4 times
    f = open("ping_google.txt",'r')
    print(f.read())
    f.close()


def ping_ip():      #task2

    print("\nTASK2\n")
    print("Pinging 'youtube.com','amazon.com','github.com' respectively...\n")

    ip_file = open('ip_file.txt','r')
    ips = ip_file.readlines()
    for ip in ips:
        os.system("ping -c 5 {} >ping_result.txt".format(ip.strip()))     #ping 4 times
        ping_file = open('ping_file.txt','a')
        ping_file.write("Ping results for {}".format(ip))

        with open('ping_result.txt','r') as ping_result:
            for line in ping_result:
                ping_file.write(line)
        try:
            os.remove("ping_result.txt")
        except FileNotFoundError:
            pass

        ping_file.write("--------------------------------------------------------\n")
        ping_file.close()

    print("Data written to file 'ping_file.txt'\n")


def google_avg():       #task3

    print("\nTASK3\n")
    print("Pinging 'google.com'...\n")

    os.system('ping -c 5 google.com >ping_google.txt')    #ping 4 times
    ping_google = open('ping_google.txt','r')
    with open('ping_google.txt','r') as ping_google:
        lines = []
        for line in ping_google:
            listed_line = line.split()
            lines.append(listed_line)
        total = 0
        for i in range(5):
            total += float(lines[i+1][-2][5:])
        print("Average time: ", total/5, "\n")


def ip_avg():       #task4

    print("\nTASK4\n")
    print("Pinging 'youtube.com','amazon.com','github.com' respectively...\n")

    ip_file = open('ip_file.txt','r')
    ips = ip_file.readlines()

    try:
        os.remove("ping_file.txt")
    except FileNotFoundError:
        pass

    for ip in ips:
        os.system('ping -c 5 {} >ping_result.txt'.format(ip.strip()))
        ping_file = open('ping_file.txt','a')
        ping_file.write("Ping results for {}".format(ip))

        with open('ping_result.txt','r') as ping_result:
            for line in ping_result:
                ping_file.write(line)
        ping_file.write("-----------------------------------------------\n")
        ping_file.close()

        lines = []
        with open('ping_file.txt','r') as ping_file:
            for line in ping_file:
                listed_line = line.split()
                lines.append(listed_line)

        total = 0
        indices = [i for i, listt in enumerate(lines) if '64' in listt]
        for i in indices:
           total = float(lines[i][-2][5:])
        avg = total/5

    ip_file.close

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("Your Computer Name is: " + hostname)
    print("Your Computer IP Address is: " + ip_address)
    print("Average time: ", avg, "\n")


try:
    os.remove("ping_file.txt")
except FileNotFoundError:
    pass

ping_google()
input("Press Enter to continue to TASK2")
ping_ip()
input("Press Enter to continue to TASK3")
google_avg()
input("Press Enter to continue to TASK4 (previously created 'ping_file.txt' will be removed and recreated in this task)")
ip_avg()
print("Program ended\n")
