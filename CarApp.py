from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cars.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def enter_details():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        license_photo = request.files.get('license_photo')
        email = request.form.get('email')
        mobile = request.form.get('mobile')

        if name and age and license_photo and email and mobile:
            # Save user details to the database or perform necessary actions
            return redirect(url_for('car_selection'))
        else:
            return "Missing required information. Please fill in all fields.", 400
    else:
        return render_template('index.html')

@app.route('/cars')
def car_selection():
    conn = get_db_connection()
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()
    return render_template('car_selection.html', cars=cars)

@app.route('/payment/<int:car_id>', methods=['GET', 'POST'])
def payment(car_id):
    if request.method == 'POST':
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')

        if card_number and expiry_date and cvv:
            # Process payment and complete rental process
            return redirect(url_for('thank_you'))
        else:
            return "Missing payment information. Please fill in all fields.", 400
    else:
        return render_template('payment.html', car_id=car_id)

@app.route('/thankyou')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cars
                        (id INTEGER PRIMARY KEY,
                         brand TEXT NOT NULL,
                         model TEXT NOT NULL,
                         price_per_hour INTEGER NOT NULL)''')
        conn.commit()
        conn.close()
    app.run(debug=True)
