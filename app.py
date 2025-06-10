from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User, Hobby
from db import dbConnection
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'supersecreto'
db = dbConnection()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        if not nombre or not email or not password:
            return render_template('register.html', error='Todos los campos son obligatorios.')

        existing_user = db['users'].find_one({'email': email})
        if existing_user:
            return render_template('register.html', error='El correo ya está registrado.')

        new_user = User(nombre, email, password)
        db['users'].insert_one(new_user.toDBCollection())
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        user_data = db['users'].find_one({'email': email})
        if user_data and user_data.get('password') == password:
            session['user_id'] = str(user_data['_id'])
            session['nombre'] = user_data['nombre']
            return redirect(url_for('inicio'))
        else:
            return render_template('login.html', error='Credenciales inválidas.')

    return render_template('login.html')

@app.route('/index')
def inicio():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    hobbies = list(db['hobbies'].find({'user_id': session['user_id']}))
    return render_template('index.html', nombre=session['nombre'], hobbies=hobbies)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_hobby', methods=['GET', 'POST'])
def add_hobby():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        level = request.form.get('level', '').strip()
        percentage = request.form.get('percentage', '').strip()

        if not description or not level or not percentage:
            flash('Todos los campos son obligatorios.')
            return redirect(url_for('add_hobby'))

        try:
            percentage = int(percentage)
        except ValueError:
            flash('El porcentaje debe ser un número.')
            return redirect(url_for('add_hobby'))

        if percentage < 0 or percentage > 100:
            flash('El porcentaje debe estar entre 0 y 100.')
            return redirect(url_for('add_hobby'))

        new_hobby = {
            "user_id": session['user_id'],
            "description": description,
            "level": level,
            "percentage": percentage
        }

        try:
            result = db['hobbies'].insert_one(new_hobby)
            flash('¡Hobby agregado exitosamente!')
        except Exception as e:
            print("Error al guardar en la base de datos:", e)
            flash('Error al guardar en la base de datos.')

        return redirect(url_for('inicio'))

    return render_template('add_hobby.html')

@app.route('/delete_hobby/<id>', methods=['POST'])
def delete_hobby(id):
    try:
        db['hobbies'].delete_one({'_id': ObjectId(id)})
        flash('Hobby eliminado con éxito')
    except Exception as e:
        print("Error al eliminar el hobby:", e)
        flash('Error al eliminar el hobby.')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=777, debug=True)

