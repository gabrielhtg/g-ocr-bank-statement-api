from flask import jsonify, request
from services.bri_ocr_service import do_ocr_bri
from services.check_is_zip import checkIsZip
from services.get_file_list_from_zip import getFileListFromZip
from services.returnFailMessage import returnFailMessage

def bri_controller(app) :
    uploadedFiles = request.files.getlist('files')
    zipPassword = ''
    bankStatementType = request.form.get('bank-statement-type')
    
    if request.form.get('zip-password') :
        zipPassword = request.form.get('zip-password')
    
    # variable ini menyimpan apakah file yang diupload adalah 
    # file zip atau bukan. 
    isZip = False
    
    # cek apakah file yang diupload adalah zip
    if len(uploadedFiles) == 1 :
        isZip = checkIsZip(uploadedFiles)
        
    if isZip:
        fileList = getFileListFromZip(uploadedFiles[0], app, zipPassword)
            
        if fileList == 400 :
            return returnFailMessage(False, 'Gagal mengekstrak zip! Password salah!')

        else :
            fileList.sort()
            
            transactionData = do_ocr_bri(fileList, app, bankStatementType)

            if transactionData == 400 :
                return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')

    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        transactionData = do_ocr_bri(sortedData, app, bankStatementType)
        
        if transactionData == 400 :
                return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')

    return jsonify({
        'data' : transactionData,
        'banyak_data' : len(transactionData)
    })