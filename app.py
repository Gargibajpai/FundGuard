from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
import pandas as pd
from werkzeug.utils import secure_filename
import os
import json
from io import StringIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def analyze_tenders(df):
    # Create a copy of the dataframe
    df_analyzed = df.copy()
    
    # Calculate over budget flag
    df_analyzed['Over_Budget'] = df_analyzed['Final Cost'] > (1.5 * df_analyzed['Estimated Cost'])
    
    # Calculate vendor repeat flag
    vendor_counts = df_analyzed['Vendor'].value_counts()
    repeat_vendors = vendor_counts[vendor_counts > 3].index
    df_analyzed['Vendor_Repeat'] = df_analyzed['Vendor'].isin(repeat_vendors)
    
    # Set Risk Flag
    df_analyzed['Risk Flag'] = 'OK'
    df_analyzed.loc[df_analyzed['Over_Budget'], 'Risk Flag'] = 'Over Budget'
    df_analyzed.loc[df_analyzed['Vendor_Repeat'], 'Risk Flag'] = 'Vendor Repeat'
    
    # Add color coding for Risk Flag
    df_analyzed['Risk_Color'] = df_analyzed['Risk Flag'].map({
        'OK': 'table-success',
        'Over Budget': 'table-danger',
        'Vendor Repeat': 'table-warning'
    })
    
    return df_analyzed

if __name__ == '__main__':
    print("✅ Running app.py")
    app.run(debug=True)


@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/about')
def about():
    """About page route - static content, only needs GET method"""
    return render_template('about.html')

@app.route('/upload', methods=['GET'])
def upload_page():
    """Upload form page route"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle CSV file uploads from the HTML form submission.
    WARNING: This route is intended to be accessed only via form submission, not directly.
    """
    file = request.files.get('file')
    if not file or file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('upload_page'))
    
    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file', 'error')
        return redirect(url_for('upload_page'))
    
    try:
        # Ensure uploads directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'latest.csv')
        file.save(file_path)
        
        # Read and validate the CSV
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['Department', 'Vendor', 'Estimated Cost', 'Final Cost', 'State']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            os.remove(file_path)  # Clean up the invalid file
            flash(f'CSV file is missing required columns: {", ".join(missing_columns)}', 'error')
            return redirect(url_for('upload_page'))
        
        # Analyze the data
        df_analyzed = analyze_tenders(df)
        
        # Save the analyzed data
        df_analyzed.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'current_data.csv'), index=False)
        
        flash('File uploaded and analyzed successfully', 'success')
        return redirect(url_for('dashboard'))
        
    except pd.errors.EmptyDataError:
        flash('The uploaded CSV file is empty', 'error')
        return redirect(url_for('upload_page'))
    except pd.errors.ParserError:
        flash('Unable to parse CSV file. Please check the file format', 'error')
        return redirect(url_for('upload_page'))
    except Exception as e:
        flash(f'An error occurred while processing the file: {str(e)}', 'error')
        return redirect(url_for('upload_page'))

@app.route('/dashboard')
def dashboard():
    """Dashboard page route"""
    try:
        # Check if we have analyzed data
        data_file = os.path.join(app.config['UPLOAD_FOLDER'], 'current_data.csv')
        if not os.path.exists(data_file):
            flash('Please upload tender data first', 'error')
            return redirect(url_for('upload_page'))

        # Read the latest uploaded file
        df = pd.read_csv(data_file)
        
        # Get unique departments and states for filters
        departments = sorted(df['Department'].unique().tolist())
        states = sorted(df['State'].unique().tolist())
        
        # Prepare dashboard data
        total_tenders = len(df)
        flagged_tenders = len(df[df['Risk Flag'] != 'OK'])
        risk_distribution = df['Risk Flag'].value_counts().to_dict()
        
        return render_template('dashboard.html',
                             table=df.to_html(classes='table table-striped', index=False,
                                            escape=False, table_id='tendersTable',
                                            columns=[col for col in df.columns if col != 'Risk_Color']),
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

@app.route('/filter', methods=['POST'])
def filter_data():
    """Handle dashboard filter requests"""
    try:
        df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'current_data.csv'))
        
        # Get filter parameters
        department = request.json.get('department')
        state = request.json.get('state')
        
        # Apply filters
        if department:
            df = df[df['Department'] == department]
        if state:
            df = df[df['State'] == state]
        
        # Update dashboard data
        total_tenders = len(df)
        flagged_tenders = len(df[df['Risk Flag'] != 'OK'])
        risk_distribution = df['Risk Flag'].value_counts().to_dict()
        
        # Convert filtered DataFrame to HTML table
        table_html = df.to_html(classes='table table-striped', index=False,
                              escape=False, table_id='tendersTable',
                              columns=[col for col in df.columns if col != 'Risk_Color'])
        
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