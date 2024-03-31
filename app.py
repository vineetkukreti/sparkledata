from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

import pandas as pd
import os
from AutoClean.autoclean import AutoClean

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
CLEANED_FOLDER = 'cleaned'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CLEANED_FOLDER'] = CLEANED_FOLDER

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', message='No selected file')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Perform cleaning
        df = pd.read_csv(file_path)
        print(filename)
        pipeline = AutoClean(df,filename)
        cleaned_df = pipeline.output
        cleaned_folder_path = app.config['CLEANED_FOLDER']
        if not os.path.exists(cleaned_folder_path):
            os.makedirs(cleaned_folder_path)
        
        # Save cleaned DataFrame to CSV file
        cleaned_filename = f"cleaned_{filename}"
        cleaned_file_path = os.path.join(cleaned_folder_path, cleaned_filename)
        cleaned_df.to_csv(cleaned_file_path, index=False)
        
        return send_file(cleaned_file_path, as_attachment=True)
    else:
        return render_template('index.html', message='File type not allowed')

if __name__ == '__main__':
    app.run(debug=True)
