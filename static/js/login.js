// -------------------- REFERENCIAS --------------------
const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const userTypeSelect = document.getElementById('userType');
const adminKeyField = document.getElementById('adminKeyField');
const sessionKeyField = document.getElementById('sessionKeyField');
const signUpForm = document.getElementById('signUpForm');
const signInForm = document.querySelector('.sign-in form');

// -------------------- FUNCIÓN DE TOAST --------------------
function mostrarToast(mensaje, tipo = 'success') {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }

    toast.textContent = mensaje;
    toast.className = `toast show ${tipo}`;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// -------------------- TRANSICIONES ENTRE FORMULARIOS --------------------
registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// -------------------- CAMBIO DE CAMPOS SEGÚN TIPO DE USUARIO --------------------
userTypeSelect.addEventListener('change', function () {
    const selectedRole = this.value;
    adminKeyField.style.display = selectedRole === 'admin' ? 'block' : 'none';
    sessionKeyField.style.display = selectedRole === 'student' ? 'block' : 'none';
});

// -------------------- REGISTRO --------------------
signUpForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const nameInput = signUpForm.querySelector('input[name="name"]');
    const emailInput = signUpForm.querySelector('input[name="email"]');
    const passwordInput = signUpForm.querySelector('input[name="password"]');
    const selectedUserType = userTypeSelect.value;
    const adminKeyInput = document.getElementById('adminKey');
    const sessionKeyInput = document.getElementById('sessionKey');

    // Validación de campos vacíos
    if (!nameInput.value || !emailInput.value || !passwordInput.value) {
        mostrarToast("Por favor, completa todos los campos.", 'warning');
        return;
    }

    if (selectedUserType === 'admin' && (!adminKeyInput.value || adminKeyInput.value.trim() === '')) {
        mostrarToast('Por favor, ingresa la llave de administrador.', 'warning');
        return;
    }

    if (selectedUserType === 'student' && (!sessionKeyInput.value || sessionKeyInput.value.trim() === '')) {
        mostrarToast('Por favor, ingresa la clave de sesión proporcionada por tu profesor.', 'warning');
        return;
    }

    // Envío de datos
    const formData = new FormData();
    formData.append('name', nameInput.value);
    formData.append('email', emailInput.value);
    formData.append('password', passwordInput.value);
    formData.append('userType', selectedUserType);
    formData.append('adminKey', adminKeyInput.value);
    formData.append('sessionKey', sessionKeyInput.value);

    fetch('/registro', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarToast('✅ Registro exitoso. Ahora puedes iniciar sesión.', 'success');
            signUpForm.reset();
            container.classList.remove("active");
        } else {
            mostrarToast('❌ Error: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error en la petición de registro:', error);
        mostrarToast('⚠️ Error de conexión con el servidor.', 'error');
    });
});

// -------------------- INICIO DE SESIÓN --------------------
signInForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const userEmailInput = signInForm.querySelector('input[name="user"]');
    const passwordInput = signInForm.querySelector('input[name="password"]');

    // Validación
    if (!userEmailInput.value || !passwordInput.value) {
        mostrarToast("Por favor, ingresa tu usuario y contraseña.", 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('user', userEmailInput.value);
    formData.append('password', passwordInput.value);

    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem('sesion_id', data.sesion_id);
            localStorage.setItem('usuario_id', data.usuario_id);
            localStorage.setItem('user_role', data.rol);

            if (data.rol === 'admin') {
                localStorage.setItem('admin_id', data.usuario_id);
                mostrarToast("Inicio de sesión como administrador.", 'success');
                setTimeout(() => window.location.href = '/PanelAdmin', 1500);
            } else if (data.rol === 'student') {
                mostrarToast("Inicio de sesión como usuario.", 'success');
                setTimeout(() => window.location.href = '/prestamos', 1500);
            }
        } else {
            mostrarToast('❌ Error al iniciar sesión: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error en el login:', error);
        mostrarToast('⚠️ Error al comunicarse con el servidor.', 'error');
    });
});

