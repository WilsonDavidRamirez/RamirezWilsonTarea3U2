from flask import Flask, render_template, request, redirect, flash
import sqlite3
import re
from werkzeug.security import generate_password_hash
from flask import g

app = Flask(__name__)
app.secret_key = "secreto123"

DATABASE = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            edad INTEGER,
            biografia TEXT,
            rol TEXT
        )
    ''')
    conn.commit()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/registro', methods=['POST'])
def registro():
    data = request.form
    errores = []

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    confirm = data.get('confirmPassword', '').strip()
    edad = data.get('edad')
    biografia = data.get('bio', '').strip()
    rol = data.get('rol')

    # Validaciones del lado del servidor
    if not username or not email or not password or not confirm or not edad or not rol:
        errores.append("Todos los campos obligatorios deben estar completos.")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errores.append("Correo inválido.")

    if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"\d", password):
        errores.append("La contraseña debe tener mínimo 8 caracteres, una mayúscula y un número.")

    if password != confirm:
        errores.append("Las contraseñas no coinciden.")

    if not edad.isdigit() or not (18 <= int(edad) <= 99):
        errores.append("Edad debe ser un número entre 18 y 99.")

    if len(biografia) > 200:
        errores.append("La biografía no debe exceder 200 caracteres.")

    if errores:
        for e in errores:
            flash(e)
        return redirect('/')

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, email, password, edad, biografia, rol) VALUES (?, ?, ?, ?, ?, ?)",
                       (username, email, generate_password_hash(password), int(edad), biografia, rol))
        conn.commit()
        flash("Registro exitoso")
    except sqlite3.IntegrityError:
        flash("El correo ya está registrado.")
    except Exception as e:
        flash(f"Error al registrar: {str(e)}")

    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        create_table()
    app.run(debug=True)
