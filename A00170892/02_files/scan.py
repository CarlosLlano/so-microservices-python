from subprocess import Popen, PIPE

with open('ip_adresses.txt', 'r') as f:
    data = f.readlines()

    for ip_address in data:
      ping_process = Popen(["ping","-c","1",ip_address.rstrip()], stdout=PIPE, stderr=PIPE)
      print ping_process.communicate()[0]
