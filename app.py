# -------------------- IMPORTACIONES --------------------
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
            database="logincic_final"
        )
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# -------------------- RUTAS VISTAS --------------------
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/pendientes')
def pendientes():
    return render_template('User/pendientesDV.html')

@app.route('/inventario')
def vista_inventario():
    return render_template('Admin/inventario.html')

@app.route('/admin/historial')
def historial_admin():
    historial = obtener_historial_desde_db()
    return render_template('Admin/historial.html', historial=historial)

@app.route('/User/prestamos')
def vista_prestamos():
    return render_template('User/prestamos.html')

@app.route('/prestamos')
def prestamos():
    return render_template('User/Prestamos.html')

@app.route('/PanelAdmin')
def admin_dashboard():
    return render_template('Admin/PanelAdmin.html')

@app.route('/admin/GestiosProfesores')
def gestios_profesores():
    return render_template('Admin/GestiosProfesores.html')




@app.route('/User/devueltos')
def mostrar_devueltos():
    conexion = conectar_bd()
    if not conexion:
        return "Error al conectar con la base de datos", 500

    cursor = conexion.cursor(dictionary=True)
    try:
        hoy = datetime.now().date()
        cursor.execute("""
            SELECT p.id, prof.nombre AS nombre, prof.matricula, i.nombre AS equipo, p.cantidad,
                   DATE_FORMAT(p.fecha_prestamo, '%H:%i') AS hora_prestamo,
                   DATE_FORMAT(p.fecha_devolucion, '%H:%i') AS hora_devolucion,
                   (SELECT nombre FROM usuarios WHERE id = p.admin_id) AS entregado_por
            FROM prestamos p
            JOIN inventario i ON p.inventario_id = i.id
            JOIN profesores prof ON p.profesor_id = prof.id
            WHERE p.devuelto = 1 AND DATE(p.fecha_devolucion) = %s
            ORDER BY p.fecha_devolucion DESC
        """, (hoy,))
        devueltos = cursor.fetchall()
        return render_template('User/devueltos.html', devueltos=devueltos)
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return "Error al obtener los datos", 500
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
            SELECT p.id, prof.nombre AS nombre_profesor, prof.matricula, a.tipo_area, a.nombre AS area, e.nombre AS edificio,
                   i.nombre AS equipo, p.cantidad, p.fecha_prestamo, p.fecha_devolucion, p.devuelto,
                   u.nombre AS nombre_usuario, s.nombre AS nombre_sesion
            FROM prestamos p
            LEFT JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN sesiones s ON p.sesion_id = s.id
            LEFT JOIN areas a ON p.area_id = a.id
            LEFT JOIN edificios e ON a.edificio_id = e.id
            LEFT JOIN inventario i ON p.inventario_id = i.id
            LEFT JOIN profesores prof ON p.profesor_id = prof.id
            ORDER BY p.fecha_prestamo DESC
        """)
        historial = cursor.fetchall()
        return render_template('User/Historial.html', historial=historial)
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return "Error al obtener los datos", 500
    finally:
        cursor.close()
        conexion.close()

# -------------------- FUNCIONES AUXILIARES --------------------
def obtener_historial_desde_db():
    conexion = conectar_bd()
    if not conexion:
        return []

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id, prof.nombre AS nombre_profesor, prof.matricula, a.tipo_area, a.nombre AS area, e.nombre AS edificio,
                   i.nombre AS equipo, p.cantidad, p.fecha_prestamo, p.fecha_devolucion, p.devuelto,
                   u.nombre AS nombre_usuario, s.nombre AS nombre_sesion
            FROM prestamos p
            LEFT JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN sesiones s ON p.sesion_id = s.id
            LEFT JOIN areas a ON p.area_id = a.id
            LEFT JOIN edificios e ON a.edificio_id = e.id
            LEFT JOIN inventario i ON p.inventario_id = i.id
            LEFT JOIN profesores prof ON p.profesor_id = prof.id
            ORDER BY p.fecha_prestamo DESC
        """)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return []
    finally:
        cursor.close()
        conexion.close()

# -------------------- REGISTRO Y LOGIN --------------------
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()

    nombre = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    user_type = request.form.get('userType', 'student')
    admin_key_provided = request.form.get('adminKey', '').strip()
    session_key = request.form.get('sessionKey', '').strip()

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email y contraseña requeridos'}), 400

    try:
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'El email ya está registrado'}), 409

        if user_type == 'admin':
            cursor.execute("SELECT clave FROM admin_keys WHERE clave = %s", (admin_key_provided,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': 'Llave de administrador incorrecta'}), 401

            cursor.execute("INSERT INTO sesiones (nombre, clave) VALUES (%s, 'TEMP')", (nombre,))
            sesion_id = cursor.lastrowid
            clave_sesion = f"CLAVE-{sesion_id}-{email.split('@')[0]}"
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

@app.route('/login', methods=['POST'])
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

# -------------------- PRÉSTAMOS Y DEVOLUCIONES --------------------
@app.route('/registrar_prestamo', methods=['POST'])
def registrar_prestamo():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()

    sesion_id = request.form.get('sesion_id')

    if not sesion_id:
        return jsonify({'success': False, 'message': 'Sesión no proporcionada'}), 400

    # Obtener usuario que pertenece a esta sesión (rol student)
    cursor.execute("SELECT id FROM usuarios WHERE sesion_id = %s AND rol = 'student' LIMIT 1", (sesion_id,))
    user_result = cursor.fetchone()
    if not user_result:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
    usuario_id = user_result[0]

    # Buscar el administrador correspondiente a esa sesión
    cursor.execute("SELECT id FROM usuarios WHERE rol = 'admin' AND sesion_id = %s LIMIT 1", (sesion_id,))
    admin_result = cursor.fetchone()
    if not admin_result:
        return jsonify({'success': False, 'message': 'No se encontró un administrador para esta sesión'}), 400
    admin_id = admin_result[0]

    profesor_id = request.form.get('profesor_id')
    area_id = request.form.get('area_id')
    inventario_id = request.form.get('equipo_id')
    cantidad = request.form.get('cantidad')

    if not profesor_id or not area_id or not inventario_id or not cantidad:
        return jsonify({'success': False, 'message': 'Faltan datos del préstamo'}), 400

    try:
        # Verificar disponibilidad del equipo
        cursor.execute("SELECT stock FROM inventario WHERE id = %s", (inventario_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'success': False, 'message': 'Equipo no encontrado'}), 404

        stock = result[0]
        if int(cantidad) > stock:
            return jsonify({'success': False, 'message': 'No hay suficiente stock disponible'}), 400

        # Registrar préstamo
        cursor.execute("""
            INSERT INTO prestamos (
                admin_id, usuario_id, sesion_id, profesor_id,
                area_id, inventario_id, cantidad, fecha_prestamo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """, (admin_id, usuario_id, sesion_id, profesor_id, area_id, inventario_id, cantidad))

        # Actualizar stock
        cursor.execute("""
            UPDATE inventario SET stock = stock - %s 
            WHERE id = %s
        """, (cantidad, inventario_id))

        conexion.commit()
        return jsonify({'success': True, 'message': 'Préstamo registrado exitosamente'}), 201

    except mysql.connector.Error as err:
        conexion.rollback()
        return jsonify({'success': False, 'message': f'Error en la base de datos: {err}'}), 500
    finally:
        cursor.close()
        conexion.close()

@app.route('/marcar_devuelto', methods=['POST'])
def marcar_devuelto():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()
    prestamo_id = request.form.get('prestamo_id')
    inventario_id = request.form.get('inventario_id')
    cantidad = request.form.get('cantidad')

    try:
        # Marcar como devuelto
        cursor.execute("""
            UPDATE prestamos 
            SET devuelto = 1, fecha_devolucion = NOW() 
            WHERE id = %s
        """, (prestamo_id,))

        # Devolver al inventario
        cursor.execute("""
            UPDATE inventario 
            SET stock = stock + %s 
            WHERE id = %s
        """, (cantidad, inventario_id))

        conexion.commit()
        return jsonify({'success': True, 'message': 'Equipo marcado como devuelto'}), 200
    except mysql.connector.Error as err:
        conexion.rollback()
        return jsonify({'success': False, 'message': f'Error en la base de datos: {err}'}), 500
    finally:
        cursor.close()
        conexion.close()

# -------------------- INVENTARIO --------------------
@app.route('/api/inventario', methods=['GET'])
def obtener_inventario():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM inventario")
        equipos = cursor.fetchall()
        return jsonify(equipos)
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return jsonify({'success': False, 'message': 'Error al obtener inventario'}), 500
    finally:
        cursor.close()
        conexion.close()

@app.route('/api/inventario', methods=['POST'])
def agregar_equipo():
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    data = request.json
    nombre = data.get('nombre')
    tipo = data.get('tipo')
    marca = data.get('marca')
    numero_serie = data.get('numero_serie')
    fecha_adquisicion = data.get('fecha_adquisicion')
    stock = data.get('stock', 1)
    estado = data.get('estado', 'Disponible')

    if not all([nombre, tipo, marca, numero_serie, fecha_adquisicion]):
        return jsonify({'success': False, 'message': 'Faltan datos requeridos'}), 400

    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO inventario 
            (nombre, tipo, marca, numero_serie, fecha_adquisicion, stock, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, tipo, marca, numero_serie, fecha_adquisicion, stock, estado))
        
        conexion.commit()
        return jsonify({'success': True, 'message': 'Equipo agregado correctamente'}), 201
    except mysql.connector.Error as err:
        conexion.rollback()
        print("Error SQL:", err)
        return jsonify({'success': False, 'message': 'Error al agregar equipo'}), 500
    finally:
        cursor.close()
        conexion.close()

@app.route('/api/inventario/<int:id>', methods=['GET'])
def obtener_equipo(id):
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM inventario WHERE id = %s", (id,))
        equipo = cursor.fetchone()
        if equipo:
            return jsonify(equipo)
        else:
            return jsonify({'success': False, 'message': 'Equipo no encontrado'}), 404
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return jsonify({'success': False, 'message': 'Error al obtener equipo'}), 500
    finally:
        cursor.close()
        conexion.close()

# -------------------- API DATOS --------------------
@app.route('/api/tipos_area')
def api_tipos_area():
    conexion = conectar_bd()
    if not conexion:
        return jsonify([])

    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT DISTINCT tipo_area FROM areas")
        tipos = [row[0] for row in cursor.fetchall()]
        return jsonify(tipos)
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return jsonify([])
    finally:
        cursor.close()
        conexion.close()

@app.route('/api/edificios')
def api_edificios():
    conexion = conectar_bd()
    if not conexion:
        return jsonify([])

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nombre FROM edificios")
        edificios = cursor.fetchall()
        return jsonify(edificios)
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return jsonify([])
    finally:
        cursor.close()
        conexion.close()

@app.route('/api/areas')
def api_areas():
    tipo = request.args.get('tipo')
    edificio_id = request.args.get('edificio_id')

    if not tipo or not edificio_id:
        return jsonify([])

    conexion = conectar_bd()
    if not conexion:
        return jsonify([])

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, nombre FROM areas
            WHERE tipo_area = %s AND edificio_id = %s
        """, (tipo, edificio_id))
        areas = cursor.fetchall()
        return jsonify(areas)
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return jsonify([])
    finally:
        cursor.close()
        conexion.close()

@app.route('/api/equipos')
def api_equipos():
    conexion = conectar_bd()
    if not conexion:
        return jsonify([])

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, nombre, stock 
            FROM inventario 
            WHERE estado = 'Disponible' AND stock > 0
        """)
        equipos = cursor.fetchall()
        return jsonify(equipos)
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return jsonify([])
    finally:
        cursor.close()
        conexion.close()

@app.route('/api/profesor_por_matricula')
def profesor_por_matricula():
    matricula = request.args.get('matricula')
    if not matricula:
        return jsonify({'success': False, 'message': 'Matrícula requerida'}), 400

    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error de conexión'}), 500

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nombre FROM profesores WHERE matricula = %s", (matricula,))
        profesor = cursor.fetchone()
        if profesor:
            return jsonify({'success': True, 'profesor': profesor}), 200
        else:
            return jsonify({'success': False, 'message': 'Profesor no encontrado'}), 404
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return jsonify({'success': False, 'message': 'Error al buscar'}), 500
    finally:
        cursor.close()
        conexion.close()

@app.route('/api/prestamos_pendientes/<int:sesion_id>', methods=['GET'])
def prestamos_pendientes(sesion_id):
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id, prof.nombre AS nombre, prof.matricula, 
                   i.nombre AS equipo, p.cantidad, i.id AS equipo_id,
                   DATE_FORMAT(p.fecha_prestamo, '%H:%i') AS hora_prestamo,
                   a.nombre AS area, e.nombre AS edificio
            FROM prestamos p
            JOIN profesores prof ON p.profesor_id = prof.id
            JOIN inventario i ON p.inventario_id = i.id
            LEFT JOIN areas a ON p.area_id = a.id
            LEFT JOIN edificios e ON a.edificio_id = e.id
            WHERE p.devuelto = 0 AND p.sesion_id = %s
            ORDER BY p.fecha_prestamo DESC
        """, (sesion_id,))
        prestamos = cursor.fetchall()

        return jsonify({'success': True, 'data': prestamos}), 200
    except mysql.connector.Error as err:
        print("Error SQL:", err)
        return jsonify({'success': False, 'message': 'Error al obtener los préstamos pendientes'}), 500
    finally:
        cursor.close()
        conexion.close()

@app.route('/api/devolver_prestamo/<int:prestamo_id>', methods=['POST'])
def devolver_prestamo(prestamo_id):
    conexion = conectar_bd()
    if not conexion:
        return jsonify({'success': False, 'message': 'Error al conectar a la base de datos'}), 500

    cursor = conexion.cursor()
    try:
        # Obtener información del préstamo
        cursor.execute("""
            SELECT inventario_id, cantidad 
            FROM prestamos 
            WHERE id = %s
        """, (prestamo_id,))
        prestamo = cursor.fetchone()
        
        if not prestamo:
            return jsonify({'success': False, 'message': 'Préstamo no encontrado'}), 404
            
        inventario_id, cantidad = prestamo

        # Marcar como devuelto
        cursor.execute("""
            UPDATE prestamos 
            SET devuelto = 1, fecha_devolucion = NOW()
            WHERE id = %s
        """, (prestamo_id,))

        # Devolver al inventario
        cursor.execute("""
            UPDATE inventario 
            SET stock = stock + %s 
            WHERE id = %s
        """, (cantidad, inventario_id))

        conexion.commit()
        return jsonify({'success': True, 'message': 'Préstamo devuelto correctamente'}), 200
    except mysql.connector.Error as err:
        conexion.rollback()
        print("Error al marcar como devuelto:", err)
        return jsonify({'success': False, 'message': 'Error al marcar como devuelto'}), 500
    finally:
        cursor.close()
        conexion.close()
        
    #---api profesores
    
    # Obtener todos los profesores
@app.route('/api/profesores', methods=['GET'])
def obtener_profesores():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profesores")
    profesores = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(profesores)

# Agregar un nuevo profesor
@app.route('/api/profesores', methods=['POST'])
def agregar_profesor():
    data = request.json
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO profesores (matricula, nombre, correo)
            VALUES (%s, %s, %s)
        """, (data['matricula'], data['nombre'], data['correo']))
        conexion.commit()
        return jsonify({'success': True})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 400
    finally:
        cursor.close()
        conexion.close()

# Actualizar un profesor
@app.route('/api/profesores/<matricula>', methods=['PUT'])
def actualizar_profesor(matricula):
    data = request.json
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE profesores SET nombre=%s, correo=%s WHERE matricula=%s
        """, (data['nombre'], data['correo'], matricula))
        conexion.commit()
        return jsonify({'success': True})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 400
    finally:
        cursor.close()
        conexion.close()

# Eliminar un profesor
@app.route('/api/profesores/<matricula>', methods=['DELETE'])
def eliminar_profesor(matricula):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM profesores WHERE matricula = %s", (matricula,))
        conexion.commit()
        return jsonify({'success': True})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 400
    finally:
        cursor.close()
        conexion.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
