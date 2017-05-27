from subprocess import Popen, PIPE, call
from modelo import db, Monitoreo
import time

while True:

#consumo de cpu
    comandos_cpu = "ps -A -o pcpu | tail -n+2 | paste -sd+ | bc"
    respuesta = Popen(comandos_cpu,shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
    pcpu = respuesta[0] + "%"

#consumo de memoria RAM
    comandos_memory = "free -m | tail -n +2 | grep Mem | awk '{print ($3/$2)*100}'"
    respuesta_memory = Popen(comandos_memory,shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
    pmemory = str(round(float(respuesta_memory[0]),2)) + "%"

#espacio disponible en disco
    comandos_disk = "df -h /home |tail -1 | awk '{print $4}'"
    respuesta_disk = Popen(comandos_disk,shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
    pdisk = respuesta_disk[0]

#estado del servicio httpd
    comandos_estado = "/bin/systemctl status  httpd.service | grep -o '\w*ctive '"
    respuesta_estado = Popen(comandos_estado,shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
    pestado = respuesta_estado[0].strip()

    registro = Monitoreo(cpu=pcpu, memory=pmemory, disk=pdisk, httpd=pestado)

#validacion de numero de registro
    cantidad = len(Monitoreo.query.all())
    if cantidad == 100:
        todos = Monitoreo.query.all()
        primero = todos[0]
        db.session.delete(primero)
        db.session.commit()

    db.session.add(registro)
    db.session.commit()

#registra cada 60 segundos
    time.sleep(60)
