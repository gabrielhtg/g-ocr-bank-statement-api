from flask import request
from services.check_is_zip import checkIsZip

def ocr_bri(app) :
    uploadedFiles = request.files.getlist('files')
    zipPassword = None
    
    # cek apakah file yang diupload adalah zip
    if checkIsZip(uploadedFiles) :
        pass
    
    else :
        bri
    