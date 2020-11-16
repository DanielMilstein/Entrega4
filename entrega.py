import psycopg2 as pg
from tabulate import tabulate


def registro(cur):
    nombre, email, clave, telefono = input('Ingrese nombre: '), input('Ingrese email: '), input('Ingrese clave: '), input('Ingrese telefono: ')
    if email != '' and telefono != ''



#establecer coneccion
con = pg.connect(
    host = '201.238.213.114',
    port = '54321',
    database = 'grupo12',
    user = 'grupo12',
    password = 'M87QW2'
)

cur = con.cursor()
#registrar o iniciar sesion
inicio = False

while inicio == False:
    menu_principal = input(' Seleccione que opción quiere:\n1. Registrar una cuenta\n2. Iniciar sesion\n(Escriba el numero de la opcion que quiere y ENTER)\nO aprete solo ENTER para salir\n')
    if menu_principal == '1':
        nombre, email, clave, telefono = input('Ingrese nombre: '), input('Ingrese email: '), input('Ingrese clave: '), input('Ingrese telefono: ')
        if email != '':
            cur.execute('select email from usuario where email = %s%s', (email,''))
            a = cur.fetchall()
        else:
            a=[]
        if telefono != '':
            cur.execute('select telefono from usuario where telefono = %s%s', (telefono,''))
            b = cur.fetchall()
        else:
            b = []
        if len(a) == 0 and len(b) == 0 and nombre != '' and clave !='':
            cur.execute('insert into usuario(email, nombre, telefono, clave) values(%s, %s, %s, %s)', (email, nombre, telefono, clave))
            con.commit()
            inicio = True
        else:
            print('Usuario incorrecto o ya existente...\nVolviendo al menu de inicio\n')
    elif menu_principal == '2':
        email, clave = input('Email: '), input('Clave: ')
        cur.execute('select u.email, u.clave from usuario u where u.email = %s and u.clave = %s', (email,clave))
        if len(cur.fetchall()) != 0:
            cerrar_sesion = False
            while cerrar_sesion == False:
                opcion = input('Iniciando sesión...\n\n Seleccione una de las siguientes opciones:\n1. Locales.\n2. Categorias.\n3. Promociones.\n4. Direcciones.\n5. Carrito.\n6. Historial de pedidos\n7. Repartidores.\nEnter para cerrar sesion y volver al menu de inicio')
                if opcion == '1':
                    cur.execute('select nombre, direccion from locales group by nombre, direccion order by nombre')
                    locales = cur.fetchall()
                    locales = [[i+1,locales[i][0],locales[i][1]] for i in range(len(locales))]
                    print('\nMostrando Locales...')
                    print(tabulate(locales, headers=['', 'nombre', 'dirección']))
                    opcion_local = input(' Seleccione una de las siguientes opciones:\n1. Ver local.\n2. Ver productos.\n3. Ver categorias.')
                    if opcion_local == '1':
                        seleccionar_local = int(input('Ponga el numero del local que quiere seleccionar: '))-1
                        local_seleccionado = locales[seleccionar_local]
                        cur.execute('select m.nombre from menu m, locales l where m.id_local = {} group by m.nombre'.format(local_seleccionado[0]))
                        menu_local = cur.fetchall()
                        cur.execute('select p.nombre from producto p, locales l where p.id_local = {} group by p.nombre'.format(local_seleccionado[0]))
                        producto_local = cur.fetchall()
                        print('\nMenus del local {}'.format(local_seleccionado[1]))
                        for menu in menu_local:
                            print(menu[0])
                        print('\nProductos del local {}'.format(local_seleccionado[1]))
                        for producto in producto_local:
                            print(producto[0])
                        print('\nVolviendo al menu de opciones...\n')
                    elif opcion_local == '2':
                        nombre, direccion, rating = input('Nombre del local: '), input('Direccion del local: '),input('Rating del local: ')
                        cur.execute('insert into locales(nombre, direccion, rating) values(%s,%s,%s)', (nombre, direccion, rating))
                        con.commit()
                        print('local añadido\nVolviendo al menu de opciones...\n')
                    elif opcion_local == '3':
                        pass
                elif opcion == '2':
                    cur.execute('select nombre from categoria group by nombre order by nombre')
                    categoria = cur.fetchall()
                    categoria = [[i+1,categoria[i][0]] for i in range(len(categoria))]
                    print(tabulate(categoria, headers= ['', 'Nombre categoria']))
                    menu_categoria = True
                    while menu_categoria == True:
                        opcion_local = input('1. Agregar categoria.\n2. Editar categoria.\n3. Eliminar categoria.\nEnter para volver al menu de opciones')
                        if opcion_local == '1': 
                            nombre = input('nombre de la nueva categoria:\n')
                            cur.execute('insert into categoria(nombre) values(%s%s)', (nombre,''))
                            con.commit()
                        elif opcion_local == '2':
                            nombre_actual, nombre_nuevo = input('Nombre de la categoria que se quiere editar:\n'), input('Nuevo nombre para la categoria:\n')
                            cur.execute('update categoria set nombre = %s where nombre = %s', (nombre_actual, nombre_nuevo))
                        elif opcion_local == '3':
                            numero = input('Numero de la categoria que se quiere eliminar:\n')
                            cur.execute('select id from categoria where nombre = %s%s', (categoria[int(numero)-1][1],''))
                            id_categoria = cur.fetchall()
                            print(id_categoria, categoria[int(numero)-1][1])
                            #cur.execute('delete from categoria where id = %s and nombre = %s', (id_categoria, categoria[int(numero)-1][1]))
                            #con.commit()
                        else:
                            menu_categoria = False
                elif opcion == '3':
                    cur.execute('select codigo, monto from promocion group by codigo, monto order by monto')
                    promocion = cur.fetchall()
                    promocion = [[i+1,promocion[i][0],promocion[i][1]] for i in range(len(promocion))]
                    print(tabulate(promocion, headers= ['', 'codigo', 'monto']))
                    menu_promocion = True
                    while menu_promocion == True:
                        opcion_local = input('1. Agregar promocion nueva.\n2. Agregar promocion a cuenta.\n3. Eliminar promocion.\nEnter para volver al menu de opciones')
                        if opcion_local == '1': 
                            monto, fecha = input('monto de la nueva promocion:\n'), input('fecha caducidad nueva promocion:\n')
                            cur.execute('insert into promocion(monto, fecha caducidad) values(%s,%s)', (monto,fecha))
                            con.commit()
                        elif opcion_local == '2':
                            codigo = input('Codigo de la promocion que se quiere agregar:\n')
                            cur.execute('insert into usuario_promocion(email,codigo) values(%s,%s)', (email,codigo))
                            con.commit()
                        elif opcion_local == '3':
                            codigo = input('Codigo de la promocion que se quiere eliminar:\n')
                            cur.execute('delete from usuario_promocion where email = %s and codigo = %s', (email,codigo))
                            con.commit()
                        else:
                            menu_promocion = False
                elif opcion == '4':
                    pass
                elif opcion == '5':
                    pass
                elif opcion == '6':
                    pass
                elif opcion == '7':
                    pass
                else:
                    cerrar_sesion = True
            print('\nCerrando sesión...\n') 
        else:
            print('Usuario o contraseña incorrecta.\nVolviendo al menu de inicio\n')
    else:
        inicio = True



#terminar cursor
cur.close()

#cerrar conexion
con.close()