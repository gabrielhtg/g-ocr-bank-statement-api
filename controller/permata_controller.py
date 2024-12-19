import datetime
import os
import uuid
from flask import jsonify, request

from services.permata_services.permata_ocr_service import doOcrPermata
from services.utils.check_is_pdf import checkIsPdf
from services.utils.check_is_zip import checkIsZip
from services.utils.get_file_list_from_zip import getFileListFromZip
from services.utils.get_images_from_pdf import getImagesFromPdf
from services.utils.return_fail_message import returnFailMessage

def permataController(app, logger) :
    username = request.headers.get('X-Username')
    
    logger.info(f"{username} : '/proceed-permata', methods=['POST']")
    
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
        logger.info(f"{username} : Proceed Permata Zip")
        logger.info(f"{username} : Zip filename {uploadedFiles[0].filename}")
        fileList = getFileListFromZip(uploadedFiles[0], app, zipPassword)
            
        if fileList == 400 :
            return returnFailMessage('Gagal mengekstrak zip! Password salah!', 400)

        else :
            statusCode, data = doOcrPermata(fileList, app, isZip, isPdf, logger, username)

            if statusCode != 200 :
                return returnFailMessage(data, statusCode)
            
    elif isPdf:
        logger.info(f"{username} : Proceed Permata PDF")
        logger.info(f"{username} : PDF filename {uploadedFiles[0].filename}")
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
            
        statusCode, data = doOcrPermata(fileList, app, isZip, isPdf, logger, username)

        if statusCode != 200 :
            return returnFailMessage(data, statusCode)
            
    else :
        sortedData = sorted(uploadedFiles, key=lambda x: x.filename)
        
        statusCode, data = doOcrPermata(sortedData, app, isZip, isPdf, logger, username)
        
        if statusCode != 200 :
            return returnFailMessage(data, statusCode)

    logger.info(f"{username} : Proceed Permata Success, {statusCode}")
    
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
            'analytics_data': data['analytics_data'],
            'is_pdf_modified':  isPdfModified,
            'banyak_halaman': data['banyak_halaman'],
        }
    })