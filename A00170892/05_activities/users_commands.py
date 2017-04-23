from subprocess import Popen, PIPE, call
import datetime

def get_all_users():
    grep_process = Popen(["grep","/bin/bash","/etc/passwd"], stdout=PIPE, stderr=PIPE)
    user_list = Popen(["awk",'-F',':','{print $1}'], stdin=grep_process.stdout, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
    return filter(None,user_list)

def get_user_info(username):
    list={}
    grep_process = Popen(["grep",username,"/etc/passwd"], stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
    user_info = filter(None,grep_process)
    user_info = user_info[0].split(':')
    list["username"] = user_info[0]
    list["User ID (UID)"] = user_info[2]
    list["Group ID (GID)"] = user_info[3]
    list["Home directory"] = user_info[5]
    list["Command/shell"] = user_info[6]
    return list

def get_users_by_groupID(GID):
    respuesta = []
    for user in get_all_users():
        list = get_user_info(user)
        userGID = list["Group ID (GID)"]
        if userGID == GID:
            respuesta.append(list["username"])
    return respuesta

def add_user(username,password):
  add_process = Popen(["sudo","adduser","--password",password,username], stdout=PIPE, stderr=PIPE)
  add_process.wait()
  return True if username in get_all_users() else False

def remove_user(username):
  vip = ["operativos","python","ruby","root"]
  if username in vip:
    return True
  else:
    remove_process = Popen(["sudo","userdel","-r",username], stdout=PIPE, stderr=PIPE)
    remove_process.wait()
    return False if username in get_all_users() else True

#retorna los usuarios que se han logueados en los ultimos <string:time> minutos
def get_users_recently_logged(time):
    respuesta = []

    comandos = "lastlog -t 1 | tail -n +2 | awk '{if(NF < 9){print $1,$6;} else if(NF==9){print $1,$7;}}'"
    users_list = Popen(comandos,shell=True, stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')
    users_list = filter(None,users_list)

    x = datetime.datetime.now() - datetime.timedelta(minutes=int(time))
    y = x.strftime('%H:%M:%S')
    z = datetime.datetime.strptime(y, '%H:%M:%S')

    for user in users_list:
        array = user.split(' ')
        usuario = array[0]
        hora_last_loggin = array[1]
        fecha = datetime.datetime.strptime(hora_last_loggin, '%H:%M:%S')
        if fecha > z:
            respuesta.append(usuario)

    return respuesta

#ejemplo: echo "icesi" | passwd --stdin carlos
#se asume que el usuario existe
def change_password(username,password):
    return True

#retorna los ultimos 10 comandos ejecutador por el usuario
def get_commands_by_user(username):
    line = "/home/"+username+"/.bash_history"
    commands = Popen(["tail",line],stdout=PIPE,stderr=PIPE).communicate()[0].split('\n')
    return filter(None,commands)
