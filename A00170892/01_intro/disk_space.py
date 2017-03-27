from subprocess import Popen, PIPE
df_process = Popen(["df","-h","/home"], stdout=PIPE, stderr=PIPE)
tail_process = Popen(["tail","-1"], stdin=df_process.stdout, stdout=PIPE, stderr=PIPE)
awk_process = Popen(["awk","{print $4}"], stdin=tail_process.stdout, stdout=PIPE, stderr=PIPE)
print awk_process.communicate()[0]
