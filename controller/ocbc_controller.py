from flask import jsonify, request

from services.ocbc_services.ocbc_ocr_service import doOcrOcbc
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.return_fail_message import returnFailMessage

def ocbcController(app) :
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
            fileList.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
            
            data = doOcrOcbc(fileList, app, bankStatementType)

            if data == 400 :
                return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: int(x.filename.split("_")[-1].split(".")[0]))
        
        data = doOcrOcbc(sortedData, app, bankStatementType)
        
        if data == 400 :
            return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')

    return jsonify({
        'message' : 'ok',
        'data' : {
            'pemilik_rekening' : data['pemilik_rekening'],
            'alamat' : data['alamat'],
            'nomor_rekening' : data['nomor_rekening'],
            'cabang' : data['cabang'],
            'periode' : data['periode'],
            'tanggal_percetakan' : data['tanggal_percetakan'],
            'mata_uang' : data['mata_uang'],
            'transaction_data' : data['transaction_data'],
            'total_debet' : data['total_debet'],
            'total_kredit' : data['total_kredit'],
            'analytics_data': data['analytics_data'],
            'tunggakan_bunga': data['tunggakan_bunga'],
            'tunggakan_denda': data['tunggakan_denda'],
            'tunggakan_biaya_lain': data['tunggakan_biaya_lain'],
            'total_tunggakan': data['total_tunggakan'],
            'kurs_valas_idr': data['kurs_valas_idr'],
            'saldo_dalam_mata_uang_idr': data['saldo_dalam_mata_uang_idr'],
            'total_saldo_dalam_idr': data['total_saldo_dalam_idr']
        }
    })