from io import BytesIO
import pyzipper

# fungsi ini digunakan untuk melakukan ekstraksi terhadap zip
def getFileListFromZip (dataFile, app, zipPassword):
    # Ekstrak file zip ke folder EXTRACT_FOLDER
    with pyzipper.AESZipFile(BytesIO(dataFile.read()), 'r') as zip_ref:
        try:
            # Gunakan kata sandi untuk membuka zip
            zip_ref.pwd = zipPassword.encode('utf-8')
            
            file_list = zip_ref.namelist()
            zip_ref.extractall(app.config['EXTRACT_FOLDER'])
        except (RuntimeError, pyzipper.BadZipFile, pyzipper.LargeZipFile) as e:
            return 400

    return file_list