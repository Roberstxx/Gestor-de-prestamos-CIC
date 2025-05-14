// -------------------- REFERENCIAS --------------------
const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const userTypeSelect = document.getElementById('userType');
const adminKeyField = document.getElementById('adminKeyField');
const sessionKeyField = document.getElementById('sessionKeyField');
const signUpForm = document.getElementById('signUpForm');
const signInForm = document.querySelector('.sign-in form');

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

    if (!nameInput.value || !emailInput.value || !passwordInput.value) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    if (selectedUserType === 'admin' && (!adminKeyInput.value || adminKeyInput.value.trim() === '')) {
        alert('Por favor, ingresa la llave de administrador.');
        return;
    }

    if (selectedUserType === 'student' && (!sessionKeyInput.value || sessionKeyInput.value.trim() === '')) {
        alert('Por favor, ingresa la clave de sesión proporcionada por tu profesor.');
        return;
    }

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
            alert('✅ Registro exitoso. Ahora puedes iniciar sesión.');
            signUpForm.reset();
            container.classList.remove("active");
        } else {
            alert('❌ Error en el registro: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error en la petición de registro:', error);
        alert('⚠️ Ocurrió un error al comunicarse con el servidor para el registro.');
    });
});

// -------------------- INICIO DE SESIÓN --------------------
signInForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const userEmailInput = signInForm.querySelector('input[name="user"]');
    const passwordInput = signInForm.querySelector('input[name="password"]');

    if (!userEmailInput.value || !passwordInput.value) {
        alert("Por favor, ingresa tu usuario y contraseña.");
        return;
    }

    const formData = new FormData();
    formData.append('user', userEmailInput.value);
    formData.append('password', passwordInput.value);

    fetch('/login', {   // asegúrate de que app.py tenga también @app.route('/login')
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // --- MEJORAS CLAVE AQUÍ ---
            localStorage.setItem('sesion_id', data.sesion_id);
            localStorage.setItem('usuario_id', data.usuario_id); // Guardamos el ID del usuario (admin o estudiante)
            localStorage.setItem('user_role', data.rol);         // Guardamos el rol

            if (data.rol === 'admin') {
                localStorage.setItem('admin_id', data.usuario_id); // ✅  GUARDAR admin_id (usuario_id)
                // Opcional: localStorage.setItem('adminEmail', userEmailInput.value); // Guardar email del admin
                window.location.href = '/PanelAdmin';
            } else if (data.rol === 'student') {
                window.location.href = '/prestamos';
            }

            alert("✅ Inicio de sesión exitoso.");
        } else {
            alert('❌ Error al iniciar sesión: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error en la petición de inicio de sesión:', error);
        alert('⚠️ Ocurrió un error al comunicarse con el servidor para iniciar sesión.');
    });
});
