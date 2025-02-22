#Importando  flask y algunos paquetes
import csv
from flask import Flask, request, session, jsonify , g
from flask_cors import CORS
from flask_mysqldb import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import cross_origin


app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'walking_legs'

mysql = MySQL(app)

app.secret_key = '97110c78ae51a45af397be6534caef90ebb9b1dcb3380af008f90b23a5d1616bf19bc29098105da20fe'
# Modulo Login
@cross_origin()
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        cursor = mysql.connection.cursor()

        # Consultar el correo y contraseña en la tabla de usuarios
        cursor.execute('''
            SELECT id, idroles, nombre, correo, contraseña 
            FROM usuarios 
            WHERE correo = %s
        ''', (email,))

        usuario = cursor.fetchone()
        cursor.close()

        # Si los datos son válidos
        if usuario and check_password_hash(usuario[4], password):
            # Crear datos de sesión
            session['conectado'] = True
            session['id'] = usuario[0]
            session['idroles'] = usuario[1]
            session['nombre'] = usuario[2]
            session['correo'] = usuario[3]
            
            print(session)

            response = {
                "message": "Logged in successfully",
                "dataLogin": {
                    "id": usuario[0],
                    "idroles": usuario[1],
                    "nombre": usuario[2],
                    "correo": usuario[3]
                }
            }
            print(response)
            return jsonify(response), 200 
        else:
            print("Usuario o contraseña incorrectos")
            response = {
                "message": "Email o contraseña incorrectos"
            }
            return jsonify(response), 401
    else:
        response = {
            "message": "Solicitud incorrecta"
        }
        return jsonify(response), 400





@app.route('/register_cliente', methods=['POST'])
def registrar_cliente():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        tipo_user = 2
        nombre = data.get('name')
        apellido = data.get('apellido')
        documento = data.get('documento')
        email = data.get('email')
        password = data.get('password')
        telefono = data.get('telefono')
        direccion = data.get('direccion')
        

        # Validar campos obligatorios
        if not nombre or not email or not password:
            response = {
                "message": "Por favor, completa todos los campos obligatorios del formulario."
            }
            return jsonify(response), 400

        # Conexión a la base de datos
        cursor = mysql.connection.cursor()

        try:
            # Buscar si ya existe el correo ingresado en la base de datos
            cursor.execute('SELECT correo FROM usuarios WHERE correo = %s', (email,))
            usuario = cursor.fetchone()

            if usuario:
                response = {
                    "message": "El correo ya está registrado."
                }
                return jsonify(response), 401  # Credenciales no válidas
            else:
                # La cuenta no existe y los datos del formulario son válidos,
                # Crear contraseña encriptada
                password_encriptada = generate_password_hash(password, method='scrypt')

                # Insertar en la base de datos
                cursor.execute('INSERT INTO usuarios (nombre, apellido, documento, correo, contraseña, telefono, direccion , idroles) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                               (nombre, apellido, documento, email, password_encriptada, telefono, direccion,  tipo_user))

                mysql.connection.commit()

                response = {
                    "message": "Cliente registrado exitosamente."
                }

                return jsonify(response), 200

        except Exception as e:
            # Manejar cualquier error que pueda ocurrir durante la ejecución de la consulta
            print(f"Error en la consulta SQL: {str(e)}")
            response = {
                "message": "Hubo un error durante el registro. Por favor, inténtalo de nuevo."
            }
            return jsonify(response), 500

        finally:
            cursor.close()

    else:
        response = {
            "message": "Solicitud incorrecta. Asegúrate de enviar datos en formato JSON."
        }
        return jsonify(response), 400


@app.route('/cerrarsesion', methods=['POST'])
def cerrarsesion():
    try:
        return jsonify({"mensaje": "Sesión cerrada exitosamente"})

    except Exception as e:
        return jsonify({"informacion": str(e)})
  
     
@app.route('/obtener_usuarios', methods=['GET'])
def informes():
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT nombre,apellido,documento,correo,telefono FROM `usuarios` WHERE idroles = 2;
        ''')

        resultados = cursor.fetchall()
        cursor.close()

        payload = []

        for result in resultados:
            content = {
                'nombre': result[0],
                'apellido': result[1],
                'documento': result[2],
                'correo': result[3],
                'telefono': result[4]
            }
            payload.append(content)

        return jsonify(payload)

    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500
    
    
    


#Solicitar PASEO (USUARIO)
@app.route('/solicitar_paseo', methods=['POST'])

def solicitar_servicio():
   

    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        tipo_mascota = data.get('tipo_mascota')
        direccion = data.get('direccion')
        fecha = data.get('fecha')
        duracion = data.get('duracion')
        # Verificar que se hayan proporcionado todos los datos necesarios
        if not tipo_mascota or not direccion or not fecha:
            response = {
                "message": "Faltan datos requeridos en la solicitud"
            }
            return jsonify(response), 401  
        
        # Conexión a la base de datos y guardar los datos del servicio solicitado
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO paseo (fecha, tipo_mascota, direccion, duracion) VALUES (%s, %s, %s, %s)',
                           (fecha, tipo_mascota, direccion,duracion))
            mysql.connection.commit()
            cursor.close()
            response = {
                "message": "Servicio solicitado exitosamente",
                "tipo_mascota": tipo_mascota,
                "direccion": direccion,
                "duracion":duracion,
                "fecha_programada": fecha
            }
            return jsonify(response), 200  # 200 OK status code for successful request
        except Exception as e:
            response = {
                "message": "Error al solicitar el servicio. Por favor, inténtelo nuevamente más tarde."
            }
            print(f"Error al insertar en la base de datos: {e}")
            return jsonify(response), 500  # 500 Internal Server Error status code for database error
    else:
        response = {
            "message": "Solicitud incorrecta"
        }
        return jsonify(response), 400  # 400 Bad Request status code for incorrect request    

"""
@app.route('/register_tecnico', methods=['POST'])
def register_tecnico():
    
    if request.method == 'POST' and request.is_json:
        
        data = request.get_json()  # Obtener los datos del cuerpo de la solicitud JSON
        tipo_user = 2
        nombre = data.get('name')
        email = data.get('email')
        password = data.get('password')

        cursor = mysql.connection.cursor()
        
        # Buscar si ya existe el correo ingresado en el formulario en la base de datos
        cursor.execute('''
                SELECT email FROM cliente WHERE email = %s
                UNION
                SELECT email FROM administrador WHERE email = %s
                UNION
                SELECT email FROM tecnico WHERE email = %s
            ''', (email, email, email))

        usuario = cursor.fetchone()
        cursor.close()  # Cerrar la conexión SQL

        if usuario:
            response = {
                "message": "El correo ya está registrado"
            }
            
            return jsonify(response), 401  # Credenciales no validas
       
        else:
            # La cuenta no existe y los datos del formulario son válidos,
            # Crear contraseña encriptada

            password_encriptada = generate_password_hash(password, method='scrypt')
            
            # Conexión a la base de datos y guardar los datos de la cuenta creada
            cursor = mysql.connection.cursor()

            # Insertar en la base de datos
            cursor.execute('INSERT INTO tecnico (nombre, email, password, tipo_usuario) VALUES (%s, %s, %s, %s)',
                           (nombre, email, password_encriptada, tipo_user))

            mysql.connection.commit()
            cursor.close()
            
            response = {

                "message": "Tecnico registrado exitosamente"
            
            }
            
            return jsonify(response), 200
    else:
        response = {
            "message": "Solicitud incorrecta"
        }
        return jsonify(response), 400 


#Solicitar servicios (CLIENTE)
@app.route('/solicitar_servicio', methods=['POST'])

def solicitar_servicio():
   

    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        tipo_servicio = data.get('tipo_servicio')
        direccion = data.get('direccion')
        fecha = data.get('fecha')
        id_cliente = data.get('idCliente')

        # Verificar que se hayan proporcionado todos los datos necesarios
        if not tipo_servicio or not direccion or not fecha:
            response = {
                "message": "Faltan datos requeridos en la solicitud"
            }
            return jsonify(response), 401  
        
        # Conexión a la base de datos y guardar los datos del servicio solicitado
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO servicio (fecha, tipo_servicio, direccion, id_cliente) VALUES (%s, %s, %s, %s)',
                           (fecha, tipo_servicio, direccion, id_cliente))
            mysql.connection.commit()
            cursor.close()
            response = {
                "message": "Servicio solicitado exitosamente",
                "tipo_servicio": tipo_servicio,
                "direccion": direccion,
                "fecha_programada": fecha
            }
            return jsonify(response), 200  # 200 OK status code for successful request
        except Exception as e:
            response = {
                "message": "Error al solicitar el servicio. Por favor, inténtelo nuevamente más tarde."
            }
            print(f"Error al insertar en la base de datos: {e}")
            return jsonify(response), 500  # 500 Internal Server Error status code for database error
    else:
        response = {
            "message": "Solicitud incorrecta"
        }
        return jsonify(response), 400  # 400 Bad Request status code for incorrect request
    



@app.route('/verserviciossolicitados', methods=['GET'])
def verserviciossolicitados():
    cursor = mysql.connection.cursor()

    # Consultar todos los servicios solicitados por los clientes
    cursor.execute('''
        SELECT servicio.id_servicio, cliente.nombre AS nombre_cliente, servicio.fecha, servicio.direccion, servicio.tipo_servicio
        FROM servicio
        INNER JOIN cliente ON servicio.id_cliente = cliente.id
    ''')

    servicios = cursor.fetchall()
    print(servicios)

    cursor.close()

    if servicios:
        # Mapeo de los resultados de la consulta a un diccionario por cada servicio
        servicios_list = []
        for servicio in servicios:
            servicio_dict = {
                "id_servicio": servicio[0],
                "nombre_cliente": servicio[1],
                "fecha": servicio[2].strftime('%Y-%m-%d'),  # Formatear la fecha al formato deseado
                "direccion": servicio[3],
                "tipo_servicio": servicio[4]
            }
            servicios_list.append(servicio_dict)

        # Crear la respuesta con la lista de servicios
        response = {
            "servicios": servicios_list
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "No se encontraron servicios solicitados"
        }
        return jsonify(response), 404



@app.route('/obtener_tecnicos', methods=['GET'])
def obtener_tecnicos():
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT id_tecnico, nombre FROM tecnico')
    tecnicos = cursor.fetchall()

    cursor.close()

    tecnicos_list = [{"id_tecnico": row[0], "nombre": row[1]} for row in tecnicos]

    if tecnicos_list:
        return jsonify({"tecnicos": tecnicos_list}), 200
    else:
        response = {
            "message": "No se encontraron técnicos en la base de datos"
        }
        return jsonify(response), 404

@app.route('/verificar_disponibilidad', methods=['POST'])
def verificar_disponibilidad():

    if request.method == 'POST' and request.is_json:
        data = request.get_json()

        id_servicio = data.get('id_servicio')
        id_tecnico = data.get('id_tecnico')

        print(id_servicio)
        print(id_tecnico)

        cursor = mysql.connection.cursor()

        # Obtener la fecha del servicio
        cursor.execute('SELECT fecha FROM servicio WHERE id_servicio = %s', (id_servicio,))
        fecha_servicio_result = cursor.fetchall()
        print(fecha_servicio_result)
        

        if fecha_servicio_result:
            fecha_servicio = fecha_servicio_result[0]
            print(fecha_servicio)

            # Verificar si el técnico está asignado a algún servicio en la misma fecha
            cursor.execute('''
                SELECT servicios_tecnico.id_servicio
                FROM servicios_tecnico
                INNER JOIN servicio ON servicios_tecnico.id_servicio = servicio.id_servicio
                WHERE servicios_tecnico.id_tecnico = %s AND servicio.fecha = %s
            ''', (id_tecnico, fecha_servicio))
            servicio_asignado = cursor.fetchone()

            cursor.close()

            if servicio_asignado:
                response = {
                    "message": "El técnico ya está asignado a otro servicio en la misma fecha. Por favor, elige otro técnico."
                }
                return jsonify(response), 401
            else:
                response = {
                    "message": "El técnico está disponible para el servicio en la fecha especificada."
                }
                return jsonify(response), 200
        else:
            cursor.close()
            response = {
                "message": "El ID del servicio no fue encontrado en el sistema."
            }
            return jsonify(response), 401

@app.route('/asignar_servicio', methods=['POST'])
def asignar_servicio():

    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        id_servicio = data.get('id_servicio')
        id_tecnico = data.get('id_tecnico')

        cursor = mysql.connection.cursor()

        # Verificar si el id_servicio y el id_tecnico existen en las tablas correspondientes
        cursor.execute('SELECT id_servicio FROM servicio WHERE id_servicio = %s', (id_servicio,))
        servicio = cursor.fetchone()

        cursor.execute('SELECT id_tecnico FROM tecnico WHERE id_tecnico = %s', (id_tecnico,))
        tecnico = cursor.fetchone()

        if servicio and tecnico:
            # Insertar la relación en la tabla servicios_tecnico
            cursor.execute('INSERT INTO servicios_tecnico (id_servicio, id_tecnico) VALUES (%s, %s)',
                           (id_servicio, id_tecnico))
            mysql.connection.commit()
            cursor.close()

            response = {
                "message": "Servicio asignado exitosamente al técnico"
            }
            return jsonify(response), 200
        else:
            response = {
                "message": "El ID del servicio no fue encontrado en el sistema"
            }
            return jsonify(response), 401
    else:
        response = {
            "message": "Solicitud incorrecta"
        }
        return jsonify(response), 400

@app.route('/ver_servicios_asignados', methods=['GET'])
def ver_servicios_asignados():

    id_tecnico = request.args.get('idTecnico') 
    print(id_tecnico)

    cursor = mysql.connection.cursor()

    # Obtener los servicios asignados al técnico por su ID
    cursor.execute('''
        SELECT servicio.id_servicio, cliente.nombre AS nombre_cliente, servicio.fecha, servicio.direccion, servicio.tipo_servicio FROM servicios_tecnico INNER JOIN servicio ON servicios_tecnico.id_servicio = servicio.id_servicio INNER JOIN cliente ON servicio.id_cliente = cliente.id WHERE servicios_tecnico.id_tecnico = %s
    ''', (id_tecnico,))
    servicios_asignados = cursor.fetchall()

    cursor.close()

    servicios_list = [{"id_servicio": row[0], "nombre_cliente": row[1], "fecha":row[2], "direccion":row[3], "tipo_servicio":row[4]} for row in servicios_asignados]

    if servicios_list:
        response = {
            "servicios_asignados": servicios_list
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "No se encontraron servicios asignados para este técnico"
        }
        return jsonify(response), 404

@app.route('/cerrarsesion', methods=['POST'])
def cerrarsesion():
    try:
        return jsonify({"mensaje": "Sesión cerrada exitosamente"})

    except Exception as e:
        return jsonify({"informacion": str(e)})
    

@app.route('/carga', methods=['POST'])
def upload_csv():
    # Verifica si se envió un archivo CSV
    if 'file' not in request.files:
        return jsonify({'error': 'No se ha proporcionado un archivo CSV'}), 400

    file = request.files['file']
    

    # Verifica si el archivo tiene una extensión CSV
    if file and file.filename.endswith('.csv'):
        try:
            # Lee el archivo CSV y almacena los registros en una lista de diccionarios
            csv_data = []
            csv_file = file.read().decode('utf-8').splitlines()
            
            csv_reader = csv.DictReader(csv_file)
            csv_reader = csv.reader(csv_file, delimiter=';')
            restros=0
            for row in csv_reader:
                nombre = row[0]
                email = row[1]
                password = row[2]
                
                restros+=  registrar_usuario(nombre,email,password)
                csv_data.append(row)

            response = {
                "message": "Numero de registros exisitoso" + str(restros)
             }
            

            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'El archivo no es un archivo CSV válido'}), 400



def  registrar_usuario(nombre, email, password):
    cursor = mysql.connection.cursor()

    # Buscar si ya existe el correo ingresado en el formulario en la base de datos
    cursor.execute('''
            SELECT email FROM cliente WHERE email = %s
            UNION
            SELECT email FROM administrador WHERE email = %s
            UNION
            SELECT email FROM tecnico WHERE email = %s
        ''', (email, email, email))

    usuario = cursor.fetchone()
    cursor.close()  # Cerrar la conexión SQL

    if usuario:
      
        return 0  # Credenciales no válidas

    else:
        # La cuenta no existe y los datos del formulario son válidos,
        # Crear contraseña encriptada

        password_encriptada = generate_password_hash(password, method='scrypt')

        # Conexión a la base de datos y guardar los datos de la cuenta creada
        cursor = mysql.connection.cursor()

        # Insertar en la base de datos
        cursor.execute('INSERT INTO tecnico (nombre, email, password, tipo_usuario) VALUES (%s, %s, %s, %s)',
                       (nombre, email, password_encriptada, 2))

        mysql.connection.commit()
        cursor.close()

        

        return 1


@app.route('/tiposervicio', methods=['GET'])
def obtener_tipo_servicio():
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT tipo_servicio, COUNT(*) as cantidad FROM servicio GROUP BY tipo_servicio;')
    data = cursor.fetchall()
    cursor.close()

    return jsonify({'tipos_servicio': data})



@app.route('/servicios6s', methods=['GET'])
def grafica3():
    try:
        
        cursor = mysql.connection.cursor()
       
        cursor.execute('SELECT s.tipo_servicio AS nombre_servicio,COUNT(s.tipo_servicio) AS numero_servicios FROM cliente c,servicio s WHERE c.id = s.id_cliente AND s.fecha >= DATE_SUB(NOW(), INTERVAL 6 MONTH) GROUP BY s.tipo_servicio;')
        rv = cursor.fetchall()
        cursor.close()
        payload = []
        content = {}
        print(rv)
        print("----------2")
        print(content)
        print(payload)
        for result in rv:
          content = {'nombre_servicio': result[0], 'numero_servicios': result[1]}
          payload.append(content)
           
        print("----------3")
        print(payload)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})



@app.route('/max_solicitado', methods=['GET'])
def grafica4():
    try:
      
        cursor = mysql.connection.cursor()
        #cur = mysql.connection.cursor()
        cursor.execute('SELECT cliente.nombre "nombre_cliente",COUNT(servicio.tipo_servicio) AS num_de_servicios_solicitados FROM cliente ,servicio WHERE cliente.id=servicio.id_cliente  GROUP BY cliente.nombre having num_de_servicios_solicitados=(SELECT MAX(num_de_servicios_solicitados) FROM(SELECT cliente.nombre "nombre_cliente",COUNT(servicio.tipo_servicio) AS num_de_servicios_solicitados FROM cliente ,servicio WHERE cliente.id=servicio.id_cliente  GROUP BY cliente.nombre) AS total);')
        rv = cursor.fetchall()
        cursor.close()
        payload = []
        content = {}
        print(rv)
        print("----------2")
        print(content)
        print(payload)
        for result in rv:
            content = {'nombre_cliente': result[0], 'num_de_servicios_solicitados': result[1]}
            payload.append(content)
           
        print("----------3")
        print(payload)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})


@app.route('/obtener_estadisticas_calificacion', methods=['GET'])
def obtener_estadisticas_calificacion():
    
    cursor = mysql.connection.cursor()

    try:
        cursor.execute('''
            SELECT
                SUM(CASE WHEN calificacion_cliente = 1 THEN 1 ELSE 0 END) AS '1',
                SUM(CASE WHEN calificacion_cliente >= 2 AND calificacion_cliente <= 3 THEN 1 ELSE 0 END) AS '2-3',
                SUM(CASE WHEN calificacion_cliente >= 4 AND calificacion_cliente <= 5 THEN 1 ELSE 0 END) AS '4-5'
            FROM informe_servicio;
        ''')

        estadisticas = cursor.fetchone()
        response = {
            "estadisticas": {
                "1": estadisticas[0],
                "2-3": estadisticas[1],
                "4-5": estadisticas[2]
            }
        }
        return jsonify(response), 200

    except Exception as e:
        response = {
            "message": f"Error al obtener estadísticas de calificación: {str(e)}"
        }
        return jsonify(response), 500

    finally:
        cursor.close()


@app.route('/estado', methods=['GET'])
def estado():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT SUM(CASE WHEN estado = 3 THEN 1 ELSE 0 END) AS servicios_finalizados, SUM(CASE WHEN estado = 2 THEN 1 ELSE 0 END) AS servicios_en_curso, SUM(CASE WHEN estado = 1 THEN 1 ELSE 0 END) AS servicios_sin_asignar FROM servicio;')
        rv = cursor.fetchone()  # Utilizamos fetchone en lugar de fetchall
        cursor.close()

        # Aquí accedemos a los elementos de la tupla directamente
        servicios_finalizados = rv[0]
        servicios_en_curso = rv[1]
        servicios_sin_asignar = rv[2]

        payload = {
            "servicios_finalizados": servicios_finalizados,
            "servicios_en_curso": servicios_en_curso,
            "servicios_sin_asignar": servicios_sin_asignar
        }

        print(payload)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500
       

@app.route('/mostrar_calificaciones', methods=['GET'])
def vercalificaciones():
   
    cursor = mysql.connection.cursor()
     
       
    # Consultar todas  las calificaciones enviadas por los clientes
    cursor.execute('''
      SELECT cliente.nombre AS nombre_cliente, cliente.id, informe_servicio.calificacion_cliente , informe_servicio.comentarios_cliente FROM servicio,cliente,informe_servicio WHERE servicio.id_servicio = informe_servicio.id_servicio AND servicio.id_cliente = cliente.id GROUP BY cliente.id;
                   

    ''')

    calificacion = cursor.fetchall()
    print(calificacion)


    cursor.close()

    if calificacion:
        # Si hay servicios solicitados, retornar la lista de servicios
        response = {
            "calificaciones": calificacion
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "No se encontraron servicios solicitados"
        }
        return jsonify(response), 404

@app.route('/calificar_servicio', methods=['POST'])
def calificar_servicio():
    try:
        if request.method == 'POST' and request.is_json:
            data = request.get_json()
            print("Datos recibidos:", data)  # Imprimir datos para depuración
            id_servicio = data.get('id_servicio')
            comentario = data.get('comentario')
            calificacion = data.get('calificacion')

            cursor = mysql.connection.cursor()

            cursor.execute('SELECT id_servicio FROM servicio WHERE id_servicio = %s', (id_servicio,))
            servicio = cursor.fetchone()

            if servicio:
                cursor.execute('UPDATE informe_servicio SET calificacion_cliente = %s, comentarios_cliente = %s WHERE id_servicio = %s', (calificacion, comentario, id_servicio))

                mysql.connection.commit()  # Agregar esta línea para aplicar cambios a la base de datos

                cursor.close()
                response = {
                    "message": "Calificacion registrada exitosamente"
                }
                return jsonify(response), 200
            else:
                response = {
                    "message": "El ID no fue encontrado en el sistema"
                }
                return jsonify(response), 401
        else:
            response = {
                "message": "Datos no válidos o faltantes en el cuerpo de la solicitud"
            }
            return jsonify(response), 400
    except Exception as e:
        print("Error en el servidor:", str(e))  # Imprimir detalles de la excepción para depuración
        response = {
            "message": f"Error en el servidor: {str(e)}"
        }
        return jsonify(response), 500


@app.route('/verinformes_cliente', methods=['GET'])
def informes():
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT informe_servicio.id_servicio, informe_servicio.descripcion_servicio AS descripcionser, informe_servicio.id_tecnico, informe_servicio.duracion_servicio, informe_servicio.recomendacion, servicio.fecha, servicio.tipo_servicio, tecnico.nombre 
            FROM informe_servicio
            INNER JOIN servicio ON servicio.id_servicio = informe_servicio.id_servicio
            INNER JOIN tecnico ON tecnico.id_tecnico = informe_servicio.id_tecnico;
        ''')

        resultados = cursor.fetchall()
        cursor.close()

        payload = []

        for result in resultados:
            content = {
                'id_servicio': result[0],
                'descripcion_servicio': result[1],
                'id_tecnico': result[2],
                'duracion_servicio': result[3],
                'recomendacion': result[4],
                'fecha': result[5],
                'tipo_servicio': result[6],
                'nombre': result[7]
            }
            payload.append(content)

        return jsonify(payload)

    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500


@app.route('/ver_estado', methods=['GET'])
def verestado():
    try:
        cursor = mysql.connection.cursor()  # Sin la opción dictionary=True
        cursor.execute(" SELECT servicio.id_servicio, cliente.nombre AS nombre_cliente, servicio.fecha, servicio.direccion , servicio.tipo_servicio, servicio.estado FROM servicio,cliente  WHERE servicio.id_cliente = cliente.id GROUP BY servicio.id_servicio;")
        servicios = cursor.fetchall()
        cursor.close()

        response = {
            "message": "Servicios solicitados obtenidos exitosamente",
            "servicios": servicios
        }
        return jsonify(response), 200

    except Exception as e:
        response = {
            "message": "Error al obtener servicios solicitados",
            "error": str(e)
        }
        return jsonify(response), 500


@app.route('/registrar_informe', methods=['POST'])
def registrarInforme():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        id_servicio = data.get('id_servicio')
        descripcion_servicio = data.get('descripcion_servicio')
        recomendacion = data.get('recomendacion')
        duracion_servicio = data.get('duracion_servicio')
        id_tecnico = data.get('id_tecnico')

        cursor = mysql.connection.cursor() 

        # Verificar si el id_servicio existe en la tabla servicio
        cursor.execute('SELECT id_servicio FROM servicio WHERE id_servicio = %s', (id_servicio,))
        servicio = cursor.fetchone()
        cursor.close()  # Cerrando conexión SQL

        if servicio:
            cursor = mysql.connection.cursor() 

            # Registrar el informe de servicio en la tabla informe_servicio
            cursor.execute('INSERT INTO informe_servicio (id_servicio, descripcion_servicio, duracion_servicio, recomendacion, id_tecnico) VALUES (%s, %s, %s, %s, %s)',
                           (id_servicio, descripcion_servicio, duracion_servicio, recomendacion, id_tecnico,))
            
            cursor.execute('''
            UPDATE servicio
            SET estado = '3'
            WHERE id_servicio = %s
            ''', (id_servicio,)) 

            cursor.close()  # Cerrando conexión SQL
            response = {
                "message": "Informe registrado exitosamente"
            }
            return jsonify(response), 200

        else:
            response = {
                "message": "El ID no fue encontrado en el sistema"
            }
            return jsonify(response), 401

    else:
        response = {
            "message": "Solicitud incorrecta"
        }
        return jsonify(response), 400


@app.route('/buscar_servicios_tecnico', methods=['GET'])
def buscar_servicios_tecnico():

    id_tecnico = request.args.get('idTecnico')  # Obtener el parámetro idTecnico de la cadena de consulta

    cursor = mysql.connection.cursor() 

    # Consultar los servicios realizados por el técnico especificado y obtener información adicional
    cursor.execute('''
        SELECT servicio.id_servicio,servicio.tipo_servicio,informe_servicio.descripcion_servicio, informe_servicio.recomendacion, 
        tecnico.id_tecnico, tecnico.nombre AS nombre_tecnico, cliente.id AS id_cliente, cliente.nombre AS 
        nombre_cliente FROM informe_servicio INNER JOIN servicio ON informe_servicio.id_servicio 
        = servicio.id_servicio INNER JOIN tecnico ON informe_servicio.id_tecnico = tecnico.id_tecnico 
        INNER JOIN cliente ON servicio.id_cliente = cliente.id WHERE tecnico.id_tecnico = %s
        
    ''', (id_tecnico,))

    servicios = cursor.fetchall()
    cursor.close()

    if servicios:
        # Si se encuentran servicios, retornar la lista de servicios con información adicional
        response = {
            "servicios": servicios
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "No se encontraron servicios realizados por usted"
        }
        return jsonify(response), 404


"""

if __name__ == '__main__':
    app.run( port=8000,debug=True)
