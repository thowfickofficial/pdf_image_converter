import os
from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_path
from img2pdf import convert

app = Flask(__name__)

# Define a folder to store temporary files
TEMP_FOLDER = 'temp_files'
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pdf_to_image', methods=['POST'])
def pdf_to_image():
    # Check if the POST request has the file part
    if 'pdf_file' not in request.files:
        return "No file part"

    file = request.files['pdf_file']

    if file.filename == '':
        return "No selected file"

    # Save the uploaded PDF file to the temporary folder
    pdf_path = os.path.join(TEMP_FOLDER, file.filename)
    file.save(pdf_path)

    # Convert the PDF to images and save them in the temporary folder
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(TEMP_FOLDER, f'page_{i}.jpg')
        image.save(image_path, 'JPEG')
        image_paths.append(image_path)

    # Return a list of image paths
    return {'image_paths': image_paths}


@app.route('/image_to_pdf', methods=['POST'])
def image_to_pdf():
    # Check if the POST request has the file part
    if 'image_files' not in request.files:
        return "No file part"

    files = request.files.getlist('image_files')

    if not files:
        return "No selected file"

    # Save the uploaded image files to the temporary folder
    image_paths = []
    for file in files:
        image_path = os.path.join(TEMP_FOLDER, file.filename)
        file.save(image_path)
        image_paths.append(image_path)

    # Convert the images to a PDF file and save it in the temporary folder
    pdf_path = os.path.join(TEMP_FOLDER, 'output.pdf')
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(convert(image_paths))

    # Return the path to the generated PDF file
    return {'pdf_path': pdf_path}


if __name__ == '__main__':
    app.run(debug=True)
