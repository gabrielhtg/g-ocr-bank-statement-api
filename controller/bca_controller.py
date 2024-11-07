from flask import jsonify, request

from services.bca_services.ocr_service import doOcrBca
from services.bri_services.bri_ocr_service import doOcrBri
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.return_fail_message import returnFailMessage

def bcaController(app) :
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
            
            data = doOcrBca(fileList, app, bankStatementType)

            if data == 400 :
                return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        data = doOcrBca(sortedData, app, bankStatementType)
        
        if data == 400 :
            return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')

    return jsonify({
        'message' : 'ok',
        'data' : {
            'kcp' : data['kcp'],
            'pemilik_rekening' : data['pemilik_rekening'],
            'alamat' : data['alamat'],
            'nomor_rekening' : data['nomor_rekening'],
            'periode' : data['periode'],
            'mata_uang' : data['mata_uang'],
            'saldo_awal' : data['saldo_awal'],
            'saldo_akhir' : data['saldo_akhir'],
            'mutasi_debit' : data['mutasi_debit'],
            'mutasi_kredit' : data['mutasi_kredit'],
            'total_mutasi_debit' : data['total_mutasi_debit'],
            'total_mutasi_kredit' : data['total_mutasi_kredit'],
            'transaction_data' : data['transaction_data'],
            'total_debet' : data['total_debit'],
            'total_kredit' : data['total_kredit'],
            # 'analytics_data': data['analytics_data']    
        }
    })