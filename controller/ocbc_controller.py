import os
import uuid
from flask import jsonify, request

from services.ocbc_services.ocbc_ocr_service import doOcrOcbc
from services.utils.check_is_pdf import checkIsPdf
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.get_images_from_pdf import getImagesFromPdf
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
    isPdf = False
    isPdfModified = None
    
    # cek apakah file yang diupload adalah zip
    if len(uploadedFiles) == 1 :
        isZip = checkIsZip(uploadedFiles)
        isPdf = checkIsPdf(uploadedFiles)
        
    if isZip:
        fileList = getFileListFromZip(uploadedFiles[0], app, isZip, isPdf)
            
        if fileList == 400 :
            return returnFailMessage(False, 'Gagal mengekstrak zip! Password salah!')

        else :
            statusCode, data = doOcrOcbc(fileList, app, bankStatementType)

            if statusCode != 200 :
                return returnFailMessage(data, statusCode)
            
    elif isPdf:
        fileList = getImagesFromPdf(uploadedFiles[0], app)
        
        unique_filename = f"{uuid.uuid4().hex}_{uploadedFiles[0].filename}"
        destination_path = os.path.join(app.config['PDF_EXTRACT_FOLDER'], unique_filename)
        uploadedFiles[0].save(destination_path)
        stat = os.stat(destination_path)
        
        if stat.st_mtime == stat.st_ctime :
            isPdfModified = False
            
        else :
            isPdfModified = True
            
        os.remove(destination_path)
            
        statusCode, data = doOcrOcbc(fileList, app, isZip, isPdf)

        if statusCode != 200 :
            return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: int(x.filename.split("_")[-1].split(".")[0]))
        
        statusCode, data = doOcrOcbc(sortedData, app, isZip, isPdf)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

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
            'total_saldo_dalam_idr': data['total_saldo_dalam_idr'],
            'is_pdf_modified' : isPdfModified
        }
    })