from flask import jsonify, request

from services.permata_services.permata_ocr_service import doOcrPermata
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.return_fail_message import returnFailMessage

def permataController(app) :
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
            return returnFailMessage('Gagal mengekstrak zip! Password salah!', 400)

        else :
            fileList.sort()
            
            statusCode, data = doOcrPermata(fileList, app, bankStatementType)

            if statusCode != 200 :
                return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        statusCode, data = doOcrPermata(sortedData, app, bankStatementType)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

    return jsonify({
        'message' : 'ok',
        'data' : {
            'pemilik_rekening' : data['pemilik_rekening'],
            'alamat' : data['alamat'],
            'periode_laporan' : data['periode_laporan'],
            'tanggal_laporan' : data['tanggal_laporan'],
            'nomor_rekening' : data['nomor_rekening'],
            'cabang' : data['cabang'],
            'nama_produk' : data['nama_produk'],
            'mata_uang' : data['mata_uang'],
            'no_cif':  data['no_cif'],
            'transaction_data' : data['transaction_data'],
            'total_debet' : data['total_debet'],
            'total_kredit' : data['total_kredit'],
            'analytics_data': data['analytics_data']    
        }
    })