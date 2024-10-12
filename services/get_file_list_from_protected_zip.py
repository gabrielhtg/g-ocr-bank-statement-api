import os
import zipfile
from werkzeug.utils import secure_filename

def get_file_list_from_protected_zip(data_file, app, password):
    file = data_file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Ekstrak file zip ke folder EXTRACT_FOLDER
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # 'setpassword' method is used to give a password to the 'Zip'
        zip_ref.setpassword(pwd=bytes(password, 'utf-8'))
        file_list = zip_ref.namelist()
        zip_ref.extractall(app.config['EXTRACT_FOLDER'])

    # aktifkan jika ingin menghapus file
    # os.remove(file_path)

    return file_list