// Obtiene una referencia al contenedor principal del login
const container = document.getElementById('container');

// Obtiene una referencia al botón de "Registrarse" en el panel de la derecha
const registerBtn = document.getElementById('register');

// Obtiene una referencia al botón de "Sign In" (Iniciar Sesión) en el panel de la izquierda
const loginBtn = document.getElementById('login');

// Obtiene una referencia al elemento <select> que permite elegir el tipo de usuario
const userTypeSelect = document.getElementById('userType');

// Obtiene una referencia al div que contiene el campo de la llave de administrador
const adminKeyField = document.getElementById('adminKeyField');

// Obtiene una referencia al formulario de registro ("Crea tu cuenta")
const signUpForm = document.getElementById('signUpForm');

// Obtiene una referencia al formulario de inicio de sesión
const signInForm = document.querySelector('.sign-in form');

// Agrega un listener al botón de "Registrarse" para mostrar el formulario de registro
registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

// Agrega un listener al botón de "Sign In" para mostrar el formulario de inicio de sesión
loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// Agrega un listener al cambio en la selección del tipo de usuario para mostrar/ocultar el campo de la llave de administrador
userTypeSelect.addEventListener('change', function() {
    adminKeyField.style.display = this.value === 'admin' ? 'block' : 'none';
});

// Agrega un listener al evento de envío del formulario de registro
signUpForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío tradicional del formulario

    const selectedUserType = userTypeSelect.value;
    const adminKeyInput = document.getElementById('adminKey');
    const nameInput = document.querySelector('.sign-up input[placeholder="Name"]');
    const emailInput = document.querySelector('.sign-up input[placeholder="Email"]');
    const passwordInput = document.querySelector('.sign-up input[placeholder="Password"]');

    if (selectedUserType === 'admin' && (adminKeyInput.value === null || adminKeyInput.value.trim() === '')) {
        alert('Por favor, ingresa la llave de administrador.');
        return;
    }

    const formData = new FormData();
    formData.append('name', nameInput.value);
    formData.append('email', emailInput.value);
    formData.append('password', passwordInput.value);
    formData.append('userType', selectedUserType);
    formData.append('adminKey', adminKeyInput.value);

    // Modificación importante: Usamos la URL absoluta para la petición al backend Flask
    fetch('http://127.0.0.1:5000/registro', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registro exitoso. Ahora puedes iniciar sesión.');
            container.classList.remove("active"); // Volver al formulario de inicio de sesión
        } else {
            alert('Error en el registro: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error en la petición de registro:', error);
        alert('Ocurrió un error al comunicarse con el servidor para el registro.');
    });
});

// Agrega un listener al evento de envío del formulario de inicio de sesión
signInForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío tradicional del formulario

    const userEmailInput = document.querySelector('.sign-in input[placeholder="Usuario"]'); // O Email
    const passwordInput = document.querySelector('.sign-in input[placeholder="Contraseña"]');

    const formData = new FormData();
    formData.append('user', userEmailInput.value);
    formData.append('password', passwordInput.value);

    // Modificación importante: Usamos la URL absoluta para la petición al backend Flask
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.rol === 'admin') {
                window.location.href = '/admin_dashboard'; // Redirigir al panel de administrador (debes crear esta página)
            } else if (data.rol === 'student') {
                window.location.href = '/student_dashboard'; // Redirigir al panel de estudiante (debes crear esta página)
            }
        } else {
            alert('Error al iniciar sesión: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error en la petición de inicio de sesión:', error);
        alert('Ocurrió un error al comunicarse con el servidor para iniciar sesión.');
    });
});
