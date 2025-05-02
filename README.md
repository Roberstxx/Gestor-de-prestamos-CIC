
# Sistema de Login con Flask y MySQL

Este es un proyecto de autenticación web usando **Flask**, **MySQL**, y un **frontend básico en HTML/CSS/JS**. Soporta registro e inicio de sesión tanto para estudiantes como para administradores.

---

## 📁 Estructura del Proyecto

```
/mi-proyecto
│
├── frontend/
│   ├── index.html       # Página principal con formulario
│   ├── script.js        # Lógica para enviar datos al backend
│   └── style.css        # Estilos básicos
│
├── app.py               # Backend principal en Flask
├── requirements.txt     # Dependencias necesarias de Python
└── README.md            # Este archivo de ayuda
```

---

## 🚀 Cómo Ejecutarlo en Local

Sigue estos pasos para correr el proyecto en tu máquina local.

### 1. Clona el repositorio
```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

### 2. Crea y activa un entorno virtual

#### En Windows:
```bash
python -m venv venv
.env\Scriptsctivate
```

#### En macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configura la base de datos MySQL

Abre **XAMPP** y asegúrate de que MySQL esté **activo**. Luego:

1. Abre [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
2. Crea una base de datos llamada: `logincic`
3. Crea las siguientes tablas dentro de esa base:

#### Tabla `usuarios`
```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('student', 'admin') NOT NULL
);
```

#### Tabla `admin_keys`
```sql
CREATE TABLE admin_keys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `key` VARCHAR(255) NOT NULL UNIQUE
);
```

4. Inserta una clave de administrador (temporal):
```sql
INSERT INTO admin_keys (`key`) VALUES ('admin1234');
```

### 5. Ejecuta la app
```bash
python app.py
```

La app se ejecutará en:
```
http://localhost:5000/
```

---

## 🧪 Pruebas rápidas

- Para registrar un usuario estudiante, solo llena el formulario.
- Para registrar un **administrador**, selecciona el rol y usa la clave: `admin1234`
- Luego puedes iniciar sesión con cualquiera de los dos tipos.

---

## ⚠️ Notas de seguridad

- Las contraseñas se almacenan con hashing seguro (`Werkzeug`).
- **Nunca expongas claves reales de admin en producción.** Usa variables de entorno o tokens.
- Este proyecto es de ejemplo educativo.

---

## 📦 Requisitos Python

Están en el archivo `requirements.txt`, pero por si acaso:

```txt
Flask
Flask-Cors
mysql-connector-python
Werkzeug
```

Instálalos con:

```bash
pip install -r requirements.txt
```

---

## ✅ Todo listo 


