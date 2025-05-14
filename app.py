# -------------------- IMPORTACIONES --------------------
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- CONFIGURACIÓN --------------------
app = Flask(__name__)
CORS(app)

# -------------------- CONEXIÓN A BASE DE DATOS --------------------
def conectar_bd():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="logincic"
        )
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# -------------------- RUTA PRINCIPAL --------------------
@app.route('/')
def index():
    return render_template('login.html')
  # ✅ Correcto

@app.route('/pendientes')
def pendientes():
    return render_template('User/pendientesDV.html')

#@app.route('/User/devueltos')
#def Vista_devueltos():
#    return render_template('User/devueltos.html')
@app.route('/inventario')
def vista_inventario():
    return render_template('Admin/inventario.html')

@app.route('/paneladmin')
def paneladmin():
    return render_template('Admin/PanelAdmin.html')

@app.route('/admin/historial')
def historial_admin():
    historial = obtener_historial_desde_db()  # Asegúrate de que esta función esté definida
    return render_template('Admin/historial.html', historial=historial)








# -------------------- REGISTRO DE USUARIOS --------------------
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()
    nombre = request.form.get('name', '')
    email = request.form.get('email')
    password = request.form.get('password')
    user_type = request.form.get('userType', 'student')
    admin_key_provided = request.form.get('adminKey', '')
    session_key = request.form.get('sessionKey', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email y contraseña requeridos'}), 400

    try:
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'El email ya está registrado'}), 409

        if user_type == 'admin':
            cursor.execute("SELECT `key` FROM admin_keys WHERE `key` = %s", (admin_key_provided,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': 'Llave de administrador incorrecta'}), 401

            cursor.execute("INSERT INTO sesiones (admin_id, nombre) VALUES (0, %s)", (nombre,))
            sesion_id = cursor.lastrowid

            clave_sesion = f'CLAVE-{sesion_id}-{email.split('@')[0]}'
            cursor.execute("UPDATE sesiones SET clave = %s WHERE id = %s", (clave_sesion, sesion_id))
        else:
            cursor.execute("SELECT id FROM sesiones WHERE clave = %s", (session_key,))
            sesion = cursor.fetchone()
            if not sesion:
                return jsonify({'success': False, 'message': 'Clave de sesión inválida'}), 401
            sesion_id = sesion[0]

        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password, rol, sesion_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, email, hashed_password, user_type, sesion_id))

        conexion.commit()
        return jsonify({'success': True, 'message': 'Registro exitoso'}), 201

    except mysql.connector.Error as err:
        conexion.rollback()
        return jsonify({'success': False, 'message': f'Error en la base de datos: {err}'}), 500
    finally:
        cursor.close()
        conexion.close()

# -------------------- INICIO DE SESIÓN --------------------
@app.route('/login', methods=['POST'])  # CAMBIO: esta ruta es la correcta que tu JS usará
def iniciar_sesion():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()
    email = request.form.get('user')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Usuario y contraseña requeridos'}), 400

    try:
        cursor.execute("SELECT id, password, rol, sesion_id FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            user_id, hashed_password, rol, sesion_id = user
            if check_password_hash(hashed_password, password):
                return jsonify({
                    'success': True,
                    'rol': rol,
                    'sesion_id': sesion_id,
                    'usuario_id': user_id
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401
        else:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Error en la base de datos: {err}'}), 500
    finally:
        cursor.close()
        conexion.close()

# -------------------- VISTA DE PRÉSTAMOS --------------------
@app.route('/prestamos')
def prestamos():
    return render_template('User/Prestamos.html')

# -------------------- PANEL DE ADMIN --------------------
@app.route('/PanelAdmin')
def admin_dashboard():
    return render_template('Admin/PanelAdmin.html')



# -------------------- REGISTRAR PRÉSTAMO --------------------
@app.route('/registrar_prestamo', methods=['POST'])
def registrar_prestamo():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()
    usuario_id = request.form.get('usuario_id')
    admin_id_solicitud = request.form.get('admin_id')  # ✅ Obtener admin_id del formulario

    # --- ¡¡¡ IMPORTANTE: VALIDAR admin_id_solicitud !!! ---
    # Aquí DEBES implementar una lógica robusta para verificar que el
    # admin_id_solicitud corresponde a un administrador autenticado
    # y tiene permiso para realizar esta acción. Esto podría implicar
    # consultar tu base de datos o utilizar algún otro mecanismo de
    # autenticación y autorización.
    #
    # Ejemplo básico (¡INSUFICIENTE PARA PRODUCCIÓN!):
    try:
        admin_id_int = int(admin_id_solicitud)
    except ValueError:
        return jsonify({'success': False, 'message': 'ID de administrador inválido'}), 400

    cursor.execute("SELECT id FROM usuarios WHERE id = %s AND rol = 'admin'", (admin_id_int,))
    admin_autenticado = cursor.fetchone()

    print(f"Valor de admin_id recibido del frontend: {admin_id_solicitud}")  # ***
    print(f"Resultado de la consulta de validación del admin: {admin_autenticado}")  # ***

    if not admin_autenticado:
        return jsonify({'success': False, 'message': 'Administrador no válido o no autenticado'}), 401
    admin_id = admin_autenticado[0]
    # --- FIN DE LA VALIDACIÓN ---

    cursor.execute("SELECT sesion_id FROM usuarios WHERE id = %s", (usuario_id,))
    sesion_result = cursor.fetchone()
    if not sesion_result:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
    sesion_id = sesion_result[0]

    nombre = request.form.get('nombre')
    matricula = request.form.get('matricula')
    tipo_area = request.form.get('tipo_area')
    area = request.form.get('area')
    edificio = request.form.get('edificio')
    equipo = request.form.get('equipo')
    cantidad = request.form.get('cantidad')

    if not nombre or not matricula:
        return jsonify({'success': False, 'message': 'Nombre y matrícula son obligatorios'}), 400

    try:
        cursor.execute("""
            INSERT INTO prestamos_realizados
            (admin_id, usuario_id, sesion_id, nombre, matricula, tipo_area, area, edificio, equipo, cantidad)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (admin_id, usuario_id, sesion_id, nombre, matricula, tipo_area, area, edificio, equipo, cantidad))

        conexion.commit()
        return jsonify({'success': True, 'message': 'Préstamo registrado exitosamente'}), 201

    except mysql.connector.Error as err:
        conexion.rollback()
        return jsonify({'success': False, 'message': f'Error en la base de datos: {err}'}), 500
    finally:
        cursor.close()
        conexion.close()
        
# -------------------- NUEVAS RUTAS PARA TARJETAS DINÁMICAS --------------------

# 1) Obtener todos los préstamos pendientes de una sesión (devuelto = 0)
@app.route('/api/prestamos_pendientes/<int:sesion_id>', methods=['GET'])
def prestamos_pendientes(sesion_id):
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, nombre, matricula, equipo, cantidad, fecha
            FROM prestamos_realizados
            WHERE sesion_id = %s AND devuelto = 0
            ORDER BY fecha ASC
        """, (sesion_id,))
        prestamos = cursor.fetchall()
        return jsonify({'success': True, 'data': prestamos}), 200

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': str(err)}), 500

    finally:
        cursor.close()
        conexion.close()


# 2) Marcar un préstamo como devuelto (devuelto = 1)
@app.route('/api/devolver_prestamo/<int:prestamo_id>', methods=['POST'])
def devolver_prestamo(prestamo_id):
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE prestamos_realizados SET devuelto = 1, updated_at = NOW() WHERE id = %s",

            (prestamo_id,)
        )
        conexion.commit()
        


        return jsonify({'success': True, 'message': 'Préstamo marcado como devuelto'}), 200

    except mysql.connector.Error as err:
        conexion.rollback()
        return jsonify({'success': False, 'message': str(err)}), 500

    finally:
        cursor.close()
        conexion.close()
        
        
        # 3) Obtener todos los préstamos devueltos de una sesión (devuelto = 1)
        
from datetime import datetime

@app.route('/User/devueltos')
def mostrar_devueltos():
    conexion = conectar_bd()
    if not conexion:
        return "Error al conectar con la base de datos", 500

    cursor = conexion.cursor(dictionary=True)

    try:
        hoy = datetime.now().date()
        cursor.execute("""
            SELECT nombre, matricula, equipo, cantidad,
                   DATE_FORMAT(fecha, '%H:%i') AS hora_prestamo,
                   DATE_FORMAT(updated_at, '%H:%i') AS hora_devolucion,
                   'Administrador' AS entregado_por  -- ajusta según tu estructura real
            FROM prestamos_realizados
            WHERE devuelto = 1 AND DATE(updated_at) = %s
            ORDER BY updated_at DESC
        """, (hoy,))
        devueltos = cursor.fetchall()
        return render_template('User/devueltos.html', devueltos=devueltos)

    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return "Error al obtener los datos", 500

    finally:
        cursor.close()
        conexion.close()

# API: obtener inventario
@app.route('/api/inventario', methods=['GET'])
def api_inventario():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM inventario")
        equipos = cursor.fetchall()
        return jsonify(equipos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conexion.close()

# API: agregar equipo
@app.route('/api/inventario', methods=['POST'])
def api_agregar_equipo():
    data = request.json
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO inventario (nombre, tipo, marca, numero_serie, fecha_adquisicion)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['nombre'],
            data['tipo'],
            data['marca'],
            data['numero_serie'],
            data['fecha_adquisicion']
        ))
        conexion.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conexion.close()

# API: eliminar equipo
@app.route('/api/inventario/<int:id>', methods=['DELETE'])
def api_eliminar_equipo(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM inventario WHERE id = %s", (id,))
        conexion.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conexion.close()
        
@app.route('/User/historial')
def historial():
    conexion = conectar_bd()
    if not conexion:
        return "Error al conectar a la base de datos", 500

    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT pr.id, pr.nombre, pr.matricula, pr.tipo_area, pr.area, pr.edificio,
                   pr.equipo, pr.cantidad, pr.fecha, pr.devuelto, pr.updated_at,
                   u.nombre AS nombre_usuario, s.nombre AS nombre_sesion
            FROM prestamos_realizados pr
            LEFT JOIN usuarios u ON pr.usuario_id = u.id
            LEFT JOIN sesiones s ON pr.sesion_id = s.id
            ORDER BY pr.fecha DESC
        """)
        historial = cursor.fetchall()
        return render_template('User/Historial.html', historial=historial)
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return "Error al obtener los datos", 500
    finally:
        cursor.close()
        conexion.close()
        
        
def obtener_historial_desde_db():
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT pr.id, pr.nombre, pr.matricula, pr.tipo_area, pr.area, pr.edificio,
                   pr.equipo, pr.cantidad, pr.fecha, pr.devuelto, pr.updated_at,
                   u.nombre AS nombre_usuario, s.nombre AS nombre_sesion
            FROM prestamos_realizados pr
            LEFT JOIN usuarios u ON pr.usuario_id = u.id
            LEFT JOIN sesiones s ON pr.sesion_id = s.id
            ORDER BY pr.fecha DESC
        """)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return []
    finally:
        cursor.close()
        conexion.close()




        

# -------------------- INICIO --------------------
if __name__ == '__main__':
    app.run(debug=True)
