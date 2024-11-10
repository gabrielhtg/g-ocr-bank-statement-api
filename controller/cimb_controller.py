from flask import jsonify, request

from services.cimb_services.cimb_ocr_service import doOcrCimb
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.return_fail_message import returnFailMessage

def cimbController(app) :
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
            
            data = doOcrCimb(fileList, app, bankStatementType)

            if data == 400 :
                return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        data = doOcrCimb(sortedData, app, bankStatementType)
        
        if data == 400 :
            return returnFailMessage(False, 'Tipe dari bank statement tidak sama!')

    return jsonify({
        'message' : 'ok',
        'data' : {
            'pemilik_rekening' : data['pemilik_rekening'],
            'alamat' : data['alamat'],
            'periode_laporan' : data['periode_laporan'],
            'tanggal_laporan' : data['tanggal_laporan'],
            'tanggal_pembukaan' : data['tanggal_pembukaan'],
            'nomor_rekening' : data['nomor_rekening'],
            'nama_produk': data['nama_produk'],    
            'nomor_cif': data['nomor_cif'],    
            'mata_uang': data['mata_uang'],   
            'transaction_data': data['transaction_data'],   
            'total_debet': data['total_debet'],   
            'total_kredit': data['total_kredit'],   
            'analytics_data': data['analytics_data'],   
        }
    })