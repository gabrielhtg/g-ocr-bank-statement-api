from flask import jsonify, request

from services.mandiri_services.mandiri_ocr_service import doOcrMandiri
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.return_fail_message import returnFailMessage

def mandiriController(app) :
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
            
            data = doOcrMandiri(fileList, app, bankStatementType)

            if data == 400 :
                return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        data = doOcrMandiri(sortedData, app, bankStatementType)
        
        if data == 400 :
            return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')

    return jsonify({
        'message' : 'ok',
        'data' : {
            'period' : data['period'],
            'nomor_rekening' : data['nomor_rekening'],
            'pemilik_rekening' : data['pemilik_rekening'],
            'currency' : data['currency'],
            'branch' : data['branch'],
            'transaction_data' : data['transaction_data'],
            'total_debet' : data['total_debet'],
            'total_kredit' : data['total_kredit'],
            'analytics_data': data['analytics_data']    
        }
    })