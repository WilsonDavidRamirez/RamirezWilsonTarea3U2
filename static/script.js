window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('registroForm');

  form.addEventListener('submit', function (e) {
    const pass = document.getElementById('password').value;
    const confirm = document.getElementById('confirmPassword').value;

    if (pass !== confirm) {
      alert("Las contraseñas no coinciden.");
      e.preventDefault();
    }

    const strongPassword = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
    if (!strongPassword.test(pass)) {
      alert("La contraseña debe tener al menos una mayúscula, un número y 8 caracteres.");
      e.preventDefault();
    }
  });
});
