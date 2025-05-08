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
    return render_template('login.html')  # login.html debe estar en /templates

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

            clave_sesion = f'CLAVE-{sesion_id}-{email.split("@")[0]}'
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
@app.route('/templates/login', methods=['POST'])
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
                return jsonify({'success': True, 'rol': rol, 'sesion_id': sesion_id}), 200
            else:
                return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401
        else:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Error en la base de datos: {err}'}), 500
    finally:
        cursor.close()
        conexion.close()

# -------------------- RUTA PARA VER PRESTAMOS --------------------
@app.route('/prestamos')
def prestamos():
    return render_template('User/Prestamos.html')  # asegúrarse que la ruta del archivo es User/Prestamos.html

# -------------------- Panel Admin --------------------
@app.route('/PanelAdmin')
def admin_dashboard():
    return render_template('Admin/PanelAdmin.html')



# -------------------- DATOS PRESTAMO --------------------
@app.route('/registrar_prestamo', methods=['POST'])
def registrar_prestamo():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()

    usuario_id = request.form.get('usuario_id')

    cursor.execute("SELECT sesion_id FROM usuarios WHERE id = %s", (usuario_id,))
    sesion_result = cursor.fetchone()
    if not sesion_result:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
    sesion_id = sesion_result[0]

    cursor.execute("SELECT admin_id FROM sesiones WHERE id = %s", (sesion_id,))
    admin_result = cursor.fetchone()
    if not admin_result:
        return jsonify({'success': False, 'message': 'Sesión no encontrada'}), 404
    admin_id = admin_result[0]

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

# -------------------- INICIO --------------------
if __name__ == '__main__':
    app.run(debug=True)
