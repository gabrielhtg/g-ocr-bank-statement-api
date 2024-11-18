from flask import jsonify, request

from services.bni_services.bni_ocr_service import doOcrBni
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.return_fail_message import returnFailMessage

def bniController(app) :
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
            statusCode, data = doOcrBni(fileList, app, bankStatementType)

            if statusCode != 200 :
                return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        statusCode, data = doOcrBni(sortedData, app, bankStatementType)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

    return jsonify({
        'message' : 'ok',
        'data' : {
            'akun_rekening' : data['akun_rekening'],
            'nomor_rekening' : data['nomor_rekening'],
            'tipe_akun' : data['tipe_akun'],
            'periode_rekening' : data['periode_rekening'],
            'pemilik_rekening' : data['pemilik_rekening'],
            'alamat' : data['alamat'],
            'transaction_data' : data['transaction_data'],
            'total_debet_by_ocr' : data['total_debet_by_ocr'],
            'total_kredit_by_ocr' : data['total_kredit_by_ocr'],
            'ending_balance' : data['ending_balance'],
            'total_debet' : data['total_debet'],
            'total_credit' : data['total_credit'],
            'total_debet_amount' : data['total_debet_amount'],
            'total_credit_amount' : data['total_credit_amount'],
            'analytics_data': data['analytics_data']    
        }
    })