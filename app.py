# ...existing code...
from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime
import os
import traceback

# DB config
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "")
DB_NAME = os.environ.get("DB_NAME", "smart_bike_db")

def get_db_connection():
    return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "devsecret")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        pwd = request.form.get('password')
        if not (name and email and pwd):
            return render_template('register.html', error="Fill all fields")
        db = get_db_connection()
        cur = db.cursor()
        hashed = generate_password_hash(pwd)
        try:
            cur.execute("INSERT INTO students (name,email,password,wallet_balance) VALUES (%s,%s,%s,%s)", (name,email,hashed,0))
            db.commit()
        except Exception as e:
            db.close()
            return render_template('register.html', error="Email already used")
        db.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')
        db = get_db_connection()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cur.fetchone()
        db.close()
        if user and check_password_hash(user['password'], pwd):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM bicycles")
    bikes = cur.fetchall()
    db.close()
    return render_template('dashboard.html', bikes=bikes, username=session.get('user_name'))

@app.route('/wallet', methods=['GET','POST'])
def wallet():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    user_id = session['user_id']
    if request.method == 'POST':
        amt = float(request.form.get('amount', 0))
        cur.execute("UPDATE students SET wallet_balance = wallet_balance + %s WHERE id=%s", (amt, user_id))
        db.commit()
    cur.execute("SELECT wallet_balance FROM students WHERE id=%s", (user_id,))
    bal = cur.fetchone()
    db.close()
    return render_template('wallet.html', balance=(bal['wallet_balance'] if bal else 0))

@app.route('/scan')
def scan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('scan.html')


# ...existing code...

@app.route('/api/unlock', methods=['POST'])
def unlock():
    if 'user_id' not in session:
        return jsonify({'status':'fail', 'msg':'Please log in.'}), 401
    
    user_id = session['user_id']
    data = request.get_json()
    
    # Get bike_id from request (could be "BIKE-QR-001" or just "101")
    bike_identifier = str(data.get('bike_id', '')).strip()
    
    if not bike_identifier:
        return jsonify({'status':'fail','msg':'No bike ID provided'}), 400
    
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    
    # Check wallet balance (minimum ₹10 required)
    cur.execute("SELECT wallet_balance FROM students WHERE id=%s", (user_id,))
    user = cur.fetchone()
    
    if not user:
        db.close()
        return jsonify({'status':'fail','msg':'User not found'}), 404
    
    balance = user['wallet_balance']
    
    if balance < 10:
        db.close()
        return jsonify({'status':'fail','msg':'Insufficient balance. Minimum ₹10 required'}), 400
    
    # Try to find bike by qr_code OR bike_id
    cur.execute("""
        SELECT * FROM bicycles 
        WHERE (qr_code=%s OR bike_id=%s) AND is_available=TRUE
    """, (bike_identifier, bike_identifier))
    
    bike = cur.fetchone()
    
    if not bike:
        db.close()
        return jsonify({'status':'fail','msg':'Bike not available or not found'}), 404
    
    # Mark bike as in use
    cur.execute("""
        UPDATE bicycles 
        SET is_available=FALSE, status='in_use' 
        WHERE bike_id=%s
    """, (bike['bike_id'],))
    
    # Store ride start time in session
    session[f'ride_start_{bike["bike_id"]}'] = datetime.now().isoformat()
    
    db.commit()
    db.close()
    
    return jsonify({
        'status':'success',
        'msg':f'Bike {bike["bike_id"]} unlocked! ₹10 initial charge applied.',
        'bike_id': bike['bike_id']
    }), 200


@app.route('/api/end_ride', methods=['POST'])
def end_ride():
    if 'user_id' not in session:
        return jsonify({'status':'error','msg':'Not authenticated'}), 401
    payload = request.get_json(silent=True) or {}
    bike_id = payload.get('bike_id')
    if not bike_id:
        return jsonify({'status':'error','msg':'No bike specified'}), 400
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    # find ongoing ride for this user and bike
    cur.execute("SELECT * FROM rides WHERE user_id=%s AND bike_id=%s AND status='ongoing' ORDER BY start_time DESC LIMIT 1", (session['user_id'], bike_id))
    ride = cur.fetchone()
    if not ride:
        db.close()
        return jsonify({'status':'error','msg':'No ongoing ride found'}), 404
    end = datetime.now()
    duration_min = max(1, int((end - ride['start_time']).total_seconds() / 60))
    fare = 10.0  # fixed for simplicity
    cur.execute("UPDATE rides SET end_time=%s, fare=%s, status='completed' WHERE id=%s", (end, fare, ride['id']))
    cur.execute("UPDATE bicycles SET is_available=1, status='idle' WHERE bike_id=%s", (bike_id,))
    cur.execute("INSERT INTO transactions (user_id, amount, type, created_at) VALUES (%s,%s,%s,%s)", (session['user_id'], -fare, 'ride_fare', end))
    db.commit()
    db.close()
    return jsonify({'status':'success','msg':'Ride ended', 'fare': fare})

@app.route('/admin', methods=['GET','POST'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    if request.method == 'POST':
        location = request.form.get('location','Campus')
        cur.execute("SELECT MAX(bike_id) AS max_id FROM bicycles")
        r = cur.fetchone()
        next_id = (r['max_id'] or 100) + 1
        qr_code = f"BIKE-QR-{(next_id-100):03d}"
        cur.execute("INSERT INTO bicycles (bike_id, qr_code, is_available, location, status) VALUES (%s,%s,1,%s,'idle')", (next_id, qr_code, location))
        db.commit()
    cur.execute("SELECT * FROM bicycles")
    bikes = cur.fetchall()
    db.close()
    return render_template('admin.html', bikes=bikes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



# ...existing code...
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)