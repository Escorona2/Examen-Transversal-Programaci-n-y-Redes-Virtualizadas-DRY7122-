import hashlib
import sqlite3
from flask import Flask, request, jsonify

# Función para hashear contraseñas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Datos de usuarios y contraseñas
usuarios_contraseñas = {
    'Estefania Coronado': 'cisco123',
    'Kimberly Valdebenito': 'cisco123',
    'Angelo Carrillo': 'cisco123'
}

# Crear o conectar a la base de datos SQLite
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                (nombre TEXT PRIMARY KEY, password_hash TEXT)''')

# Insertar usuarios y contraseñas hasheadas en la base de datos
for usuario, contraseña in usuarios_contraseñas.items():
    password_hash = hash_password(contraseña)
    cursor.execute('INSERT INTO usuarios VALUES (?, ?)', (usuario, password_hash))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

# Crear aplicación Flask
app = Flask(__name__)

# Ruta principal del sitio web
@app.route('/')
def index():
    return '¡Sitio web en funcionamiento en el puerto 5800!'

# Ruta para validar usuarios
@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    datos = request.get_json()
    usuario = datos['usuario']
    contraseña = datos['contraseña']

    # Conectar a la base de datos y validar usuario
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute('SELECT password_hash FROM usuarios WHERE nombre = ?', (usuario,))
    resultado = cursor.fetchone()

    if resultado:
        password_hash = resultado[0]
        if hash_password(contraseña) == password_hash:
            return jsonify({'mensaje': f'¡Bienvenido, {usuario}!'})
    
    return jsonify({'error': 'Usuario o contraseña incorrectos.'}), 401

if __name__ == '__main__':
    app.run(port=5800)
