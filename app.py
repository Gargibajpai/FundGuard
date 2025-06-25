from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'supersecretkey'  # Required for flash messages and sessions

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

USERNAME = 'admin'
PASSWORD = 'admin123'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_tenders(df):
    df_analyzed = df.copy()
    df_analyzed['Over_Budget'] = df_analyzed['Final Cost'] > (1.5 * df_analyzed['Estimated Cost'])
    vendor_counts = df_analyzed['Vendor'].value_counts()
    repeat_vendors = vendor_counts[vendor_counts > 3].index
    df_analyzed['Vendor_Repeat'] = df_analyzed['Vendor'].isin(repeat_vendors)
    df_analyzed['Risk Flag'] = 'OK'
    df_analyzed.loc[df_analyzed['Over_Budget'], 'Risk Flag'] = 'Over Budget'
    df_analyzed.loc[df_analyzed['Vendor_Repeat'], 'Risk Flag'] = 'Vendor Repeat'
    df_analyzed['Risk_Color'] = df_analyzed['Risk Flag'].map({
        'OK': 'table-success',
        'Over Budget': 'table-danger',
        'Vendor Repeat': 'table-warning'
    })
    return df_analyzed

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
            flash('You were successfully logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    """About page route - static content, only needs GET method"""
    return render_template('about.html')

@app.route('/upload', methods=['GET'])
def upload_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            df = pd.read_csv(file_path)
            
            required_columns = ['Department', 'Vendor', 'Estimated Cost', 'Final Cost', 'State']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                os.remove(file_path)
                flash(f'CSV file is missing required columns: {", ".join(missing_columns)}', 'error')
                return redirect(url_for('upload_page'))
            
            df_analyzed = analyze_tenders(df)
            
            analyzed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'current_data.csv')
            df_analyzed.to_csv(analyzed_file_path, index=False)
            
            flash('File uploaded and analyzed successfully', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            flash(f'An error occurred while processing the file: {str(e)}', 'error')
            return redirect(url_for('upload_page'))
    else:
        flash('Allowed file type is CSV', 'error')
        return redirect(url_for('upload_page'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        data_file = os.path.join(app.config['UPLOAD_FOLDER'], 'current_data.csv')
        if not os.path.exists(data_file):
            return redirect(url_for('upload_page'))

        df = pd.read_csv(data_file)
        
        departments = sorted(df['Department'].unique().tolist())
        states = sorted(df['State'].unique().tolist())
        
        total_tenders = len(df)
        flagged_tenders = len(df[df['Risk Flag'] != 'OK'])
        risk_distribution = df['Risk Flag'].value_counts().to_dict()
        
        table_html = df.to_html(classes='table table-striped', index=False, escape=False, table_id='tendersTable', columns=[col for col in df.columns if col != 'Risk_Color'])
        
        return render_template('dashboard.html',
                             table=table_html,
                             dashboard_data={
                                 'total_tenders': total_tenders,
                                 'flagged_tenders': flagged_tenders,
                                 'risk_distribution': risk_distribution,
                                 'departments': departments,
                                 'states': states
                             })
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('upload_page'))

@app.route('/export')
def export():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'current_data.csv'), as_attachment=True)


@app.route('/filter', methods=['POST'])
def filter_data():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'current_data.csv'))
        
        department = request.json.get('department')
        state = request.json.get('state')
        
        if department:
            df = df[df['Department'] == department]
        if state:
            df = df[df['State'] == state]
        
        total_tenders = len(df)
        flagged_tenders = len(df[df['Risk Flag'] != 'OK'])
        risk_distribution = df['Risk Flag'].value_counts().to_dict()
        
        table_html = df.to_html(classes='table table-striped', index=False, escape=False, table_id='tendersTable', columns=[col for col in df.columns if col != 'Risk_Color'])
        
        return jsonify({
            'success': True,
            'table': table_html,
            'dashboard': {
                'total_tenders': total_tenders,
                'flagged_tenders': flagged_tenders,
                'risk_distribution': risk_distribution
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
