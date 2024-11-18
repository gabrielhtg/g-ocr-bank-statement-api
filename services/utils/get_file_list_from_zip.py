from io import BytesIO
import os
import uuid
import pyzipper

# fungsi ini digunakan untuk melakukan ekstraksi terhadap zip
def getFileListFromZip (dataFile, app, zipPassword):
    extracted_files = []
    
    # Ekstrak file zip ke folder EXTRACT_FOLDER
    with pyzipper.AESZipFile(BytesIO(dataFile.read()), 'r') as zip_ref:
        try:
            # Gunakan kata sandi untuk membuka zip
            zip_ref.pwd = zipPassword.encode('utf-8')
            
            file_list = zip_ref.namelist()
            # file_list.sort()
            file_list.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
            
            for file_name in file_list:
                unique_filename = f"{uuid.uuid4().hex}_{os.path.basename(file_name)}"
                destination_path = os.path.join(app.config['EXTRACT_FOLDER'], unique_filename)
                
                # Simpan file yang diekstrak dengan nama unik
                with open(destination_path, 'wb') as extracted_file:
                    extracted_file.write(zip_ref.read(file_name))
                
                # Tambahkan nama file baru ke daftar
                extracted_files.append(unique_filename)
            # zip_ref.extractall(app.config['EXTRACT_FOLDER'])
        except (RuntimeError, pyzipper.BadZipFile, pyzipper.LargeZipFile) as e:
            return 400

    return extracted_files