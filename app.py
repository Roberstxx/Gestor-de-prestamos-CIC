# -------------------- IMPORTACIONES --------------------

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Para permitir peticiones de otros dominios (como Vercel o frontend local)
import mysql.connector  # Conexión a MySQL/MariaDB
from werkzeug.security import generate_password_hash, check_password_hash  # Hash de contraseñas seguro
import os  # Para rutas (aunque no se usa directamente aquí)

# -------------------- CONFIGURACIÓN INICIAL --------------------

app = Flask(__name__)
CORS(app)  # Permite peticiones CORS (necesario para que el frontend se comunique con la API)

# -------------------- SERVIR FRONTEND ESTÁTICO --------------------

@app.route('/')
def index():
    # Carga el archivo index.html desde la carpeta frontend/
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    # Carga cualquier otro archivo estático (JS, CSS, imágenes, etc.)
    return send_from_directory('frontend', filename)

# -------------------- CONEXIÓN A BASE DE DATOS --------------------

def conectar_bd():
    """Establece conexión con la base de datos MySQL."""
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="logincic"
        )
        print("Conexión a la base de datos exitosa!")
        return mydb
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# -------------------- REGISTRO DE USUARIOS --------------------

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    """Registra a un nuevo usuario, validando si es admin o student."""
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()
    nombre = request.form.get('name', '')  # nombre es opcional
    email = request.form.get('email')
    password = request.form.get('password')
    user_type = request.form.get('userType', 'student')  # Por defecto es student
    admin_key_provided = request.form.get('adminKey', '')  # Solo necesario si es admin

    # Validación básica
    if not email or not password:
        cursor.close()
        conexion.close()
        return jsonify({'success': False, 'message': 'Email y contraseña son requeridos'}), 400

    try:
        # Verificar si el email ya existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'El email ya está registrado'}), 409

        # Validación de clave admin si se intenta registrar como administrador
        if user_type == 'admin':
            cursor.execute("SELECT `key` FROM admin_keys WHERE `key` = %s", (admin_key_provided,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': 'Llave de administrador incorrecta'}), 401

        # Encriptar la contraseña
        hashed_password = generate_password_hash(password)

        # Insertar el nuevo usuario
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password, rol)
            VALUES (%s, %s, %s, %s)
        """, (nombre, email, hashed_password, user_type))

        conexion.commit()
        return jsonify({'success': True, 'message': 'Registro exitoso'}), 201

    except mysql.connector.Error as err:
        conexion.rollback()
        print(f"Error MySQL: {err}")
        return jsonify({'success': False, 'message': f'Error en la base de datos: {err}'}), 500
    except Exception as e:
        conexion.rollback()
        print(f"Error inesperado: {e}")
        return jsonify({'success': False, 'message': f'Error inesperado en el servidor: {e}'}), 500
    finally:
        cursor.close()
        conexion.close()

# -------------------- INICIO DE SESIÓN --------------------

@app.route('/login', methods=['POST'])
def iniciar_sesion():
    """Verifica credenciales del usuario y devuelve el rol si es correcto."""
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()
    email = request.form.get('user')  # El frontend envía el email bajo el campo "user"
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Usuario y contraseña son requeridos'}), 400

    try:
        cursor.execute("SELECT id, password, rol FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            user_id, hashed_password, rol = user
            if check_password_hash(hashed_password, password):
                # Devuelve el rol para que el frontend decida a dónde redirigir
                return jsonify({'success': True, 'rol': rol}), 200
            else:
                return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 401
        else:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Error en la base de datos: {err}'}), 500
    except Exception as e:
        print(f"Error inesperado durante el login: {e}")
        return jsonify({'success': False, 'message': f'Error inesperado: {e}'}), 500
    finally:
        cursor.close()
        conexion.close()

# -------------------- INICIO DE LA APLICACIÓN --------------------

if __name__ == '__main__':
    app.run(debug=True)
    # Cambia el puerto si es necesario, por defecto es 5000
    # Puedes usar `app.run(host=' 
