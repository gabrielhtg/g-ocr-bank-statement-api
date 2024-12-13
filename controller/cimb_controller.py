import os
import uuid
from flask import jsonify, request

from services.cimb_services.cimb_ocr_service import doOcrCimb
from services.utils.check_is_pdf import checkIsPdf
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.get_images_from_pdf import getImagesFromPdf
from services.utils.return_fail_message import returnFailMessage

def cimbController(app, logger) :
    username = request.headers.get('X-Username')
    
    logger.info(f"{username} : '/proceed-cimb', methods=['POST']")
    
    uploadedFiles = request.files.getlist('files')
    zipPassword = ''
    
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
        fileList = getFileListFromZip(uploadedFiles[0], app, zipPassword)
            
        if fileList == 400 :
            return returnFailMessage(False, 'Gagal mengekstrak zip! Password salah!')

        else :
            statusCode, data = doOcrCimb(fileList, app, isZip, isPdf, logger, username)

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
            
        statusCode, data = doOcrCimb(fileList, app, isZip, isPdf, logger, username)

        if statusCode != 200 :
            return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        statusCode, data = doOcrCimb(sortedData, app, isZip, isPdf, logger, username)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

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
            'is_pdf_modified': isPdfModified 
        }
    })