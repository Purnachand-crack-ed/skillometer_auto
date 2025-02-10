from flask import Flask, render_template, request, send_from_directory, redirect, url_for, send_file
import os
import shutil
import pandas as pd
from candidate_report import generate_reports  # Correct import

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORT_FOLDER'] = 'reports'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Generate reports
        try:
            generate_reports(filepath, app.config['REPORT_FOLDER'])  # Correct function call
            df = pd.read_csv(filepath)
            for _, row in df.iterrows():
                skill_chart = os.path.join(app.config['REPORT_FOLDER'], f"{row['Name']}_skills.png")
                performance_meter = os.path.join(app.config['REPORT_FOLDER'], f'rating_meter_{row["Aptitude Score"]}.html')
                return render_template('success.html', skill_chart=skill_chart, performance_meter=performance_meter)
        except Exception as e:
            return f"Error generating reports: {str(e)}", 500
    else:
        return "Invalid file format. Please upload a CSV file.", 400
    
# Define the ZIP folder
app.config['ZIP_FOLDER'] = 'zipped_reports'
os.makedirs(app.config['ZIP_FOLDER'], exist_ok=True)

@app.route('/download_all_reports')
def download_all_reports():
    zip_path = os.path.join(app.config['ZIP_FOLDER'], 'reports.zip')
    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', app.config['REPORT_FOLDER'])
    return send_file(zip_path, as_attachment=True)

@app.route('/reports/<filename>')
def download_report(filename):
    return send_from_directory(app.config['REPORT_FOLDER'], filename)

if __name__ == '__main__':
    app.run()
