from modelo import db, Monitoreo

def get_all_checks():

    checks_list = []
    todos = Monitoreo.query.all()
    tamanio = len(todos)

    for i in range(0,tamanio):
        check = todos[i]
        checkData = ['cpu:'+str(check.cpu),'memory:'+str(check.memory),'disk:'+str(check.disk),'httpd:'+str(check.httpd)]

        checks_list.append(checkData)

    return filter(None,checks_list)

def get_last_cpu_checks(size):

    checks_list = []

    todos = Monitoreo.query.order_by(Monitoreo.id.desc()).limit(int(size)).all()
    tamanio = len(todos)


    for i in range(0,tamanio):
        check = todos[i]
        checks_list.append(check.cpu)

    return filter(None,checks_list)
