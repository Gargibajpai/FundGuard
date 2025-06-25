from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USERNAME = 'admin'
PASSWORD = 'admin123'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return 'Invalid file type', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    df['Status'] = '✅ OK'
    df.loc[df['Final Cost'] > 1.5 * df['Estimated Cost'], 'Status'] = '⚠ Over Budget'
    df['Vendor Count'] = df.groupby('Vendor')['Vendor'].transform('count')
    df.loc[df['Vendor Count'] > 3, 'Status'] = '🔁 Vendor Repeat'
    df.drop('Vendor Count', axis=1, inplace=True)

    flagged_path = os.path.join(UPLOAD_FOLDER, 'flagged.csv')
    df.to_csv(flagged_path, index=False)

    data = df.to_dict(orient='records')
    summary = {
        'total': len(df),
        'flagged': len(df[df['Status'] != '✅ OK']),
        'ok': len(df[df['Status'] == '✅ OK']),
        'over': len(df[df['Status'] == '⚠ Over Budget']),
        'repeat': len(df[df['Status'] == '🔁 Vendor Repeat'])
    }

    return render_template('dashboard.html', data=data, summary=summary)

@app.route('/export')
def export():
    return send_file(os.path.join(UPLOAD_FOLDER, 'flagged.csv'), as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)