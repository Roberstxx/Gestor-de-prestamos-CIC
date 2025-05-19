# 📚 CIC | Sistema de Préstamo de Equipos

Sistema web para la **gestión de préstamos y devoluciones de equipos de cómputo** en entornos universitarios (como el Centro de Innovación y Computación - CIC). Pensado para brindar control, trazabilidad y facilidad en el préstamo de materiales como laptops, cables HDMI, proyectores, entre otros.

---

## 🚀 Funcionalidades principales

🔐 **Login con roles dinámicos**  
- Registro e inicio de sesión para **administradores** y **estudiantes**, con flujos y vistas personalizadas.  
- Integración de claves de sesión al estilo *Google Classroom* para estudiantes.

🧾 **Módulo de Préstamos**  
- Realiza préstamos indicando profesor, área, equipo y cantidad.  
- Registro visual y validado con notificaciones tipo toast.

📌 **Préstamos Pendientes y Devoluciones**  
- Vista moderna con tarjetas interactivas que permiten **devolver equipos** con un solo clic.  
- Mensajes de confirmación animados y claros.

📅 **Historial y Devueltos del Día**  
- Consulta de préstamos ya devueltos filtrados por sesión y fecha.

👨‍🏫 **Gestión de Profesores**  
- CRUD completo para **registrar, editar y eliminar profesores**.  
- Interface amigable estilo inventario con animaciones suaves.

📦 **Gestión de Inventario**  
- Control del stock de cada equipo disponible para préstamo.  
- Añadir, modificar o eliminar ítems del inventario.

🛠 **Panel de Administrador**  
- Acceso centralizado para administrar el sistema, con accesos directos visuales a cada módulo.  
- Cierre de sesión visual y seguro.

---

## 🖥️ Tecnologías utilizadas

- **Flask** + Jinja2  
- **MySQL**  
- **HTML5 / CSS3 / JavaScript**  
- **Fetch API / AJAX**  
- **Notificaciones toast personalizadas**  
- **LocalStorage para control de sesión y flujo entre roles**

---

## 📸 Capturas del sistema

> (Aquí puedes subir imágenes como: login, módulo de préstamos, tarjetas de devoluciones, panel admin, etc.)

---

## 🧭 Estructura general del proyecto

```
/static/
    ├── css/
    ├── js/
    └── icons/

/templates/
    ├── login.html
    ├── Admin/
    └── User/

app.py (archivo principal Flask)
```

---

## 🧑‍💻 Cómo ejecutar el proyecto localmente

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/cic-prestamos.git
   cd cic-prestamos
   ```

2. Instala las dependencias (opcional si usas un entorno virtual):
   ```bash
   pip install flask mysql-connector-python
   ```

3. Crea la base de datos en MySQL con el esquema correspondiente (tablas: `usuarios`, `prestamos`, `inventario`, `profesores`, etc.).

4. Configura tu conexión a la base de datos en `app.py`:
   ```python
   mysql.connector.connect(
       host="localhost",
       user="root",
       password="",
       database="logincic_final"
   )
   ```

5. Ejecuta el servidor:
   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

6. Abre en tu navegador:
   ```
   http://localhost:5000
   ```

---

## ✅ Estado del proyecto

🟢 **Versión estable**  
Actualmente en uso funcional con módulos completos. Se siguen aplicando mejoras visuales y optimizaciones.

---

## 👨‍💻 Autores

- Roberto Martín  
- Alan Sauriel

---

## 📄 Licencia

Proyecto de uso académico. Sin licencia comercial aún definida.
