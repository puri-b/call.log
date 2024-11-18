import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ฟังก์ชันสำหรับสร้างฐานข้อมูล
def init_db():
    conn = sqlite3.connect('call_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS call_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            customer_name TEXT,
            phone_number TEXT,
            call_date TEXT,
            service TEXT,
            call_result TEXT,
            notes TEXT,
            caller TEXT,
            call_duration TEXT
        )
    ''')
    conn.commit()
    conn.close()

# เรียกฟังก์ชันเพื่อสร้างฐานข้อมูล
init_db()

# หน้าแรกของโปรแกรม
@app.route('/')
def home():
    return render_template('home.html')

# ฟังก์ชันสำหรับเพิ่มบันทึกการโทร
@app.route('/add_call', methods=['GET', 'POST'])
def add_call():
    if request.method == 'POST':
        # ดึงข้อมูลจากฟอร์ม
        company = request.form['company']
        customer_name = request.form['customer_name']
        phone_number = request.form['phone_number']
        call_date = request.form['call_date']
        service = request.form['service']
        call_result = request.form['call_result']
        notes = request.form['notes']
        caller = request.form['caller']
        call_duration = request.form['call_duration']

        # บันทึกข้อมูลลงฐานข้อมูล
        conn = sqlite3.connect('call_logs.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO call_logs (company, customer_name, phone_number, call_date, service, call_result, notes, caller, call_duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (company, customer_name, phone_number, call_date, service, call_result, notes, caller, call_duration))
        conn.commit()
        conn.close()

        return redirect(url_for('add_call'))

    # ดึงข้อมูลทั้งหมดจากฐานข้อมูล
    conn = sqlite3.connect('call_logs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM call_logs')
    call_logs = cursor.fetchall()
    conn.close()

    return render_template('add_call.html', calls=call_logs)

# ฟังก์ชันสำหรับกรองข้อมูล
@app.route('/filter', methods=['GET'])
def filter_calls():
    date_filter = request.args.get('date')
    caller_filter = request.args.get('caller')

    query = 'SELECT * FROM call_logs WHERE 1=1'
    params = []

    if date_filter:
        query += ' AND call_date = ?'
        params.append(date_filter)
    
    if caller_filter:
        query += ' AND caller = ?'
        params.append(caller_filter)

    conn = sqlite3.connect('call_logs.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    filtered_calls = cursor.fetchall()
    conn.close()

    return render_template('add_call.html', calls=filtered_calls)

if __name__ == '__main__':
    app.run(debug=True)
