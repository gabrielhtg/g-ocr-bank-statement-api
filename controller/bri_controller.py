from flask import jsonify, request

from services.bri_services.bri_ocr_service import doOcrBri
from services.bri_services.get_bri_analysis import getBriAnalysisData
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.return_fail_message import returnFailMessage

def briController(app) :
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
            
            statusCode, data = doOcrBri(fileList, app, bankStatementType)

            if statusCode != 200 :
                return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        data = doOcrBri(sortedData, app, bankStatementType)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

    return jsonify({
        'message' : 'ok',
        'data' : {
            'transaction_data' : data['transaction_data'],
            'banyak_data' : len(data['transaction_data']),
            'summary_data' : data['summary_data'],
            'analysis_data' : getBriAnalysisData(data['transaction_data'], data['summary_data']),
            'pemilik_rekening' : data['pemilik_rekening'],
            'tanggal_laporan' : data['tanggal_laporan'],
            'periode_transaksi' : data['periode_transaksi'],
            'alamat' : data['alamat'],
            'nomor_rekening' : data['nomor_rekening'],
            'nama_produk' : data['nama_produk'],
            'valuta' : data['valuta'],
            'unit_kerja' : data['unit_kerja'],
            'alamat_unit_kerja' : data['alamat_unit_kerja']
        }
    })