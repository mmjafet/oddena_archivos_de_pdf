from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import uuid
from werkzeug.utils import secure_filename
from pdf_processor import process_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload and download folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.endswith('.pdf'):
        # Generate unique filename for both input and output
        unique_id = str(uuid.uuid4())
        input_filename = f"{unique_id}_input.pdf"
        output_filename = f"{unique_id}_sorted.pdf"
        
        # Save uploaded file
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)
        file.save(input_path)
        
        # Process PDF
        try:
            process_pdf(input_path, output_path)
            return render_template('result.html', filename=output_filename)
        except Exception as e:
            return render_template('index.html', error=f"Error processing PDF: {str(e)}")
    
    return redirect(request.url)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), 
                     as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)