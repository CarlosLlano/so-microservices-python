from subprocess import Popen, PIPE
import sys
resultado=Popen(str(sys.argv), stdout=PIPE)
print resultado.communicate()[0]

